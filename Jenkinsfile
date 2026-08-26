@Library('demo@main') _

import org.jenkinsci.plugins.workflow.steps.FlowInterruptedException


def environment_euc1 = [
  "env_code=euc1",
  "aws_code=aws-com"
]

def environment_cnn1 = [
  "env_code=cnn1",
  "aws_code=aws-cnn"
]

def cloud = ""
def node_config = [
  podConfig : [
    name: 'demo-pod',
    image: '487835535578.dkr.ecr.ap-southeast-1.amazonaws.com/build-image:latest'
  ]
]

Closure pipeline_infra = { config ->
  stage("checkout") {
    checkout(scm)
  }
  try {
    config.stage_phase.each { job ->
      if(job instanceof ArrayList) {
        job_dict = [:]
        job.each { sub_job ->
          job_dict[sub_job.name] = {
            def stage_name = config.cloud + " " + sub_job.name
            stage(stage_name) {
              withEnv(config.environment) {
                echo "running with environment: ${config.environment}"
                sh '''
                  echo "env_code=$env_code"
                  echo "aws_code=$aws_code"
                '''
              }
              echo " name: ${sub_job.name}, ${sub_job.description}"
            }
          }
        }
        parallel job_dict
      }
      else {
        def stage_name = config.cloud + " " + job.name
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
}

def dev_environment = [
  workspace: [ build: true, test: false, destroy: false, env:'aws-com-dev-euc1' ],
  pr:        [:],
  codacydev: [ transition: 'codacystg', build: true, force: false, test: false, destroy: false, merge: false, merge_args: [], env:'aws-com-dev-euc1' ],
  codacystg: [ transition: 'codacysvc', build: true, force: false, test: true, destroy: false, merge: false, merge_args: [], env:'aws-com-dev-main-euc1' ],
  codacysvc: [ transition: 'codacydem', build: true, force: false, test: false, destroy: false,  merge: false, merge_args: [], env:'aws-com-svc-euc1' ],
  codacydem: [ transition: 'main', build: true, force: true, test: false, destroy: false, merge: true, merge_args: ['-X ours'], env:'aws-com-dev-dem-euc1' ],
  main:      [ transition: 'codacydev', build: true, force: true, test: false, destroy: false,  merge: true, merge_args: ['-X theirs'], env:'aws-com-dev-main-euc1' ]
]

dev_environment.pr = [ build: true, test: false, destroy: true, env: 'aws-com-dev-jenkins-euc1' ]

def branch = []
def create_workspace = false
def pr_id = false
def pr_changed_files = ["hello"]
def plan_only = true
def destroy = false
def run_test = false
def workspace
def pr_workspace_label = "workspace"
def gha_label = "gha"
def pr_workspace_label_present = false

if(env.CHANGE_ID) {
  dev_environment.pr = [ build: true, test: false, destroy: true, env: pullRequest.draft? 'aws-com-dev-euc1' : 'aws-com-dev-jenkins-euc1' ]
  stage("stage env") {
    withEnv(environment_euc1) {
      if (pullRequest.draft) {
        echo "i am a draft"
      } else {
        echo "i am not a draft"
      }
    }
  }
  if (!(pullRequest.getBase() ==~ 'production/.*')) {

    if (gha_label in pullRequest.labels.collect {it}) {
      echo "PR Label \"${gha_label}\" available. PR"
      return
    }

    if (pr_workspace_label in pullRequest.labels.collect {it}) {
      echo "PR LABEL \"${pr_workspace_label}\" available. workspace will be created"
    } else {
      echo "PR LABEL \"${pr_workspace_label}\" not available. pipeline will stop"
      currentBuild.result = 'SUCCESS'
      return
    }
  }

  branch = [ env.CHANGE_TARGET ]
  workspace = env.CHANGE_TARGET
  
  if (workspace == 'development') {
    create_workspace = true
    pr_changed_files = pullRequest.files.collect {
      it.getFilename()
    }
  }

  if (env.CHANGE_TARGET.startsWith('production/')) {
    branch = env.CHANGE_TARGET.tokenize('/')
  }

  pr_id = env.CHANGE_ID
  plan_only = true

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
  echo "pr target branch : ${pullRequest.getBase()}"
  echo "environment code : ${ ENV_GLOBAL }"  // environment variable declared in jenkins system / global properties
  runMe(
    name: 'mediocre',
    environment: 'infrastructure'
  )


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
    euc1: {    
      //environment = environment_euc1 
      runWithPod(pipeline_infra, node_config + [stage_phase: stage_phase, cloud: 'euc1', environment: environment_euc1 ]) 
    },
    cnn1: {
      //environment = environment_cnn1 
      runWithPod(pipeline_infra, node_config + [stage_phase: stage_phase, cloud: 'cnn1', environment: environment_cnn1 ]) 
    }
  )
}
