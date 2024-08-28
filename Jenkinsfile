pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Clean workspace before checkout
                cleanWs()
                
                // Checkout the code from the repository
                checkout([
                    $class: 'GitSCM', 
                    branches: [[name: '*/main']],
                    doGenerateSubmoduleConfigurations: false,
                    extensions: [[$class: 'CleanBeforeCheckout'], [$class: 'CloneOption', noTags: false, shallow: false, depth: 0, reference: '']],
                    submoduleCfg: [],
                    userRemoteConfigs: [[url: 'https://github.com/RayyanMinhaj/jenkins-demo.git']]
                ])
            }
        }

        stage('Get Changeset') {
            steps {
                script {
                    // Get the last two commits for comparison
                    def oldCommit = bat(returnStdout: true, script: 'git rev-parse HEAD~1').trim()
                    def newCommit = bat(returnStdout: true, script: 'git rev-parse HEAD').trim()

                    echo "Old Commit: ${oldCommit}"
                    echo "New Commit: ${newCommit}"

                    // Save the differences for .py files
                    bat 'git diff HEAD~1 HEAD -- "*.py" > code_changes.txt'
                }
            }
        }

        stage('Archive Changeset') {
            steps {
                // Archive the code changes so they can be downloaded from Jenkins
                archiveArtifacts artifacts: 'code_changes.txt', allowEmptyArchive: true
            }
        }
    }

    post {
        always {
            // Clean up the workspace after the build
            cleanWs()
        }
    }
}
