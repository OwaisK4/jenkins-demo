pipeline {
    agent any

    environment {
        OPENAI_API_KEY = credentials('OPENAI_API_KEY') 
        PYTHON_PATH = 'C:\\Users\\rayyan.minhaj\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
    }

    stages {
        stage('Prepare Environment') {
            steps {
                script {
                    // Debugging: Print all environment variables
                    powershell 'gci env:\\ | ft name,value -autosize'
                    
                    // Add a ref to git config to make it aware of the main branch
                    powershell '& git config --add remote.origin.fetch +refs/heads/main:refs/remotes/origin/main'
                    
                    // Fetch the main branch so you can do a diff against it
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

                    // Save the git_diff.txt file for use in the next stage
                    writeFile file: 'git_diff.txt', text: diffOutput
                }
            }
        }

        stage('Generate Report') {
            steps {
                script {
                    // Update the path to Python executable
                    //def pythonPath = 'C:\\Users\\rayyan.minhaj\\AppData\\Local\\Programs\\Python\\Python312\\python.exe'
                    // Run the Python script to generate the report
                    def reportOutput = powershell(script: "& '$env:PYTHON_PATH' generate_report.py git_diff.txt", returnStdout: true).trim()
                    // Save the report to a file
                    writeFile file: 'PR_Report.txt', text: reportOutput
                }
            }
        }

        stage('Archive Report') {
            steps {
                script {
                    // Archive the generated report as an artifact
                    archiveArtifacts artifacts: 'PR_Report.txt', allowEmptyArchive: false
                }
            }
        }
    }
}
