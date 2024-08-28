pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                //clean workspace b4 checkout
                cleanWs()
                
                //checking the code from repository
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
                    //get the lsat 2 recent commits and place them into a txt file
                    //def oldCommit = bat(returnStdout: true, script: 'git rev-parse HEAD~1').trim()
                    //def newCommit = bat(returnStdout: true, script: 'git rev-parse HEAD').trim()

                    // Get the base commit and the latest commit
                    bat(script: 'git merge-base origin/main HEAD > base_commit.txt', returnStdout: true)
                    bat(script: 'git rev-parse HEAD > pr_commit.txt', returnStdout: true)

                    def baseCommit = readFile('base_commit.txt').trim()
                    def prCommit = readFile('pr_commit.txt').trim()

                    echo "Base Commit: ${baseCommit}"
                    echo "PR Commit: ${prCommit}"

                    // Save the changes in Python files to a single file
                    bat(script: "git diff ${prCommit} ${baseCommit} -- \"*.py\" > code_changes.txt")
                }
            }
        }

        stage('Archive Changeset') {
            steps {
                //archive the txt file as an artifact so we can download it
                archiveArtifacts artifacts: 'code_changes.txt', allowEmptyArchive: true
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
