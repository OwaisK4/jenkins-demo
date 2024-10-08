from github import Github
import os

with open('PR_Report.txt', 'r') as file:
    pr_report_content = file.read()

g = Github(os.getenv('GITHUB_TOKEN'))

repo = g.get_repo('OwaisK4/jenkins-demo')

pr_number = int(os.getenv('GITHUB_PR_NUMBER'))
pull_request = repo.get_pull(pr_number)

pull_request.create_issue_comment(pr_report_content)