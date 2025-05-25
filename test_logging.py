import json
import logging
import requests
import time
import socket
import os
import random
from datetime import datetime, timedelta

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('healthcare-chatbot')

# Function to send logs directly to Elasticsearch via HTTP
def send_log_to_elasticsearch(message, level="INFO", log_type="python", timestamp=None, metadata=None):
    # Get the Elasticsearch service URL
    elasticsearch_url = os.environ.get("ELASTICSEARCH_HOST", "http://localhost:30001")
    index_name = f"healthcare-chatbot-logs-{datetime.now().strftime('%Y.%m.%d')}"
    
    # Create a log entry
    log_entry = {
        "@timestamp": timestamp or datetime.utcnow().isoformat(),
        "message": message,
        "level": level,
        "type": log_type,
        "app": "healthcare-chatbot",
        "hostname": socket.gethostname(),
        "environment": os.environ.get("ENVIRONMENT", "development"),
        "service_name": "healthcare-chatbot",
        "component_name": "api"
    }
    
    # Add any additional metadata
    if metadata:
        log_entry.update(metadata)
    
    try:
        # Send the log entry to Elasticsearch
        url = f"{elasticsearch_url}/{index_name}/_doc"
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json=log_entry
        )
        print(f"Log sent to Elasticsearch. Response: {response.status_code} - {response.text}")
        return response.status_code
    except Exception as e:
        print(f"Error sending log to Elasticsearch: {e}")
        return None

# Sample healthcare chatbot log messages
HEALTHCARE_INFO_MESSAGES = [
    "User query processed successfully",
    "Retrieved medical information for query about diabetes",
    "Symptom analysis completed",
    "Medical document retrieval successful",
    "User authentication successful",
    "Chat session started",
    "Response generated successfully",
    "Retrieved 5 relevant medical documents",
    "Processed user query about COVID-19 symptoms",
    "Successfully loaded medical knowledge base"
]

HEALTHCARE_WARNING_MESSAGES = [
    "Slow response time detected",
    "Limited matches found for user query",
    "Medical term not found in knowledge base",
    "High server load detected",
    "User session timeout warning",
    "Low confidence in medical response",
    "Multiple potential matches for symptom description",
    "Knowledge base update needed",
    "Rate limiting applied to API requests"
]

HEALTHCARE_ERROR_MESSAGES = [
    "Failed to retrieve medical information",
    "Database connection error",
    "Error processing user query",
    "Medical document retrieval failed",
    "API rate limit exceeded",
    "Error in symptom analysis",
    "Knowledge base access error",
    "User authentication failed",
    "Invalid input format detected",
    "Error generating response"
]

# Generate realistic healthcare chatbot logs
def generate_healthcare_logs(num_logs=20, time_span_hours=2):
    print(f"Generating {num_logs} healthcare chatbot logs spanning {time_span_hours} hours...")
    
    # Generate logs with timestamps spanning the specified time period
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=time_span_hours)
    
    log_levels = ["INFO", "WARNING", "ERROR"]
    log_weights = [0.7, 0.2, 0.1]  # 70% INFO, 20% WARNING, 10% ERROR
    
    for i in range(num_logs):
        # Generate a random timestamp within the time span
        log_time = start_time + timedelta(seconds=random.randint(0, time_span_hours * 3600))
        timestamp = log_time.isoformat()
        
        # Select log level based on weights
        level = random.choices(log_levels, weights=log_weights)[0]
        
        # Select appropriate message based on log level
        if level == "INFO":
            message = random.choice(HEALTHCARE_INFO_MESSAGES)
            metadata = {
                "user_id": f"user_{random.randint(1000, 9999)}",
                "session_id": f"session_{random.randint(10000, 99999)}",
                "response_time_ms": random.randint(50, 500),
                "query_type": random.choice(["symptom", "disease", "medication", "treatment", "general"])
            }
        elif level == "WARNING":
            message = random.choice(HEALTHCARE_WARNING_MESSAGES)
            metadata = {
                "user_id": f"user_{random.randint(1000, 9999)}",
                "session_id": f"session_{random.randint(10000, 99999)}",
                "response_time_ms": random.randint(500, 2000),
                "warning_type": random.choice(["performance", "data", "system", "user"])
            }
        else:  # ERROR
            message = random.choice(HEALTHCARE_ERROR_MESSAGES)
            metadata = {
                "user_id": f"user_{random.randint(1000, 9999)}",
                "session_id": f"session_{random.randint(10000, 99999)}",
                "error_code": random.randint(400, 599),
                "error_type": random.choice(["database", "api", "processing", "authentication", "input"])
            }
        
        # Send log to Elasticsearch
        send_log_to_elasticsearch(message, level, "healthcare-chatbot", timestamp, metadata)
        
        # Small delay to avoid overwhelming Elasticsearch
        time.sleep(0.2)
    
    print(f"Successfully generated {num_logs} healthcare chatbot logs")

# Function to check if Elasticsearch is running
def check_elasticsearch():
    elasticsearch_url = os.environ.get("ELASTICSEARCH_HOST", "http://localhost:30001")
    try:
        response = requests.get(elasticsearch_url)
        if response.status_code == 200:
            print(f"Successfully connected to Elasticsearch at {elasticsearch_url}")
            return True
        else:
            print(f"Failed to connect to Elasticsearch: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Error connecting to Elasticsearch: {e}")
        return False

if __name__ == "__main__":
    print("Testing Healthcare Chatbot Elasticsearch logging...")
    if check_elasticsearch():
        # Generate realistic healthcare chatbot logs
        generate_healthcare_logs(num_logs=30, time_span_hours=4)
    else:
        print("Elasticsearch connectivity check failed. Exiting.")
    print("Test completed.")