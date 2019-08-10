def proceed = true

pipeline {
    agent {
        label "master"
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
    }

    environment {
        X_AUTH_KEY = credentials('cloudflare-api-key')
        X_AUTH_EMAIL = credentials('admin-email')
        DDNS_PROFILE = "default"
        IMAGE_NAME = "haomingyin/script.ddns-cloudflare"
    }

    stages {
        stage("Input") {
            steps {
                script {
                    timeout(time: 10, unit: 'MINUTES') {
                        proceed = input(message: 'Has Travis finished building docker image?', 
                        ok: 'Confirm', 
                        parameters: [booleanParam(defaultValue: true, description: 'Select YES to proceed deployment.', name: 'YES')])
                    }
                }
            }
        }
        stage("Deploy") {
            when {
                branch "master"
                expression { proceed == true }
            }
            steps {
                script {
                    sh "docker pull ${env.IMAGE_NAME}:latest"
                    sh "docker kill script.ddns-cloudflare || true"
                    sh "docker run --rm -d -e X_AUTH_KEY=${env.X_AUTH_KEY}  -e X_AUTH_EMAIL=${env.X_AUTH_EMAIL} -e DDNS_PROFILE=${env.DDNS_PROFILE} --name script.ddns-cloudflare ${env.IMAGE_NAME}:latest"
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
