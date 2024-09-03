pipeline {
    agent any

    environment{
        OPENAI_API_KEY = credentials('OPENAI_API_KEY')
        PYTHON_PATH = "C:\\Users\\rayyan.minhaj\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"
    }

    stages {
        stage('Prepare Environment') {
            steps {
                script {

                    powershell 'gci env:\\ | ft name,value -autosize'
                    
                    powershell '& git config --add remote.origin.fetch +refs/heads/main:refs/remotes/origin/main'
                    
                    powershell '& git fetch --no-tags'
                }
            }
        }

        stage('Generate Git Diff') {
            steps {
                script {
                    // Perform a diff for .py files and save the output with the actual changes to a text file
                    def diffOutput = powershell(returnStdout: true, script: '''
                        git diff origin/main..origin/$env:GITHUB_PR_SOURCE_BRANCH -- *.py > git_diff.txt
                    ''').trim()

                    // Archive the git diff output as an artifact
                    archiveArtifacts artifacts: 'git_diff.txt', allowEmptyArchive: false
                }
            }
        }

        stage('Generate Report'){
            steps{
                script{
                    def reportOutput = powershell(script: "& ${env.PYTHON_PATH} generate_report.py git_diff.txt", returnStdout: true).trim()
                    writeFile file: 'PR_Report.txt', text: reportOutput
                }
            }    
        }
        stage('Archive Reports'){
            steps{
                script{
                    archiveArtifacts artifacts: 'PR_Report.txt', allowEmptyArchive: false
                }
            }           
        }
    }
}
