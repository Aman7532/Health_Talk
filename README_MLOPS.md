# Healthcare Chatbot MLOps Setup

This document describes the MLOps setup for the Healthcare Chatbot project.

## Project Structure

```
├── Jenkinsfile                  # CI/CD pipeline configuration
├── training/                    # Model training code
│   ├── Dockerfile               # Dockerfile for model training
│   ├── train_model.py           # Model training script (copied from train_extratrees.py)
│   └── test.py                  # Model testing script
├── healthcare_chatbot_backend/  # Backend application code
│   └── Dockerfile               # Dockerfile for backend application
├── healthcare_chatbot_frontend/ # Frontend application code
│   └── Dockerfile               # Dockerfile for frontend application
├── kubernetes/                  # Kubernetes manifests
│   ├── backend.yaml             # Backend deployment and service
│   ├── frontend.yaml            # Frontend deployment and service
│   ├── elasticsearch.yaml       # Elasticsearch deployment and service
│   ├── kibana.yaml              # Kibana deployment and service
│   └── logstash.yaml            # Logstash deployment, service, and config
└── ansible-deploy/              # Ansible deployment scripts
    ├── ansible-book.yml         # Ansible playbook
    └── inventory                # Ansible inventory
```

## CI/CD Pipeline

The CI/CD pipeline is defined in the Jenkinsfile and consists of the following stages:

1. **Checkout**: Clone the repository
2. **Test Model**: Run the model test script
3. **Train Model**: Build a Docker image for model training and push it to Docker Hub
4. **Build Docker Backend Image**: Build the backend Docker image and push it to Docker Hub
5. **Build Docker Frontend Image**: Build the frontend Docker image and push it to Docker Hub
6. **Deploy with Ansible**: Deploy the application to Kubernetes using Ansible

## Deployment

The application is deployed as a set of microservices on Kubernetes:

- **Frontend**: React application served on port 3000
- **Backend**: Flask application serving the chat and prediction API on port 3000
- **ELK Stack**: Elasticsearch, Logstash, and Kibana for logging and monitoring

## How to Use

### Prerequisites

- Docker and Docker Compose
- Kubernetes cluster (such as Minikube for local development)
- Jenkins server with appropriate plugins
- Ansible

### Local Development

1. Clone the repository
2. Build and run the Docker containers:

```bash
docker-compose up -d
```

### Jenkins Setup

1. Install required plugins:
   - Docker Pipeline
   - Ansible
   - Kubernetes

2. Configure credentials:
   - `SUDO_PASSWORD`: Sudo password for the deployment server
   - `DockerHubCred`: Docker Hub credentials

3. Create a Jenkins pipeline job using the Jenkinsfile from this repository

### Kubernetes Deployment

The application can be manually deployed to Kubernetes using:

```bash
kubectl apply -f kubernetes/
```

### Ansible Deployment

The application can be deployed using Ansible:

```bash
cd ansible-deploy
ansible-playbook -i inventory ansible-book.yml
```

## Monitoring

The ELK stack is set up for monitoring:

- Kibana UI is available on port 31601
- Logs are collected via Logstash on port 30044

## Continuous Integration

Each commit to the main branch triggers the Jenkins pipeline, which builds the Docker images, tests the model, and deploys the application to Kubernetes.

## Author

Aman Agarwal 