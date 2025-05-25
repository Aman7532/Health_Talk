import logging
import json
import requests
from datetime import datetime

class LogstashHandler(logging.Handler):
    """
    Custom logging handler that sends logs to Logstash via HTTP.
    """
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.url = f"http://{host}:{port}"
    
    def emit(self, record):
        try:
            # Format the log message
            log_entry = {
                "@timestamp": datetime.utcnow().isoformat(),
                "message": self.format(record),
                "level": record.levelname,
                "logger_name": record.name,
                "path": record.pathname,
                "line_number": record.lineno,
                "function": record.funcName,
                "type": "python",
                "app": "healthcare-chatbot"
            }
            
            # Add any extra fields from the record
            for key, value in record.__dict__.items():
                if key.startswith('_') or key in log_entry:
                    continue
                log_entry[key] = value
            
            # Send the log entry to Logstash
            response = requests.post(self.url, json=log_entry, timeout=5)
            if response.status_code != 200:
                print(f"Failed to send log to Logstash. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error sending log to Logstash: {e}")
