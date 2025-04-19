pipeline {
    agent any
    environment {
        // Optional: Add environment variables if needed
        // e.g., SECRET_KEY = credentials('secret_key')
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                // Make sure you have tests and pytest installed
                bat 'pytest'
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