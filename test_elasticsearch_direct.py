import logging
import json
import requests
import datetime
import os
import sys
import socket
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("elasticsearch-test")

# Elasticsearch configuration
ELASTICSEARCH_HOST = os.environ.get("ELASTICSEARCH_HOST", "http://localhost:30001")
INDEX_NAME = f"healthcare-chatbot-test-{datetime.datetime.now().strftime('%Y.%m.%d')}"

def send_log_to_elasticsearch(log_data):
    """Send log data directly to Elasticsearch"""
    url = urljoin(ELASTICSEARCH_HOST, f"/{INDEX_NAME}/_doc")
    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(log_data)
        )
        if response.status_code >= 200 and response.status_code < 300:
            print(f"Successfully sent log to Elasticsearch: {response.json()}")
            return True
        else:
            print(f"Failed to send log to Elasticsearch: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Exception when sending log to Elasticsearch: {str(e)}")
        return False

def test_elasticsearch_connection():
    """Test connection to Elasticsearch"""
    try:
        response = requests.get(ELASTICSEARCH_HOST)
        if response.status_code == 200:
            print(f"Successfully connected to Elasticsearch at {ELASTICSEARCH_HOST}")
            return True
        else:
            print(f"Failed to connect to Elasticsearch: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Exception when connecting to Elasticsearch: {str(e)}")
        return False

def generate_test_log():
    """Generate a test log entry"""
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "level": "INFO",
        "message": "Test log message from direct Elasticsearch test",
        "logger": "test-logger",
        "hostname": socket.gethostname(),
        "application": "healthcare-chatbot",
        "environment": os.environ.get("ENVIRONMENT", "development"),
        "test_run": True
    }

def main():
    """Main function to test Elasticsearch logging"""
    print(f"Testing Elasticsearch connection to {ELASTICSEARCH_HOST}")
    
    # Test connection
    if not test_elasticsearch_connection():
        print("Failed to connect to Elasticsearch. Exiting.")
        sys.exit(1)
    
    # Send test log
    log_data = generate_test_log()
    if send_log_to_elasticsearch(log_data):
        print("Test log sent successfully to Elasticsearch")
    else:
        print("Failed to send test log to Elasticsearch")
        sys.exit(1)
    
    # Check if index exists
    try:
        url = urljoin(ELASTICSEARCH_HOST, f"/_cat/indices/{INDEX_NAME}?v")
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Index {INDEX_NAME} exists in Elasticsearch:")
            print(response.text)
        else:
            print(f"Failed to check if index {INDEX_NAME} exists: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Exception when checking index: {str(e)}")
    
    print("Elasticsearch direct logging test completed")

if __name__ == "__main__":
    main()
