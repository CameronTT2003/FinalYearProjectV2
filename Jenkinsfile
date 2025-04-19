pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                // Check out the repository as configured in the job
                checkout scm
            }
        }
        stage('Install Dependencies') {
            steps {
                // Upgrade pip and install dependencies from requirements.txt
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            when {
                // Only run tests if test files exist
                expression { fileExists('tests') }
            }
            steps {
                // Run tests using pytest
                bat 'pytest'
            }
        }
        stage('Deploy') {
            steps {
                // Deploy the app by running run.py. For production, consider using a WSGI server.
                bat 'python run.py'
            }
        }
    }
    post {
        success {
            echo 'Build and deployment succeeded!'
        }
        failure {
            echo 'Build or deployment failed!'
        }
    }
}