pipeline {
    agent any

    environment {
        // Define paths and filenames
        OLD_CODE_FILE = 'old_code.txt'
        NEW_CODE_FILE = 'new_code.txt'
        DIFF_FILE = 'diff.txt'
    }

    triggers {
        // Trigger the pipeline when a pull request is opened
        githubPullRequest {
            // Make sure you have the GitHub Pull Request Builder plugin installed and configured
            triggerPhrase('retest')
            useGitHubHooks()
        }
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the PR branch
                checkout([$class: 'GitSCM', 
                    userRemoteConfigs: [[url: 'https://github.com/RayyanMinhaj/jenkins-demo.git']], 
                    branches: [[name: "origin/${env.CHANGE_BRANCH}"]]
                ])
            }
        }

        stage('Fetch Previous Commit') {
            steps {
                script {
                    // Fetch the previous commit from the base branch
                    bat 'git fetch origin'
                    bat "git checkout ${env.CHANGE_TARGET}"
                    bat 'git pull origin ${env.CHANGE_TARGET}'
                    bat "git batow ${env.CHANGE_TARGET} > ${env.OLD_CODE_FILE}"
                }
            }
        }

        stage('Get New Code') {
            steps {
                script {
                    // Switch to the PR branch and get the new code
                    bat "git checkout ${env.CHANGE_BRANCH}"
                    bat "git batow ${env.CHANGE_BRANCH} > ${env.NEW_CODE_FILE}"
                }
            }
        }

        stage('Compare Changes') {
            steps {
                script {
                    // Compare the old and new code
                    bat "diff ${env.OLD_CODE_FILE} ${env.NEW_CODE_FILE} > ${env.DIFF_FILE}"
                }
            }
        }

        stage('Archive Artifacts') {
            steps {
                // Archive the diff file and any other relevant files
                archiveArtifacts artifacts: "${env.DIFF_FILE}", allowEmptyArchive: true
            }
        }
    }

    post {
        always {
            // Clean up
            deleteDir()
        }
    }
}
