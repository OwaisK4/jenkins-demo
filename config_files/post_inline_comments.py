import os
from github import Github
from dotenv import load_dotenv
from openai import Client
import re

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
github_token = os.getenv("GITHUB_TOKEN")

client = Client(api_key=openai_key)
g = Github(github_token)

repo_name = 'RayyanMinhaj/jenkins-demo'
pr_number = int(os.getenv('PR_NUMBER'))



def generate_ai_comments(diff_file):
    with open(diff_file, 'r') as f:
        diff_content = f.read()
    
    prompt = f"""
    You are reviewing code changes in a GitHub pull request. For each line added (marked with '+') or removed (marked with '-'), 
    provide a helpful, detailed comment about what the code does and any potential improvements or issues. You need to generate comments for every line.
    Here is the git diff file:
    {diff_content}

    Your response should strictly follow this format for each change:
    LINE NUMBER: COMMENT

    Example:
    + 12: This function adds two numbers and returns the result. Consider error handling.
    - 15: This line removes error handling for null values, which may cause issues.
    """

    response = client.chat.completions.create(
        model='gpt-3.5-turbo-16k',
        messages=[{"role": "assistant", "content": [{"type": "text", "text": prompt}]}],
        max_tokens=3000,
        temperature=0.1,
        top_p=1.0
    )

    return response.choices[0].message.content


def extract_file_from_diff(diff_content):
    #assumes only one file in git diff file [THIS NEEDS TO BE CHANGED LATER ON!]
    for line in diff_content.splitlines():
        if line.startswith('+++ b/'):
            return line[6:].strip()  #Extracts file path after '+++ b/'
    return None


def post_inline_comments(diff_file, ai_comments):

    with open(diff_file, 'r') as f:
        diff_content = f.read()


    repo = g.get_repo(repo_name)
    pull_request = repo.get_pull(pr_number)
    comments = ai_comments.split('\n')

    commit_id = os.getenv('GIT_COMMIT')
    commit = repo.get_commit(commit_id)

    file_path = re.search(r'\+\+\+ b/(.+)', diff_content)
    file_path = file_path.group(1)

    for comment in comments:
        if comment.strip():
            line_info, ai_comment = comment.split(':', 1)
            line_number = int(line_info.strip().lstrip("+-"))


            side = "RIGHT" if "+" in line_info else "LEFT"

            pull_request.create_review_comment(
                body=ai_comment.strip(), 
                path=file_path, 
                commit= commit,
                line=line_number,
                side=side
            )




if __name__ == "__main__":
    import sys
    diff_file = sys.argv[1]

    ai_comments = generate_ai_comments(diff_file)

    post_inline_comments(diff_file, ai_comments)

