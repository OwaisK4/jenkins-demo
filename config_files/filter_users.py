from github import Github
import os
import sys
from dotenv import load_dotenv
load_dotenv()


def get_pr_author(repo_name, pr_number):
    token = os.getenv('GITHUB_TOKEN')
    g = Github(token)
    
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    pr_author = str(pr.user.login.strip())
    return pr_author

if __name__ == "__main__":
    repo_name = 'OwaisK4/jenkins-demo'
    pr_number = int(os.getenv('GITHUB_PR_NUMBER'))
    author = get_pr_author(repo_name, pr_number)
    print(author)
