node {

    stage('Inspect PR') {

        def pr_workspace_label = "workspace"

        if (!env.CHANGE_ID) {
            echo "Not a Pull Request build."
        } else {

            echo "PR Number : ${pullRequest.number}"
            echo "Draft     : ${pullRequest.draft}"

            if (pullRequest.draft) {
                echo "I am draft"
            }

            if (pr_workspace_label in pullRequest.labels.collect { it }) {
                echo "PR label ${pr_workspace_label} available"
            }

            echo "branch name     : ${env.BRANCH_NAME}"
            echo "build number    : ${env.BUILD_NUMBER}"
            echo "job name        : ${env.JOB_NAME}"
            echo "workspace       : ${env.WORKSPACE}"
            echo "pr number       : ${env.CHANGE_ID}"
            echo "pr target branch: ${env.CHANGE_TARGET}"
        }
    }


    stage('Build') {

        def pr_changed_files =
            pullRequest.files.collect { it.getFilename() }

        pr_changed_files.each { file ->
            echo file
        }

        echo "${pr_changed_files}"
    }


    stage('Test') {
        echo "testing stage"
    }


    stage('Deploy') {

        parallel(

            'Europe': {

                stage('Deploy Europe') {

                    retry(2) {
                        echo "Deploying to Europe EKS..."
                        sleep 5
                        echo "Europe deployment finished"
                    }
                }
            },


            'China': {

                stage('Deploy China') {

                    retry(2) {
                        echo "Deploying to China EKS..."
                        sleep 5
                        echo "China deployment finished"
                    }
                }
            }
        )
    }
}