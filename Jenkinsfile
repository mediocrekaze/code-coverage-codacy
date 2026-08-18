@Library('demo@main') _

import org.jenkinsci.plugins.workflow.steps.FlowInterruptedException

def pr_workspace_label = "workspace"

def environment = [
  development: [ build: true, destroy: false, env: env_code == 'aws-com' ? 'aws-com' : 'aws-cnn' ]    
]

node_config = [
  podConfig : [
    cloud: 'demo',
    name: 'demo-pod',
    image: '487835535578.dkr.ecr.ap-southeast-1.amazonaws.com/build-image:latest'
  ]
]

stage_phase = [
  [ name: 'config', description: 'i am config' ],
  [ name: 'dependencies', description: 'i am dependencies' ],
  [
    [ name: 'workspace1', description: 'i am workspace one' ],
    [ name: 'workspace2', description: 'i am workspace two' ],
    [ name: 'workspace3', description: 'i am workspace three' ],
  ],
  [ name: 'build', description: 'i am build' ],
  [ name: 'build', description: 'i am deployment' ]
]


def pipeline_sample = {
  stage("checkout") {
    checkout(scm)
  }
  try {
    config.stage_phase.each { job ->
      if(job instanceof ArrayList) {
        job_dict = [:]
        job.each { sub_job ->
          job_dict[sub_job.name] = {
            def stage_name = sub_job.name
            stage(stage_name) {
              echo " name: ${sub_job.name}, ${sub_job.description}"
            }
          }
        }
        parallel job_dict
      }
      else {
        def stage_name = stage_phase.name
        stage(stage_name) {
          echo " name: ${sub_job.name}, ${sub_job.description}"
        }
      }
    }
  }
  catch(e) {
    stage("sleep phase") {
      echo "i am sleeping"
    }
    throw e
  }
  finally {
    stage("exit") {
      echo "i will now exit"
    }
  }
  //stage("build") {
  //  parallel(
  //    'Europe': {
  //      stage('Deploy Europe') {
  //        retry(2) {
  //          echo "Deploying to Europe EKS..."
  //          echo "Europe deployment finished"
  //        }
  //      }
  //    },
  //    'China': {
  //      stage('Deploy China') {
  //        retry(2) {
  //          echo "Deploying to China EKS..."
  //          echo "China deployment finished"
  //        }
  //      }
  //    }
  //  )
  //}
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
}

if(env.CHANGE_ID) {
  runWithPod(pipeline_sample, node_config) 
}
