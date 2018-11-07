pipeline {
    agent {
        label "master-docker"
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
    }
 
    post {
        always {
            cleanWs()
        }
    }
}
