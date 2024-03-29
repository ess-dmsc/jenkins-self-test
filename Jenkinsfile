// Trigger every two hours.
properties([
  pipelineTriggers([cron('12 2 * * *')]),
])

docker_nodes = nodesByLabel('docker')
inttest_nodes = nodesByLabel('inttest')
master_nodes = nodesByLabel('master')
names = docker_nodes + inttest_nodes + master_nodes

def failure_function(exception_obj, failureMessage) {
   withCredentials([string(
     credentialsId: 'jenkins-notification-email',
     variable: 'NOTIFICATION_EMAIL'
   )]) {
     emailext body: '${DEFAULT_CONTENT}\n\"' + failureMessage + '\"\n\nCheck console output at $BUILD_URL to view the results.',
       to: "${NOTIFICATION_EMAIL}",
       subject: '${DEFAULT_SUBJECT}'
   }

  throw exception_obj
}

def builders = [:]
for (x in names) {
  def name = x
  builders[name] = {
    node(name) {
      cleanWs()

      stage('Checkout') {
        checkout([
          $class: 'GitSCM',
          branches: [[name: '*/master']],
          userRemoteConfigs: [[
            url: 'https://github.com/ess-dmsc/jenkins-self-test'
          ]]
        ])
      }
      stage('Test') {
        sh "python test_free_disk_space.py --min 10.0"
      }
    }
  }
}

try {
  timeout(time: 1, unit: 'HOURS') {
    parallel builders
  }
} catch (e) {
  failure_function(e, 'Jenkins self-test failed')
}
