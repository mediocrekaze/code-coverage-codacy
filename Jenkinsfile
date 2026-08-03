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
                echo "branch name     : ${env.BRANCH_NAME}"
                echo "build number    : ${env.BUILD_NUMBER}"
                echo "job name        : ${env.JOB_NAME}"
                echo "workspace       : ${env.WORKSPACE}"
                echo "pr number       : ${env.CHANGE_ID}"
                echo "pr target branch: ${env.CHANGE_TARGET}"
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
