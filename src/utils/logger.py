import logging
import json
import os
import sys
from datetime import datetime

class JsonFormatter(logging.Formatter):
    """
    Custom formatter to output logs in structured JSON format.
    Extremely valuable for modern cloud logging platforms (Datadog, ELK, CloudWatch).
    """
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "line_no": record.lineno,
        }
        
        # Capture exceptions if they occur
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
            
        # Incorporate context dictionaries passed via 'extra'
        if hasattr(record, "pipeline_name"):
            log_record["pipeline_name"] = record.pipeline_name
        if hasattr(record, "step"):
            log_record["step"] = record.step
        if hasattr(record, "row_count"):
            log_record["row_count"] = record.row_count
            
        return json.dumps(log_record)

def get_logger(name="ecommerce-pipeline", log_level=logging.INFO):
    """
    Generates a structured logger equipped with stream and file outputs.
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers if logger is fetched multiple times
    if logger.handlers:
        return logger
        
    logger.setLevel(log_level)
    
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir)
        except Exception:
            pass # Suppress if running in restrictive docker environments
            
    # Stream Handler (stdout)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(log_level)
    
    # We use standard clean formatted output for local developer readability,
    # but could switch to JSON formatter when executing inside containers.
    if os.getenv("DOCKER_CONTAINER") == "true" or os.getenv("JSON_LOGS") == "true":
        stream_handler.setFormatter(JsonFormatter())
    else:
        standard_format = logging.Formatter(
            '[%(asctime)s] %(levelname)-8s [%(name)s:%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        stream_handler.setFormatter(standard_format)
        
    logger.addHandler(stream_handler)
    
    # Optional File Handler
    try:
        file_path = os.path.join(log_dir, f"{name}.log")
        file_handler = logging.FileHandler(file_path, encoding='utf-8')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(JsonFormatter())
        logger.addHandler(file_handler)
    except Exception:
        pass # Avoid crashing if write permission is restricted
        
    return logger

def log_pipeline_metric(logger, pipeline_name, step, row_count, duration_seconds=0.0, status="SUCCESS", error=None):
    """
    Observability pattern: logs structured data ingestion pipelines metrics.
    """
    extra_metrics = {
        "pipeline_name": pipeline_name,
        "step": step,
        "row_count": row_count,
        "duration_seconds": round(duration_seconds, 3),
        "status": status
    }
    
    log_msg = f"Pipeline {pipeline_name} | Step: {step} | Rows: {row_count} | Status: {status}"
    if error:
        log_msg += f" | Error: {str(error)}"
        logger.error(log_msg, extra=extra_metrics)
    else:
        logger.info(log_msg, extra=extra_metrics)
