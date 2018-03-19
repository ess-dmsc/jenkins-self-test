// Trigger every two hours.
properties([
  pipelineTriggers([cron('12 H/2 * * *')]),
])

shell_script="""
which clang-format
which cmake
which cppcheck
which gcovr
which git
which g++
which lcov
which python
which valgrind
"""

def names = [
  'master',
  'dmbuild01.dm.esss.dk',
  'dmbuild02.dm.esss.dk',
  'dmbuild03.dm.esss.dk'
]

def failure_function(exception_obj, failureMessage) {
  withCredentials([string(
    credentialsId: 'jenkins-notification-email',
    variable: 'NOTIFICATION_EMAIL'
  )]) {
    emailext body: '${DEFAULT_CONTENT}\n\"' + failureMessage + '\"\n\nCheck console output at $BUILD_URL to view the results.',
      to: "${NOTIFICATION_EMAIL}",
      subject: "${DEFAULT_SUBJECT}"
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
        sh(shell_script)
        sh "python test_free_disk_space.py --min 10.0"
      }
    }
  }
}

try {
  parallel builders
} catch (e) {
  failure_function(e, 'Jenkins self-test failed')
}
