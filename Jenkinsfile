pipeline {
    agent any
    stages {
        stage('Inspect PR') {
            steps {
                script {

                    def pr_workspace_label = "workspace"

                    if (!env.CHANGE_ID) {
                        echo "Not a Pull Request build."
                        return
                    }
                    echo "PR Number : ${pullRequest.number}"
                    echo "Draft     : ${pullRequest.draft}"
                    if (env.CHANGE_ID) {
                        if(pullRequest.draft) {
                            echo "i am draft"
                        }
                    }
                    if (pr_workspace_label in pullRequest.labels.collect {it}) {
                        echo "PR label ${pr_workspace_label } available"
                    }
                }
                echo "CHANGE_ID: ${env.CHANGE_ID}"
                echo "CHANGE_TARGET: ${env.CHANGE_TARGET}"
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
