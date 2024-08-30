pipeline {
    agent any

    stages {
        stage('Prepare Environment') {
            steps {
                script {
                    //Debugging to check if env is setup correctly
                    powershell 'gci env:\\ | ft name,value -autosize'
                    
                    //This modifies git config so that main is recognised as ref
                    //This is necessary so that git knows which branch to fetch and compare against.
                    powershell '& git config --add remote.origin.fetch +refs/heads/main:refs/remotes/origin/main'
                    
                    //This command fetches the latest changes from the remote repository, specifically the main branch.
                    powershell '& git fetch --no-tags'
                }
            }
        }

        stage('Generate Git Diff') {
            steps {
                script {
                    
                    //This command compares the main branch with the source branch of the PR ($env:GITHUB_PR_SOURCE_BRANCH) for changes specifically in Python files (*.py). 
                    //The output is saved to git_diff.txt. This is our change set.
                    def diffOutput = powershell(returnStdout: true, script: '''
                        git diff origin/main..origin/$env:GITHUB_PR_SOURCE_BRANCH -- *.py > git_diff.txt
                    ''').trim()

                    //Archive the git diff output as an artifact
                    archiveArtifacts artifacts: 'git_diff.txt', allowEmptyArchive: false
                }
            }
        }
    }
}
