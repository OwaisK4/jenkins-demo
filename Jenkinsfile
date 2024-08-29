pipeline {
    agent any

    stages {
        stage('Prepare Environment') {
            steps {
                script {
                    // Debugging: Print all environment variables
                    powershell 'gci env:\\ | ft name,value -autosize'
                    
                    // Add a ref to git config to make it aware of main branch
                    powershell '& git config --add remote.origin.fetch +refs/heads/main:refs/remotes/origin/main'
                    
                    // Fetch the main branch so you can do a diff against it
                    powershell '& git fetch --no-tags'
                }
            }
        }

        stage('Generate Git Diff') {
            steps {
                script {
                    // Perform a diff and save the output to a text file using the correct PR source branch
                    def diffOutput = powershell(returnStdout: true, script: '''
                        git diff --name-only origin/main..origin/$env:GITHUB_PR_SOURCE_BRANCH > git_diff.txt
                    ''').trim()

                    // Archive the git diff output as an artifact
                    archiveArtifacts artifacts: 'git_diff.txt', allowEmptyArchive: false
                }
            }
        }
    }
}
