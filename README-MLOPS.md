# Healthcare Chatbot MLOps Setup

This document provides instructions for deploying the Healthcare Chatbot using Docker, Kubernetes, and Ansible with an ELK stack for monitoring and logging.

## Project Structure

```
├── Dockerfile                # Container definition for the application
├── docker-compose.yml        # Local development setup with ELK stack
├── ansible-deploy.yml        # Ansible playbook for automated deployment
├── k8s/                      # Kubernetes manifests
│   ├── namespace.yaml        # Kubernetes namespace definition
│   ├── app-deployment.yaml   # Application deployment and service
│   ├── persistent-volumes.yaml # PVCs for application data
│   ├── secrets.yaml          # Kubernetes secrets for API keys
│   ├── elasticsearch-deployment.yaml # Elasticsearch StatefulSet
│   ├── logstash-deployment.yaml # Logstash deployment with ConfigMap
│   ├── kibana-deployment.yaml # Kibana deployment and service
│   ├── logstash-config/      # Logstash configuration files
│   │   ├── logstash.yml      # Logstash main configuration
│   │   └── logstash.conf     # Logstash pipeline configuration
```

## Local Development

To run the application locally with Docker Compose:

```bash
# Set your Google API key in .env file or export it
export GOOGLE_API_KEY=your_api_key_here

# Start the application and ELK stack
docker-compose up -d

# Access the application at http://localhost:3000
# Access Kibana at http://localhost:5601
```

## Kubernetes Deployment with Ansible

### Prerequisites

1. Kubernetes cluster with kubectl configured
2. Docker registry access
3. Ansible installed with kubernetes.core collection

```bash
# Install required Ansible collections
ansible-galaxy collection install kubernetes.core
```

### Deployment Steps

1. Update the variables in `ansible-deploy.yml`:
   - `docker_registry`: Your Docker registry URL
   - Set your Google API key as an environment variable

2. Run the Ansible playbook:

```bash
export GOOGLE_API_KEY=your_api_key_here
ansible-playbook ansible-deploy.yml
```

This will:
- Build and push the Docker image
- Create the Kubernetes namespace
- Deploy secrets, persistent volumes, and the ELK stack
- Deploy the application with proper configuration

### Accessing the Application

After deployment:
- Application: http://healthcare-chatbot.example.com
- Kibana dashboard: http://kibana.healthcare-chatbot.example.com

## Manual Kubernetes Deployment

If you prefer to deploy manually without Ansible:

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create secrets (update with your actual API key first)
kubectl apply -f k8s/secrets.yaml

# Deploy persistent volumes
kubectl apply -f k8s/persistent-volumes.yaml

# Deploy ELK stack
kubectl apply -f k8s/elasticsearch-deployment.yaml
kubectl apply -f k8s/logstash-deployment.yaml
kubectl apply -f k8s/kibana-deployment.yaml

# Deploy application (replace variables first)
envsubst < k8s/app-deployment.yaml | kubectl apply -f -
```

## Monitoring and Logging

The ELK stack provides comprehensive monitoring and logging:

- **Elasticsearch**: Stores logs and metrics
- **Logstash**: Processes and forwards logs from the application
- **Kibana**: Visualizes logs and metrics

Access Kibana to create dashboards for monitoring application health, performance metrics, and user interactions.

## Scaling

The Kubernetes deployment supports horizontal scaling:

```bash
kubectl scale deployment healthcare-chatbot -n healthcare-chatbot --replicas=3
```

## Troubleshooting

Check pod status:
```bash
kubectl get pods -n healthcare-chatbot
```

View application logs:
```bash
kubectl logs -f deployment/healthcare-chatbot -n healthcare-chatbot
```

Check ELK stack:
```bash
kubectl get pods -n healthcare-chatbot -l app=elasticsearch
kubectl get pods -n healthcare-chatbot -l app=logstash
kubectl get pods -n healthcare-chatbot -l app=kibana
```
