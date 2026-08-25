@Library('demo@main') _

import org.jenkinsci.plugins.workflow.steps.FlowInterruptedException


def environment_cnn1 = [
  "ENV_CODE=cnn1",
  "AWS_CODE=aws-cnn"
]

def environment_euc1 = [
  "ENV_CODE=euc1",
  "AWS_CODE=aws-com"
]


def pr_workspace_label = "workspace"

def cloud = ""

def environment = [
  pr:         [ build: true, destroy: false, env: env_code == 'aws-com' ? 'aws-com' : 'aws-cnn' ],
  'codacy-dev': [ transition: 'codacy-stg', build: true, destroy: false, merge: false, merge_args: [], env: env_code == 'aws-com' ? 'aws-com' : 'aws-cnn' ],
  'codacy-stg': [ transition: 'codacy-svc', build: true, destroy: false, merge: false, merge_args: [], env: env_code == 'aws-com' ? 'aws-com' : 'aws-cnn' ],
  'codacy-svc': [ transition: 'codacy-dem', build: true, destroy: false,  merge: false, merge_args: [], env: env_code == 'aws-com' ? 'aws-com' : 'aws-cnn' ],
  'codacy-dem': [ transition: 'main', build: true, destroy: false, env:  merge: true, merge_args: ['-X ours'], env_code == 'aws-com' ? 'aws-com' : 'aws-cnn' ],
  main:       [ transition: 'codacy-dev', build: true, destroy: false,  merge: true, merge_args: ['-X theirs'], env: env_code == 'aws-com' ? 'aws-com' : 'aws-cnn' ]
]

def node_config = [
  podConfig : [
    name: 'demo-pod',
    image: '487835535578.dkr.ecr.ap-southeast-1.amazonaws.com/build-image:latest'
  ]
]

Closure pipeline_sample = { config ->
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
              withEnv(environment) {
                echo "ENV_CODE = ${env.ENV_CODE}"
                echo "AWS_CODE = ${env.AWS_CODE}"
              }
              echo " name: ${sub_job.name}, ${sub_job.description}"
            }
          }
        }
        parallel job_dict
      }
      else {
        def stage_name = job.name
        stage(stage_name) {
          echo " name: ${job.name}, ${job.description}"
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

def stage_phase = [
  [ name: 'configuration', description: 'i am configuration' ],
  [ name: 'dependencies', description: 'i am dependencies' ],
  [
    [ name: 'workspace1', description: 'i am workspace one' ],
    [ name: 'workspace2', description: 'i am workspace two' ],
    [ name: 'workspace3', description: 'i am workspace three' ],
  ],
  [ name: 'build', description: 'i am build' ],
  [ name: 'deployment', description: 'i am deployment' ]
]

if(env.CHANGE_ID) {
  parallel(
    'aws-com': {    
      def environment = environment_euc1 
      runWithPod(pipeline_sample, node_config + [stage_phase: stage_phase, cloud: 'aws-com']) 
    },
    'aws-cnn': {
      def environment = environment_cnn1 
      runWithPod(pipeline_sample, node_config + [stage_phase: stage_phase, cloud: 'aws-cnn']) 
    }
  )
}
