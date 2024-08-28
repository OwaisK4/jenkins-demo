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
                    def oldCommit = sh(returnStdout: true, script: 'git rev-parse HEAD~1').trim()
                    def newCommit = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()

                    echo "Old Commit: ${oldCommit}"
                    echo "New Commit: ${newCommit}"

                    // Save the diff between the old and new code in a single file
                    bat 'git diff HEAD~1 HEAD > code_changes.diff'
                }
            }
        }

        stage('Archive Changeset') {
            steps {
                // Archive the diff file so it can be downloaded from Jenkins
                archiveArtifacts artifacts: 'code_changes.diff', allowEmptyArchive: true
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
