pipeline {
    agent any

    stages {
        stage('Prepare Environment') {
            when {
                changeRequest()
            }
            steps {
                script {
                    // Print all environment variables for debugging
                    powershell 'gci env:\\ | ft name,value -autosize'
                    
                    // Add a ref to git config to make it aware of main branch
                    powershell '& git config --add remote.origin.fetch +refs/heads/main:refs/remotes/origin/main'
                    
                    // Fetch the main branch so you can do a diff against it
                    powershell '& git fetch --no-tags'
                }
            }
        }

        stage('Generate Git Diff') {
            when {
                changeRequest()
            }
            steps {
                script {
                    // Perform a diff and save the output to a text file
                    def diffOutput = powershell(returnStdout: true, script: '''
                        git diff --name-only origin/main..origin/$env:BRANCH_NAME > git_diff.txt
                    ''').trim()

                    // Archive the git diff output as an artifact
                    archiveArtifacts artifacts: 'git_diff.txt', allowEmptyArchive: false
                }
            }
        }
    }
}
