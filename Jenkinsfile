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

        stage("Sync Records") {
            when {
                branch "master"
            }
            steps {
                sh "inv cf.sync --profile=default"
            }
        }
    }
 
    post {
        always {
            cleanWs()
        }
    }
}
