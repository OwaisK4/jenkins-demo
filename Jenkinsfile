pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Clean workspace before checkout
                cleanWs()

                // Checkout the code from the PR branch
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: 'FETCH_HEAD']],
                    doGenerateSubmoduleConfigurations: false,
                    extensions: [[$class: 'CleanBeforeCheckout'], [$class: 'CloneOption', noTags: false, shallow: false, depth: 0, reference: '']]],
                    submoduleCfg: [],
                    userRemoteConfigs: [[url: 'https://github.com/RayyanMinhaj/jenkins-demo.git', refspec: '+refs/pull/*:refs/remotes/origin/pr/*']]
                ])
            }
        }

        stage('Get Python File Changes') {
            steps {
                script {
                    // Get the base commit (last commit on main before PR was opened)
                    def baseCommit = bat(returnStdout: true, script: 'git merge-base origin/main HEAD').trim()
                    
                    // Get the current commit (PR branch at the time of opening)
                    def prCommit = bat(returnStdout: true, script: 'git rev-parse HEAD').trim()

                    echo "Base Commit: ${baseCommit}"
                    echo "PR Commit: ${prCommit}"

                    // Save the changes in Python files to a single file
                    bat "git diff ${baseCommit} ${prCommit} -- \"*.py\" > code_changes.txt"
                }
            }
        }

        stage('Archive Changeset') {
            steps {
                // Archive the code changes file so it can be downloaded from Jenkins
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
