pipeline {
    agent {
        label "master"
    }

    environment {
        X_AUTH_KEY = credentials('cloudflare-api-key')
        X_AUTH_EMAIL = credentials('admin-email')
        DDNS_PROFILE = "default"
        IMAGE_NAME = "haomingyin/script.ddns-cloudflare"
    }

    stages {
        stage("Deploy") {
            when {
                branch "master"
            }
            steps {
                script {
                    sh "docker pull ${env.IMAGE_NAME}:latest"
                    sh "docker kill ${env.IMAGE_NAME} || true"
                    sh "docker run -t --rm --name ${env.IMAGE_NAME} ${env.IMAGE_NAME}:latest"
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
