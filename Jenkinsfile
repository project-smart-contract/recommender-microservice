pipeline {
    agent any
    environment {
        IMAGE_NAME = 'recommender-microservice'
        CONTAINER_NAME = 'recommender-microservice-container'
        DOCKERHUB_CREDENTIALS = credentials('dockerhub_amina')
    }
    stages {
        stage('Install dependencies') {
            steps {
                script {
                    echo 'Installing dependencies...'
                    sh 'pip install -r requirements.txt'
                }
            }
        }
        stage('Dockerize') {
            steps {
                script {
                    echo 'Dockerizing...'
                    sh "docker build -t aminabakkali/${IMAGE_NAME} ."
                }
            }
        }
        stage('Login + Push') {
            steps {
                echo 'Login...'
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                echo 'Pushing...'
                sh "docker push aminabakkali/${IMAGE_NAME}"
            }
        }
    }
}
