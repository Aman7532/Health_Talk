import logging
import json
import requests
import datetime
import os
import traceback
from logging.handlers import RotatingFileHandler

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create a custom handler that sends logs to Elasticsearch
class ElasticsearchHandler(logging.Handler):
    def __init__(self, host, index_prefix="healthcare-chatbot"):
        super().__init__()
        self.host = host
        self.index_prefix = index_prefix
        
    def emit(self, record):
        try:
            # Format the log message
            log_entry = self.format(record)
            
            # Create the Elasticsearch index name with date
            today = datetime.datetime.now().strftime("%Y.%m.%d")
            index_name = f"{self.index_prefix}-{today}"
            
            # Prepare the log document
            doc = {
                "timestamp": datetime.datetime.now().isoformat(),
                "level": record.levelname,
                "message": record.getMessage(),
                "logger": record.name,
                "path": record.pathname,
                "function": record.funcName,
                "line_number": record.lineno
            }
            
            # Add exception info if available
            if record.exc_info:
                doc["exception"] = '\n'.join(traceback.format_exception(*record.exc_info))
            
            # Add any extra fields from the record
            if hasattr(record, 'user_id'):
                doc["user_id"] = record.user_id
                
            if hasattr(record, 'request_data'):
                doc["request_data"] = record.request_data
                
            if hasattr(record, 'response_data'):
                doc["response_data"] = record.response_data
                
            if hasattr(record, 'execution_time'):
                doc["execution_time"] = record.execution_time
            
            # Send the log to Elasticsearch
            url = f"{self.host}/{index_name}/_doc"
            response = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(doc),
                timeout=5
            )
            
            # Check if the request was successful
            if response.status_code not in (200, 201):
                print(f"Failed to send log to Elasticsearch: {response.text}")
        
        except Exception as e:
            print(f"Error sending log to Elasticsearch: {str(e)}")

def get_logger(name="healthcare-chatbot"):
    """
    Get a configured logger that sends logs to Elasticsearch and file
    
    Args:
        name (str): Name of the logger
        
    Returns:
        logging.Logger: Configured logger
    """
    # Get Elasticsearch host from environment or use default
    elasticsearch_host = os.environ.get("ELASTICSEARCH_HOST", "http://elasticsearch-service:9200")
    
    # Create a custom logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Clear existing handlers if any
    if logger.handlers:
        logger.handlers = []
    
    # Create and add the Elasticsearch handler
    es_handler = ElasticsearchHandler(elasticsearch_host)
    es_handler.setLevel(logging.INFO)
    logger.addHandler(es_handler)
    
    # Also log to file for backup
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, f"{name}.log"),
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    
    # Add console handler for development
    if os.environ.get("ENVIRONMENT", "development") == "development":
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)
    
    return logger

# Example usage
if __name__ == "__main__":
    logger = get_logger()
    logger.info("Test log message")
    
    try:
        # Simulate an error
        result = 10 / 0
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
