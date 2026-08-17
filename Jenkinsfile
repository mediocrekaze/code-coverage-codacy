@Library('demo@main') _

import org.jenkinsci.plugins.workflow.steps.FlowInterruptedException

def pr_workspace_label = "workspace"

def environment = [
  development: [ build: true, destroy: false, env: env_code == 'aws-com' ? 'aws-com' : 'aws-cnn' ]    
]

def pipeline_sample = {
  stage("checkout") {
    //checkout(scm)
  }

  stage("build") {
    parallel(
      'Europe': {
        stage('Deploy Europe') {
          retry(2) {
            echo "Deploying to Europe EKS..."
            echo "Europe deployment finished"
          }
        }
      },
      'China': {
        stage('Deploy China') {
          retry(2) {
            echo "Deploying to China EKS..."
            echo "China deployment finished"
          }
        }
      }
    )
  }
}

if(env.CHANGE_ID) {
  stage("stage env") {
    echo "hello there!"
    echo "PR Number : ${pullRequest.number}"
    echo "Draft     : ${pullRequest.draft}"
    if (pr_workspace_label in pullRequest.labels.collect { it }) {
        echo "PR label ${pr_workspace_label} available"
    }
    echo "branch name      : ${env.BRANCH_NAME}"
    echo "build number     : ${env.BUILD_NUMBER}"
    echo "job name         : ${env.JOB_NAME}"
    echo "workspace        : ${env.WORKSPACE}"
    echo "pr number        : ${env.CHANGE_ID}"
    echo "pr target branch : ${env.CHANGE_TARGET}"
    echo "environment code : ${ env_code }"
    echo "sample condition : ${ environment.development.env }"
    runMe(
      name: 'mediocre',
      environment: 'infrastructure'
    )
  }
  pipeline_sample()
}

if(env.CHANGE_ID) {
  runWithPod(cloud: 'demo', container: 'builder') {
    stage('pod test') {
      sh 'echo "Hello from Jenkins Kubernetes agent"'
      sh 'hostname'
      sh 'cat /etc/os-release'      
    }
    stage('pod build') {
      sh 'echo "running build"'
    }
  }
}
