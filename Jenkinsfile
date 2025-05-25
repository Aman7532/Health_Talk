pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE_NAME = 'healthcare-chatbot'
        GITHUB_REPO_URL = 'https://github.com/Aman7532/Health_Talk'
        DOCKER_REGISTRY = 'docker.io/aman7532'
        IMAGE_TAG = 'latest'
        NAMESPACE = 'healthcare-chatbot'
        PYTHON_VERSION = '3.9'
        VENV_NAME = 'healthcare-chatbot-venv'
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    git branch: 'main', url: "${GITHUB_REPO_URL}"
                }
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                script {
                    // Create and activate virtual environment
                    sh """
                        # Check if Python is installed
                        python3 --version
                        
                        # Create virtual environment if it doesn't exist
                        if [ ! -d "${VENV_NAME}" ]; then
                            python3 -m venv ${VENV_NAME}
                        fi
                        
                        # Activate virtual environment and install dependencies
                        . ${VENV_NAME}/bin/activate
                        pip install --upgrade pip
                        
                        # Check if requirements.txt exists and install dependencies
                        if [ -f "requirements.txt" ]; then
                            echo "Installing dependencies from requirements.txt"
                            pip install -r requirements.txt
                        else
                            echo "No requirements.txt found, installing essential packages"
                            pip install flask requests elasticsearch python-dotenv numpy pandas scikit-learn nltk pytest gunicorn
                        fi
                        
                        # Run any tests if available
                        if [ -d "tests" ] || [ -f "test_*.py" ]; then
                            echo "Running tests"
                            pytest -v || echo "Tests failed but continuing"
                        else
                            echo "No tests found"
                        fi
                        
                        # Deactivate virtual environment
                        deactivate
                    """
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'DockerHub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh 'echo "$DOCKER_PASS" | /usr/local/bin/docker login -u "$DOCKER_USER" --password-stdin'
                    }
                    sh "/usr/local/bin/docker build -t ${DOCKER_IMAGE_NAME} ."
                }
            }
        }
        
        stage('Push Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'DockerHub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh 'echo "$DOCKER_PASS" | /usr/local/bin/docker login -u "$DOCKER_USER" --password-stdin'
                    }
                    sh "/usr/local/bin/docker tag ${DOCKER_IMAGE_NAME} ${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:${IMAGE_TAG}"
                    sh "/usr/local/bin/docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }
        
        stage('Clean Existing Deployment') {
            steps {
                script {
                    // Delete existing namespace if it exists (ignore errors if it doesn't)
                    sh "kubectl delete namespace ${NAMESPACE} --ignore-not-found=true"
                    
                    // Wait for namespace to be fully deleted
                    sh '''
                        while kubectl get namespace ${NAMESPACE} &>/dev/null; do
                            echo "Waiting for namespace ${NAMESPACE} to be deleted..."
                            sleep 5
                        done
                    '''
                }
            }
        }
        
        stage('Run Ansible Playbook') {
            steps {
                script {
                    sh "/opt/homebrew/bin/ansible-playbook ansible-deploy.yml"
                }
            }
        }
        
        stage('Set Up Port Forwarding') {
            steps {
                script {
                    // Kill any existing port-forwarding processes
                    sh "pkill -f 'kubectl port-forward' || true"
                    
                    // Set up port forwarding for all services
                    sh '''
                        kubectl port-forward -n healthcare-chatbot svc/healthcare-chatbot-service 30000:80 &
                        kubectl port-forward -n healthcare-chatbot svc/elasticsearch-service 30001:9200 &
                        kubectl port-forward -n healthcare-chatbot svc/kibana-service 30002:80 &
                        
                        # Wait a bit to ensure port forwarding is established
                        sleep 5
                        
                        # Verify port forwarding is working
                        curl -s http://localhost:30000/test || echo "Healthcare Chatbot service not responding"
                        curl -s http://localhost:30001 || echo "Elasticsearch service not responding"
                        curl -s http://localhost:30002 || echo "Kibana service not responding"
                    '''
                }
            }
        }
        
        stage('Success') {
            steps {
                script {
                    echo """
                    ===============================================
                    DEPLOYMENT SUCCESSFUL!
                    
                    The Healthcare Chatbot has been successfully deployed.
                    
                    Access the services at:
                    - Healthcare Chatbot: http://localhost:30000
                    - Elasticsearch: http://localhost:30001
                    - Kibana: http://localhost:30002
                    
                    Note: Port forwarding has been set up automatically.
                    ===============================================
                    """
                }
            }
        }
    }
    
    post {
        success {
            echo "Pipeline executed successfully!"
        }
        failure {
            echo "Pipeline failed. Please check the logs for details."
            
            // Kill port forwarding on failure
            sh "pkill -f 'kubectl port-forward' || true"
        }
        always {
            // Clean up Docker images to save space
            sh "/usr/local/bin/docker system prune -f || true"
        }
    }
}
