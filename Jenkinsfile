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
                echo "branch name     : ${env.BRANCH_NAME}"          // 
                echo "build number    : ${env.BUILD_NUMBER}"         // jenkins build number
                echo "job name        : ${env.JOB_NAME}"             // jenkins job name
                echo "workspace       : ${env.WORKSPACE}"            // jenkins workspace path location
                echo "pr number       : ${env.CHANGE_ID}"            // github pr number
                echo "pr target branch: ${env.CHANGE_TARGET}"        // github branch target for pr
            }
        }
        stage('build') {
            steps {
                script {
                  def pr_changed_files = pullRequest.files.collect { it.getFilename() }
                  pr_changed_files.each { file ->
                    echo file
                  }
                  echo "${pr_changed_files}"
                }
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
