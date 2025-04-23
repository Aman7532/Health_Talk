#!/bin/bash

# Setup MLOps project structure for Healthcare Chatbot
echo "Setting up MLOps project structure..."

# Create directories if they don't exist
mkdir -p training
mkdir -p healthcare_chatbot_backend
mkdir -p healthcare_chatbot_frontend
mkdir -p kubernetes
mkdir -p ansible-deploy

# Setup backend
echo "Setting up backend..."
cp chatpdf1.py healthcare_chatbot_backend/
cp data.pth healthcare_chatbot_backend/
cp ExtraTrees healthcare_chatbot_backend/
cp -r src healthcare_chatbot_backend/
cp -r templates healthcare_chatbot_backend/
cp -r static healthcare_chatbot_backend/
cp intents.json healthcare_chatbot_backend/
cp .env healthcare_chatbot_backend/
cp requirement.txt healthcare_chatbot_backend/requirements.txt
cp -r data healthcare_chatbot_backend/

# Setup frontend
echo "Setting up frontend..."
mkdir -p healthcare_chatbot_frontend/public
cp -r static/* healthcare_chatbot_frontend/public/
cp -r templates/* healthcare_chatbot_frontend/public/

# Setup training
echo "Setting up training..."
cp train_extratrees.py training/train_model.py
cp -r data training/

echo "MLOps structure setup complete!"
echo "You can now build and run the project using Docker Compose:"
echo "docker-compose up -d" 