pipeline {
    agent {
        label "master-docker"
    }

    environment {
        X_AUTH_KEY = credentials('cloudflare-api-key')
        X_AUTH_EMAIL = credentials('admin-email')
    }

    triggers {
        cron('H H * * *')
    }

    stages {
        stage("Install Dependencies") {
            steps {
                sh "pip install -r requirements.txt"
            }
        }

        stage("Linting") {
            steps {
                sh "inv lint"
            }
        }

        stage("Unit Test") {
            steps {
                sh "inv test"
            }
        }

        stage("Sync Records") {
            steps {
                sh "inv cf.sync"
            }
        }
    }
 
    post {
        always {
            cleanWs()
        }
    }
}
