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
                
                // Save the latest commit hash from the main branch
                bat(script: 'git rev-parse HEAD > main_commit.txt', returnStdout: true)
            }
        }

        stage('Checkout PR Branch') {
            steps {
                script {
                    // Checkout the feature branch (current PR branch)
                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: "${env.CHANGE_BRANCH}"]],
                        doGenerateSubmoduleConfigurations: false,
                        extensions: [[$class: 'CleanBeforeCheckout'], [$class: 'CloneOption', noTags: false, shallow: false, depth: 0, reference: '']],
                        submoduleCfg: [],
                        userRemoteConfigs: [[url: 'https://github.com/RayyanMinhaj/jenkins-demo.git']]
                    ])
                    
                    // Save the latest commit hash from the feature branch
                    bat(script: 'git rev-parse HEAD > feature_commit.txt', returnStdout: true)
                }
            }
        }

        stage('Get Changeset') {
            steps {
                script {
                    //get the lsat 2 recent commits and place them into a txt file
                    //def oldCommit = bat(returnStdout: true, script: 'git rev-parse HEAD~1').trim()
                    //def newCommit = bat(returnStdout: true, script: 'git rev-parse HEAD').trim()

                    // Get the base commit and the latest commit
                    //bat(script: 'git merge-base origin/main HEAD > base_commit.txt', returnStdout: true)
                    //bat(script: 'git rev-parse HEAD > pr_commit.txt', returnStdout: true)

                    //def baseCommit = readFile('base_commit.txt').trim()
                    //def prCommit = readFile('pr_commit.txt').trim()

                    //echo "Base Commit: ${baseCommit}"
                    //echo "PR Commit: ${prCommit}"

                    

                    // Save the changes in Python files to a single file
                    //bat(script: "git diff ${prCommit} ${baseCommit} -- \"*.py\" > code_changes.txt")


                    // ////////////////////////////////////////////////////////////////////////////////////////
                    def mainCommit = readFile('main_commit.txt').trim()
                    def featureCommit = readFile('feature_commit.txt').trim()

                    echo "Main Commit: ${mainCommit}"
                    echo "Feature Commit: ${featureCommit}"

                    // Get the diff between the feature branch and the main branch
                    bat(script: "git diff ${mainCommit} ${featureCommit} -- \"*.py\" > code_changes.txt", returnStdout: true)
                    
                    // Display the content of the code_changes.txt file for debugging
                    bat(script: 'type code_changes.txt')
                
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
