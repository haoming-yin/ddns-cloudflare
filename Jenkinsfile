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

    // triggers {
    //     cron('H H * * *')
    // }

    stages {
        stage("Build") {
            steps {
                script {
                    docker.withRegistry("https://index.docker.io/v1/", "docker-hub-credential") {
                        def image = docker.build("${env.IMAGE_NAME}:${env.BUILD_ID}")
                        image.push()
                        image.push('latest')
                    }
                }
                
            }
        }

        stage("Deploy") {
            steps {
                script {
                    sh "docker run -t --rm ${env.IMAGE_NAME}:latest"
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
