import logging
import json
import requests
import datetime
import os
from logging.handlers import RotatingFileHandler

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create a custom logger
logger = logging.getLogger('healthcare-chatbot')

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
                import traceback
                doc["exception"] = '\n'.join(traceback.format_exception(*record.exc_info))
            
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

# Get Elasticsearch host from environment or use default
elasticsearch_host = os.environ.get("ELASTICSEARCH_HOST", "http://localhost:30001")

# Create and add the Elasticsearch handler
es_handler = ElasticsearchHandler(elasticsearch_host)
es_handler.setLevel(logging.INFO)
logger.addHandler(es_handler)

# Also log to file for backup
file_handler = RotatingFileHandler(
    "healthcare-chatbot.log",
    maxBytes=10485760,  # 10MB
    backupCount=5
)
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)

# Test logging
def test_logging():
    logger.info("Starting Healthcare Chatbot application")
    logger.debug("This is a debug message")
    
    try:
        # Simulate an error
        result = 10 / 0
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
    
    logger.info("Processing user request: 'What are the symptoms of diabetes?'")
    logger.info("Generated response about diabetes symptoms")
    logger.warning("API rate limit approaching")

if __name__ == "__main__":
    test_logging()
    print("Logs sent to Elasticsearch successfully!")
