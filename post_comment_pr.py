import os
from dotenv import load_dotenv
from octokit import Octokit

load_dotenv()
token = os.getenv('GITHUB_TOKEN')

octokit = Octokit(token=token)

owner = 'RayyanMinhaj'
repo = 'jenkins-demo'
pr_number = 1

with open('PR_Report.txt', 'r') as file:
    pr_report_content = file.read()


response = octokit.issues.create_comment(
    owner=owner,
    repo=repo,
    issue_number=pr_number,
    body=pr_report_content
)

print('Comment posted successfully:', response)