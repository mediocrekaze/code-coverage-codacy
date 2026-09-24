@Library('demo@main') _

import org.jenkinsci.plugins.workflow.steps.FlowInterruptedException


def k8s = new io.kubernetes.Pod()

def cloud = ""
def node_config = [
  podConfig : [
    name: 'demo-pod',
    image: '487835535578.dkr.ecr.ap-southeast-1.amazonaws.com/build-image:latest'
  ]
]

def node_config_euc = [:]
def node_config_cnn = [:]



def test_instance_config = [
  euc: [
    dev: [
      address: 'https://test.dev.mediocrewind.com',
      role: 'euc-dev-test'
    ],
    prd: [
      address: 'https://test.mediocrewind.com',
      role: 'euc-prd-test'
    ]
  ],
  cnn: [
    dev: [
      address: 'https://test.dev.mediocrewind.cn',
      role: 'cnn-dev-test'
    ],
    prd: [
      address: 'https://test.mediocrewind.cn',
      role: 'cnn-prd-test'
    ]
  ]
]

Closure get_test_instance_config = {
  if (env.CHANGE_ID) {
    return 'dev'
  }
  if (branch_name in ['codacystg', 'codacysvc', 'codacydem']) {
    return 'dev'
  }
  if (branch_name ==~ /^production\/.*/) {
    return 'prd'
  }
  return null
}

def euc_test_display = [:]

Closure euc_get_test = { 
  def testme = new hashtag.Test()
  def test_environment = get_test_instance_config(env.BRANCH_NAME)
  if (test_environment == null) {
    return
  }
  def test_instance = test_instance_config.euc[test_environment]
  euc_test_display = testme.getDisplay([
    test_instance_role: test_instance.role,
    test_instance_addr: test_instance.address
  ])
}

k8s.dynamicPod(
  euc_get_test,
  node_config + [cloud: 'euc']
)

def cnn_test_display = [:]

Closure cnn_get_test = { 
  def testme = new hashtag.Test()
  def test_environment = get_test_instance_config(env.BRANCH_NAME)
  if (test_environment == null) {
    return
  }
  def test_instance = test_instance_config.cnn[test_environment]
  cnn_test_display = testme.getDisplay([
    test_instance_role: test_instance.role,
    test_instance_addr: test_instance.address
  ])
}

k8s.dynamicPod(
  cnn_get_test,
  node_config + [cloud: 'cnn']
)

def environment_euc = [
  "env_code=euc",
  "aws_code=aws-com",
  "role_value=${euc_test_display.role_value}",
  "addr_value=${euc_test_display.addr_value}"
]

def environment_cnn = [
  "env_code=cnn",
  "aws_code=aws-cnn",
  "role_value=${cnn_test_display.role_value}",
  "addr_value=${cnn_test_display.addr_value}"
]


Closure fast_forward = { config ->
  stage("Fast Forward")
    echo("fast forward (${ config.source } -> ${ config.destination })")
    sshagent (credentials: ['mediocrewind-ssh']) {
      sh("""
        mkdir ~/.ssh
        ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts
        git clone git@github.com:mediocrekaze/code-coverage-codacy.git . -b ${ config.source }
        git config --global --add safe.directory "\$PWD"
        git push origin ${ config.source }:${ config.destination } ${config?.force ? '--force' : ''}
      """)
    }
}

Closure merge = { config ->
  stage("Merge") {
    echo("merge (${ config.source } -> ${ config.destination })")
    sshagent (credentials: ['mediocrewind-ssh']) {
      sh("""
        mkdir ~/.ssh
        ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts
        git config --global user.email "arcenoallan214@gmail.com"
        git config --global user.name "Allan Arceno"
        git clone git@github.com:mediocrekaze/code-coverage-codacy.git . -b ${ config.destination }
        git config --global --add safe.directory "\$PWD"
        git merge ${ config.merge_args.join(' ') } origin/${ config.source } --no-edit
        git push origin ${ config.destination } ${config?.force ? '--force' : ''}
      """)
    }
  }

}

// -----------------------------------------------------------------------------------------------------------------------------------------
// pipeline logic execution
Closure pipeline_infra = { config ->
  stage(config.cloud + " " + "checkout") {
    checkout(scm)
  }
  try {
    config.stage_phases.each { job ->
      if(job instanceof ArrayList) {
        def job_dict = [:]
        job.each { sub_job ->
          job_dict[sub_job.name] = {
            def stage_name = config.cloud + " " + sub_job.name
            stage(stage_name) {
              withEnv(config.environment + ["STAGE_NAME=${sub_job.name}", "config_name=${config.config_name}" ]) {
                echo "running with environment: ${config.environment}"
                sh '''
                  echo "env_code=$env_code aws_code=$aws_code role_value=$role_value addr_value=$addr_value stage_name='$STAGE_NAME' config_name='$config_name'"   >> env.txt
                '''
              }
              echo " name: ${sub_job.name}, ${sub_job.description}"
            }
          }
        }
        parallel(job_dict)
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

def dev_environment_backup = [
  workspace: [ build: true, test: false, destroy: false, env:'euc-dev' ],
  pr:        [:],
  codacydev: [ transition: 'codacystg', build: true, force: false, test: false, destroy: false, merge: false, merge_args: [], env:'euc-dev' ],
  codacystg: [ transition: 'codacysvc', build: true, force: false, test: true, destroy: false, merge: false, merge_args: [], env:'euc-dev-main' ],
  codacysvc: [ transition: 'codacydem', build: true, force: false, test: false, destroy: false,  merge: false, merge_args: [], env:'euc-svc' ],
  codacydem: [ transition: 'main', build: true, force: true, test: false, destroy: false, merge: true, merge_args: ['-X ours'], env:'euc-dev-dem' ],
  main:      [ transition: 'codacydev', build: true, force: true, test: false, destroy: false,  merge: true, merge_args: ['-X theirs'], env:'euc-dev-main' ]
]

def dev_environment = [
    workspace: [ build: true, test: false, destroy: false, env:'ENV_CODE-dev' ],
    pr:        [:],
    codacydev: [ transition: 'codacystg', build: false, force: false, test: false, destroy: false, merge: false, merge_args: [], env:'ENV_CODE-dev' ],
    codacystg: [ transition: 'codacysvc', build: true, force: false, test: true, destroy: false, merge: false, merge_args: [], env:'ENV_CODE-dev-main' ],
    codacysvc: [ transition: 'codacydem', build: true, force: false, test: false, destroy: false,  merge: false, merge_args: [], env:'ENV_CODE-svc' ],
    codacydem: [ transition: 'main', build: true, force: true, test: false, destroy: false, merge: true, merge_args: ['-X ours'], env:'ENV_CODE-dev-dem' ],
    main:      [ transition: 'codacydev', build: false, force: true, test: false, destroy: false,  merge: true, merge_args: ['-X theirs'], env:'ENV_CODE-dev-main' ]
  ]

dev_environment.pr = [ build: true, test: false, destroy: true, env: 'ENV_CODE-dev-jenkins' ]
euc_test_display
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

// -----------------------------------------------------------------------------------------------------------------------------------------
// pull request
if(env.CHANGE_ID) {
  dev_environment.pr = [ build: true, test: false, destroy: true, env: pullRequest.draft? 'ENV_CODE-dev' : 'ENV_CODE-dev-jenkins' ]
  stage("stage env") {
    withEnv(environment_euc) {
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
      pr_workspace_label_present = true
    } else {
      echo "PR LABEL \"${pr_workspace_label}\" not available. pipeline will stop"
      currentBuild.result = 'SUCCESS'
      return
    }
  }

  branch = [ env.CHANGE_TARGET ]
  workspace = env.CHANGE_TARGET
  
  // creating test workspace on development
  if (workspace == 'codacydev') {
    create_workspace = true
    pr_changed_files = pullRequest.files.collect {
      it.getFilename()
    }
  }

  // production plan for pr
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

// -----------------------------------------------------------------------------------------------------------------------------------------
// branch
else {
  branch = env.BRANCH_NAME.tokenize('/')
  pr_id = false
  workspace = branch[0]

  if (dev_environment.containsKey( branch[0] )) {
    plan_only = false
    if (!dev_environment[branch[0]].isEmpty()) {
      destroy = dev_environment[branch[0]]['destroy']
      run_test = dev_environment[branch[0]]['test']
    }
    if (branch[0] == 'workspace') {
      workspace = branch[1..-1].join("-").toLowerCase().replaceAll("_","-")
      if (!(workspace ==~ "(?=.{3,20}\$)(?!-)(?!.*--)[a-z0-9-]+(?<!-)") || dev_environment.containsKey(workspace)) {
        error("invalid workspace name")
      }
    }
  }
  else if (branch[0] == 'production') {
    plan_only = false
  }
  else if (branch[0] == 'release') {}
  else if (branch[0] == 'main') {}

  else {
    branch = [ 'codacydev' ]
    workspace = "codacydev"
    plan_only = true
  }
}

// -----------------------------------------------------------------------------------------------------------------------------------------
// development (actual deployment)

if (dev_environment.containsKey(branch[0])) {
  def stage_prepare = [
    [ name: 'configuration', description: 'i am configuration on a non-production phase' ],
    [
      [ name: 'workspace1', description: 'i am workspace one on a non-production phase' ],
      [ name: 'workspace2', description: 'i am workspace two on a non-production phase' ],
      [ name: 'workspace3', description: 'i am workspace three on a non-production phase' ],
    ],
    [ name: 'dependencies', description: 'i am dependencies on a non-production phase' ]
  ]
  def stage_construct = [
    [ name: 'build', description: 'i am build on a non-production phase' ],
    [ name: 'deployment', description: 'i am deployment on a non-production phase' ]
  ]
  def stage_codetest = [
    [ name: 'test_code', description: 'i am test_code on a non-production phase' ],
    [ name: 'test_output', description: 'i am test_output on a non-production phase' ]
  ]
  def stage_finalize = [
    [ name: 'user_acceptance', description: 'i am user_acceptance on a non-production phase' ],
    [ name: 'backup', description: 'i am backup on a non-production phase' ],
  ]
  def stage_report = [
    [ name: 'report', description: 'i am report on a non-production phase' ]
  ]  
  def stage_not_pr = [
    [ name: 'not_pr', description: 'i am not pr on a non-production phase' ]
  ]

  def stage_phases = []

  if (env.CHANGE_ID) {
    if (pullRequest.draft) {
      println("PR is draft")
      stage_phases += stage_prepare
      stage_phases += stage_construct
    } else {
      print("PR is not draft")
      stage_phases += stage_prepare
      stage_phases += [
        stage_construct + stage_codetest,
        stage_finalize + stage_report
      ]
    }
  } else {
    println("We are not on a PR")
    stage_phases += stage_prepare
    stage_phases += [
      stage_construct + stage_finalize
    ]
    stage_phases += stage_not_pr
  }

  if (dev_environment[branch[0]].build || pr_workspace_label_present) {
    if (plan_only) {
      if (create_workspace)
        try {
          parallel(
            euc: {
              runWithPod(                              
                pipeline_infra,
                node_config_euc + node_config + [
                  stage_phases: stage_phases,
                  cloud: 'euc',
                  config_name: dev_environment['pr'].env.replace('ENV_CODE', 'euc'),
                  environment: environment_euc
                ]
              )
            },
            cnn: {
              runWithPod(
                pipeline_infra,
                node_config_cnn + node_config + [
                  stage_phases: stage_phases,
                  cloud: 'cnn',
                  config_name: dev_environment['pr'].env.replace('ENV_CODE', 'cnn'),
                  environment: environment_cnn
                ]
              )
            }
          )        
        } catch(e) {
            throw e
        }
    } else {
        try {
          parallel(
            euc: {    
              runWithPod(
                pipeline_infra,
                node_config_euc + node_config + [
                  stage_phases: stage_phases,
                  cloud: 'euc',
                  config_name: dev_environment[branch[0]].env,
                  environment: environment_euc
                ]
              )
            },
            cnn: {
              runWithPod(
                pipeline_infra,
                node_config_cnn + node_config + [
                  stage_phases: stage_phases,
                  cloud: 'cnn',
                  config_name: dev_environment[branch[0]].env,
                  environment: environment_cnn
                ]
              )
            }
          )          
        } catch (e) {
            throw e
        }
    }
  }
  // merge and fast forward
  if (pr_id == false && plan_only == false && dev_environment[branch[0]].containsKey('transition')) {
    if (dev_environment[branch[0]].merge)
      runWithPod(merge, 
        node_config + [
          cloud: 'euc',
          source: branch[0],
          destination: dev_environment[branch[0]].transition,
          force: dev_environment[branch[0]].force,
          merge_args: dev_environment[branch[0]].merge_args
      ])
    else
      runWithPod(fast_forward, 
        node_config + [
        cloud: 'euc',
        source: branch[0],
        destination: dev_environment[branch[0]].transition,
        force: dev_environment[branch[0]].force
      ])      
  }
}

// -----------------------------------------------------------------------------------------------------------------------------------------
// production (actual deployment)
else if (branch[0] == 'production') {
  def stage_phases = [:]
  def plan_phase = [:]
  def env = ''
  workspace = 'production'

  if (branch[1] == 'auth') {
    stage_phases = [
      [ name: 'configuration', description: 'i am configuration on a production phase' ],
      [ name: 'workspace', description: 'i am workspace one on a production phase' ],
      [ name: 'dependencies', description: 'i am dependencies on a production phase' ]
    ]
    plan_phase = [
      [ name: 'configuration', description: 'i am configuration on a production phase' ],
      [ name: 'workspace', description: 'i am workspace one on a production phase' ],
      [ name: 'dependencies', description: 'i am dependencies on a production phase' ]
    ]
    env = "aws-com-key-euc1"
  } else {
    stage_phases = [
      [ name: 'configuration', description: 'i am configuration on a production phase' ],
      [ name: 'workspace', description: 'i am workspace one on a production phase' ],
      [ name: 'dependencies', description: 'i am dependencies on a production phase' ]
    ]
    plan_phase = [
      [ name: 'configuration', description: 'i am configuration on a production phase' ],
      [ name: 'workspace', description: 'i am workspace one on a production phase' ],
      [ name: 'dependencies', description: 'i am dependencies on a production phase' ]
    ]
    env = "aws-com-${branch[1]}-euc1".toString()
  }

  if (plan_only) {
    runWithPod(
      pipeline_infra,
      node_config + [
        stage_phases: stage_phases,
        //cloud: 'cnn1',
        //environment: environment_cnn1
      ]
    ) 
  } else {
    try {
      runWithPod(
        pipeline_infra,
        node_config + [
          stage_phases: stage_phases,
          //cloud: 'cnn1',
          //environment: environment_cnn1
        ]
      )      
    } catch (e) {
      throw e
    }
  }
}

if (branch[0] == 'main') {

}


//if(env.CHANGE_ID) {
//  parallel(
//    euc1: {    
//      //environment = environment_euc1 
//      runWithPod(pipeline_infra, node_config + [stage_phase: stage_phase, cloud: 'euc1', environment: environment_euc1 ]) 
//    },
//    cnn1: {
//      //environment = environment_cnn1 
//      runWithPod(pipeline_infra, node_config + [stage_phase: stage_phase, cloud: 'cnn1', environment: environment_cnn1 ]) 
//    }
//  )
//}
