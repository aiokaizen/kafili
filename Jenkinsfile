pipeline {
    agent { 
        node {
            label 'docker-agent-alpine-django'
        }
    }
    triggers {
        pollSCM '*/3 * * * *'
    }
    stages {
        stage('Build') {
            steps {
                echo "Building.."
                sh '''
#!/bin/bash

. ~/.bashrc

echo "BUILD_ID=${BUILD_ID}" > build_info.txt
echo "BUILD_URL=${BUILD_URL}" >> build_info.txt

python -m venv venv
. venv/bin/activate
pip install --upgrade pip setuptools wheel cffi
pip install -r requirements.txt
                '''
            }
        }
        stage('Test') {
            steps {
                echo "Testing.."
                sh '''
python manage.py migrate
                '''
            }
        }
        stage('Deliver') {
            steps {
                echo 'Deliver....'
                sh '''
                echo "Delivery was successful."
                '''
            }
        }
    }
}
