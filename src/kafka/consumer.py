import json
import os
import sys
import time
from kafka import KafkaConsumer
from src.utils.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, KAFKA_GROUP_ID
from src.utils.logger import get_logger

logger = get_logger("kafka-consumer-utility")

class EcommerceKafkaConsumer:
    """
    Standard consumer utility for testing, logging, and validating events 
    currently passing through Kafka topics.
    """
    def __init__(self, bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, topic=KAFKA_TOPIC, group_id=KAFKA_GROUP_ID):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.group_id = group_id
        self.consumer = self._create_consumer()

    def _create_consumer(self):
        """Attempts to establish connection with the Kafka broker."""
        retries = 3
        delay = 5
        for i in range(retries):
            try:
                logger.info(f"Connecting to Kafka brokers at: {self.bootstrap_servers} (Attempt {i+1}/{retries})")
                consumer = KafkaConsumer(
                    self.topic,
                    bootstrap_servers=self.bootstrap_servers,
                    group_id=self.group_id,
                    auto_offset_reset='earliest',
                    enable_auto_commit=True,
                    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
                )
                logger.info(f"Successfully subscribed to topic: {self.topic}")
                return consumer
            except Exception as e:
                logger.warning(f"Consumer connection failure: {e}. Retries in {delay} seconds...")
                time.sleep(delay)
        logger.error("Could not bind consumer to Kafka. Exiting...")
        return None

    def consume(self, max_messages=10, timeout_ms=5000):
        """Consumes a limited count of events from the topic."""
        if not self.consumer:
            logger.error("Consumer not connected.")
            return []

        logger.info(f"Beginning poll for messages (max: {max_messages}, timeout: {timeout_ms/1000}s)...")
        messages = []
        
        # We manually poll the consumer to avoid infinite blocking inside Airflow/automation tasks
        start_time = time.time()
        while len(messages) < max_messages:
            elapsed = (time.time() - start_time) * 1000
            if elapsed > timeout_ms:
                logger.info("Poll timeout reached.")
                break
                
            raw_poll = self.consumer.poll(timeout_ms=1000, max_records=max_messages - len(messages))
            for tp, records in raw_poll.items():
                for record in records:
                    messages.append(record.value)
                    
        logger.info(f"Consumed {len(messages)} events.")
        return messages

    def save_messages_to_json(self, output_path, count=50):
        """Utility function to grab sample stream data and write to local JSON files."""
        events = self.consume(max_messages=count, timeout_ms=10000)
        if not events:
            logger.warning("No events consumed to write.")
            return
            
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(events, f, indent=4)
            logger.info(f"Saved {len(events)} sample events to {output_path}")
        except Exception as e:
            logger.error(f"Error saving events: {e}")

    def close(self):
        """Disconnects consumer cleanly."""
        if self.consumer:
            self.consumer.close()
            logger.info("Kafka consumer shut down.")

if __name__ == '__main__':
    # Execution for simple debugging
    consumer = EcommerceKafkaConsumer()
    messages = consumer.consume(max_messages=5, timeout_ms=5000)
    for m in messages:
        print(json.dumps(m, indent=2))
    consumer.close()
