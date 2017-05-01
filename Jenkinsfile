// Set periodic trigger at 21:12 every day.
properties([
    pipelineTriggers([cron('12 21 * * *')]),
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

def builders = [:]
for (x in names) {
    def name = x
    builders[name] = {
        node(name) {
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
            }
        }
    }
}

parallel builders
