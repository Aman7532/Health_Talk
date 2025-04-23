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
                sh 'python3 test_model.py'
            }
        }

        stage('Train Model') {
            steps {
                script {
                    dir('training') {
                        // Copy the training script and data
                        sh 'cp ../train_extratrees.py train_model.py'
                        sh 'cp -r ../data .'
                        
                        def trainImage = docker.build("${DOCKER_USERNAME}/train-model:latest", '-f Dockerfile .')
                        withDockerRegistry([credentialsId: "DockerHubCred", url: ""]) {
                            trainImage.push("${env.BUILD_NUMBER}")
                            trainImage.push("latest")
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
                        sh 'cp ../chatpdf1.py .'
                        sh 'cp ../data.pth .'
                        sh 'cp ../ExtraTrees .'
                        sh 'cp -r ../src .'
                        sh 'cp -r ../templates .'
                        sh 'cp -r ../static .'
                        sh 'cp ../intents.json .'
                        sh 'cp ../.env .'
                        sh 'cp ../requirement.txt requirements.txt'
                        sh 'cp -r ../data .'
                        
                        backendImage = docker.build("${DOCKER_USERNAME}/flask-app:backend-${env.BUILD_NUMBER}")
                        backendImage.push()
                        backendImage.push("latest")
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
                        sh 'mkdir -p public'
                        sh 'cp -r ../static/* public/'
                        sh 'cp -r ../templates/* public/'

                        // Create a simple package.json file
                        sh '''
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
                        
                        frontendImage = docker.build("${DOCKER_USERNAME}/react-app:frontend-${env.BUILD_NUMBER}")
                        withDockerRegistry([credentialsId: "DockerHubCred", url: ""]) {
                            frontendImage.push()
                            frontendImage.push("latest")
                        }
                    }
                }
            }
        }

        stage('Deploy with Ansible') {
            steps {
                script {
                    withEnv(["SUDO_PASSWORD=${SUDO_PASSWORD}"]) {
                        ansiblePlaybook becomeUser: null, 
                                        colorized: true, 
                                        disableHostKeyChecking: true, 
                                        installation: 'Ansible', 
                                        inventory: './ansible-deploy/inventory', 
                                        playbook: './ansible-deploy/ansible-book.yml', 
                                        sudoUser: null,
                                        extraVars: [ansible_become_pass: SUDO_PASSWORD]
                    }
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