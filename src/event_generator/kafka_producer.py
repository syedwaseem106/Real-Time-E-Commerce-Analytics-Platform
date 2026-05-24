import json
import time
import sys
import signal
from kafka import KafkaProducer
from kafka.errors import KafkaError
from src.event_generator.generator import EcommerceEventGenerator
from src.utils.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC
from src.utils.logger import get_logger, log_pipeline_metric

logger = get_logger("kafka-producer")

class EcommerceKafkaProducer:
    """
    Kafka Event Publisher with production-style configurations:
    - Retries (acks='all')
    - Gzip compression
    - Batching & Linger optimizations
    - Graceful signal handling
    """
    def __init__(self, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, topic=KAFKA_TOPIC):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.running = True
        self.producer = self._create_producer()
        self.generator = EcommerceEventGenerator()
        
        # Setup signal listeners for clean container exits
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)

    def _create_producer(self):
        """Builds the producer, retrying connection on start if broker isn't fully ready."""
        retries = 5
        delay = 5
        for i in range(retries):
            try:
                logger.info(f"Connecting to Kafka brokers at: {self.bootstrap_servers} (Attempt {i+1}/{retries})")
                producer = KafkaProducer(
                    bootstrap_servers=self.bootstrap_servers,
                    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                    acks='all',              # Strongest delivery guarantee
                    retries=3,               # Retry transient broker errors
                    compression_type='gzip', # Compress batches
                    linger_ms=10,            # Batch message buffer window
                    batch_size=32768         # 32KB batch limit
                )
                logger.info("Kafka Producer initialized successfully.")
                return producer
            except Exception as e:
                logger.warning(f"Failed connecting to Kafka: {e}. Retrying in {delay} seconds...")
                time.sleep(delay)
                
        logger.critical("Could not establish connection to Kafka. Exiting...")
        sys.exit(1)

    def _handle_shutdown(self, signum, frame):
        """Interrupt callback to terminate loops cleanly."""
        logger.info(f"Received terminate signal ({signum}). Initiating graceful shutdown...")
        self.running = False

    def _on_success(self, record_metadata):
        """Callback on successful event delivery."""
        pass # Silenced in production to prevent spam, but active for tracking offsets
        
    def _on_error(self, exc):
        """Callback on delivery failure."""
        logger.error(f"Kafka delivery error occurred: {exc}")

    def start_streaming(self, events_per_second=5):
        """Streams events continuously into the Kafka topic."""
        logger.info(f"Starting e-commerce clickstream generation. Target rate: {events_per_second} events/sec")
        
        event_count = 0
        start_time = time.time()
        
        try:
            for event in self.generator.stream_events(events_per_second):
                if not self.running:
                    break
                    
                # Publish event asynchronously
                future = self.producer.send(self.topic, value=event)
                future.add_callback(self._on_success)
                future.add_errback(self._on_error)
                
                event_count += 1
                
                # Periodically log throughput metrics every 500 events
                if event_count % 500 == 0:
                    elapsed = time.time() - start_time
                    throughput = event_count / elapsed
                    log_pipeline_metric(
                        logger, 
                        pipeline_name="kafka_ingestion", 
                        step="stream_publishing", 
                        row_count=event_count,
                        duration_seconds=elapsed,
                        status="RUNNING"
                    )
                    logger.info(f"Generated {event_count} events total | Current throughput: {throughput:.2f} msg/sec")
                    
        except Exception as e:
            logger.error(f"Event streaming loop crashed: {e}")
        finally:
            self.close()

    def close(self):
        """Flushes buffered records and releases network connections."""
        logger.info("Flushing Kafka message buffers...")
        if self.producer:
            self.producer.flush()
            self.producer.close(timeout=10)
        logger.info("Kafka Producer connection closed cleanly. Exit.")

if __name__ == '__main__':
    # Default to 5 events per second for simulation stability
    producer = EcommerceKafkaProducer()
    producer.start_streaming(events_per_second=5)
