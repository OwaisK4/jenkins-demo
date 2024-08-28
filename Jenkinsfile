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
