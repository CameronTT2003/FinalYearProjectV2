pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'python -m pip install -r requirements.txt'
            }
        }
        stage('Deploy') {
            steps {
                // Consider using a production WSGI server for production environments.
                bat 'python run.py'
            }
        }
    }
}