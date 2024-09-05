import os
import re
from dotenv import load_dotenv
from openai import Client
from github import Github


load_dotenv()
key = os.getenv("OPENAI_API_KEY")


client = Client(api_key=key)

def generate_report(diff_file):
    with open(diff_file, 'r') as f:
        diff_content = f.read()


    prompt = f"""You are reviewing code changes in a GitHub pull request. For each line added (marked with '+') or removed (marked with '-'), 
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
    
    
    content = response.choices[0].message.content
        
    return content

if __name__ == "__main__":
    
    import sys
    diff_file = sys.argv[1]
    report = generate_report(diff_file)
    print(report)

    ## Now we publish the inline comments
    with open(diff_file, 'r') as f:
        diff_content = f.read()

    github_token = os.getenv("GITHUB_TOKEN")
    g = Github(github_token)
    repo_name = 'RayyanMinhaj/jenkins-demo'
    pr_number = int(os.getenv('PR_NUMBER'))

    repo = g.get_repo(repo_name)
    pull_request = repo.get_pull(pr_number)
    
    comments = report.split('\n')

    commit_id = os.getenv('GIT_COMMIT')
    commit = repo.get_commit(commit_id)

    file_path_match = re.search(r'\+\+\+ b/(.+)', diff_content)
    file_path = file_path_match.group(1)

    for comment in comments:
        if comment.strip():
            line_info, ai_comment = comment.split(':', 1)
            line_number = int(line_info.strip().lstrip("+-"))

            side = "RIGHT" if "+" in line_info else "LEFT"

            pull_request.create_review_comment(
                body=ai_comment.strip(), 
                path=file_path, 
                commit=commit,
                line=line_number,
                side=side
            )








