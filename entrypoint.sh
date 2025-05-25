#!/bin/bash
set -e

# Create models directory if it doesn't exist
mkdir -p /app/models

# Copy ExtraTrees file to models directory if it exists and models directory is empty
if [ -f /app/ExtraTrees ] && [ ! -f /app/models/ExtraTrees ]; then
    echo "Copying ExtraTrees file to models directory..."
    cp /app/ExtraTrees /app/models/
fi

# Start the application
exec python /app/chatpdf1.py
