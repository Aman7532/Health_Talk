pipeline {
    agent any

    environment {
        // Retrieve credentials from Jenkins
        SUDO_PASSWORD = credentials('SUDO_PASSWORD')
        DOCKER_HUB_CREDENTIALS = credentials('DockerHubCred')
        DOCKER_USERNAME = "aman7532"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Aman7532/Health_Talk.git'
            }
        }

        stage('Test Model') {
            steps {
                sh '''
                    # Install required packages
                    pip3 install --user numpy scikit-learn pandas
                    
                    # Check where the model file is located
                    echo "Current directory: $(pwd)"
                    echo "Listing files:"
                    ls -la
                    
                    # If the model is missing in the root, try to find it elsewhere
                    if [ ! -f "ExtraTrees" ]; then
                        echo "ExtraTrees not found in root, searching in other locations..."
                        find . -name "ExtraTrees" | xargs -I{} cp {} ./
                    fi
                    
                    # Run the test
                    python3 test_model.py
                '''
            }
        }

        stage('Train Model') {
            steps {
                script {
                    dir('training') {
                        // First check if the model already exists to avoid unnecessary training
                        sh '''
                            if [ -f "../ExtraTrees" ]; then
                                echo "ExtraTrees model already exists, skipping training"
                                mkdir -p data
                                cp -r ../data/* data/ || true
                                cp ../train_extratrees.py train_model.py || true
                            else
                                echo "ExtraTrees model not found, will train a new model"
                                # Copy the training script and data
                                cp ../train_extratrees.py train_model.py || true
                                cp -r ../data . || true
                            fi
                        '''
                        
                        sh "/usr/local/bin/docker build -t ${DOCKER_USERNAME}/train-model:latest -f Dockerfile ."
                        withCredentials([usernamePassword(credentialsId: "DockerHubCred", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                            sh 'echo "$DOCKER_PASS" | /usr/local/bin/docker login -u "$DOCKER_USER" --password-stdin'
                            sh "/usr/local/bin/docker push ${DOCKER_USERNAME}/train-model:latest"
                        }
                    }
                }
            }
        }

        stage('Build Docker Backend Image') {
            steps {
                dir('healthcare_chatbot_backend') {
                    script {
                        // Copy necessary files to the backend directory
                        sh '''
                            cp ../chatpdf1.py .
                            cp ../data.pth .
                            cp ../ExtraTrees .
                            cp -r ../src .
                            cp -r ../templates .
                            cp -r ../static .
                            cp ../intents.json .
                            cp ../.env .
                            cp ../requirement.txt requirements.txt || true
                            cp -r ../data .
                        '''
                        
                        sh "/usr/local/bin/docker build -t ${DOCKER_USERNAME}/flask-app:latest ."
                        withCredentials([usernamePassword(credentialsId: "DockerHubCred", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                            sh 'echo "$DOCKER_PASS" | /usr/local/bin/docker login -u "$DOCKER_USER" --password-stdin'
                            sh "/usr/local/bin/docker push ${DOCKER_USERNAME}/flask-app:latest"
                        }
                    }
                }
            }
        }

        stage('Build Docker Frontend Image') {
            steps {
                dir('healthcare_chatbot_frontend') {
                    // For now, we'll just use the static files as a simple frontend
                    // Later this can be expanded to a full React app if needed
                    script {
                        sh '''
                            mkdir -p public
                            cp -r ../static/* public/ || true
                            cp -r ../templates/* public/ || true

                            # Create a simple package.json file
                            cat > package.json << 'EOF'
{
  "name": "healthcare-chatbot-frontend",
  "version": "1.0.0",
  "description": "Frontend for Healthcare Chatbot",
  "main": "index.js",
  "scripts": {
    "start": "serve -s public -l 3000"
  },
  "dependencies": {
    "serve": "^14.0.0"
  }
}
EOF
                        '''
                        
                        sh "/usr/local/bin/docker build -t ${DOCKER_USERNAME}/react-app:latest ."
                        withCredentials([usernamePassword(credentialsId: "DockerHubCred", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                            sh 'echo "$DOCKER_PASS" | /usr/local/bin/docker login -u "$DOCKER_USER" --password-stdin'
                            sh "/usr/local/bin/docker push ${DOCKER_USERNAME}/react-app:latest"
                        }
                    }
                }
            }
        }

        stage('Deploy with Ansible') {
            steps {
                script {
                    sh "/opt/homebrew/bin/ansible-playbook -i ./ansible-deploy/inventory ./ansible-deploy/ansible-book.yml"
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
} 