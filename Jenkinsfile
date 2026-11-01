pipeline {
    agent any
    triggers { githubPush() }

    stages {
        stage('Fetch Code') {
            steps { checkout scm }
        }
        stage('Check in Container') {
            steps {
                sh 'docker run --rm -v "$PWD":/app -w /app python:3.11-slim python -m py_compile app.py'
            }
        }
        stage('Build & Deploy') {
            steps {
                sh 'docker compose -p part2 down || true'
                sh 'docker compose -p part2 up -d'
            }
        }
        stage('Verify') {
            steps {
                retry(10) {
                    sleep 10
                    sh 'curl -fs http://localhost:5000 > /dev/null'
                }
            }
        }
    }

    post {
        always {
            script {
                def TEST_MODE = false   // set to false only at the very end
                def subj = "Build #${env.BUILD_NUMBER} - ${currentBuild.currentResult}"
                def body = "Job: ${env.JOB_NAME}\nResult: ${currentBuild.currentResult}\nLogs: ${env.BUILD_URL}console"
                if (TEST_MODE) {
                    emailext(subject: "[TEST] ${subj}", body: body, to: 'ashy19spawner10@gmail.com')
                } else {
                    emailext(subject: subj, body: body, recipientProviders: [developers(), requestor()])
                }
            }
        }
    }
}
