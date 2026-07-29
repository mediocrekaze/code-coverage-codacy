pipeline {
    agent any
    stages {
        stage('Inspect PR') {
            steps {
                script {
                    if (!env.CHANGE_ID) {
                        echo "Not a Pull Request build."
                        return
                    }
                    echo "PR Number : ${pullRequest.number}"
                    echo "Draft     : ${pullRequest.draft}"

                    // Get label names
                    def labels = pullRequest.labels.collect { it.name }

                    echo "Labels    : ${labels.join(', ')}"

                    if (labels.contains("terraform")) {
                        echo "Terraform label detected."
                    }

                    if (labels.contains("skip-tests")) {
                        echo "Skipping tests."
                    }
                }
            }
        }
        stage('build') {
            steps {
                echo "building stage"
            }
        }
        stage('test') {
            steps {
                echo "testing stage"
            }
        }
        stage('deploy') {
            steps {
                retry(2) {
                     echo "deploying stage"
                }
            }
        }
    }
}
