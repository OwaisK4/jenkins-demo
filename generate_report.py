import os
from dotenv import load_dotenv
from openai import Client


load_dotenv()
key = os.getenv("OPENAI_API_KEY")


client = Client(api_key=key)

def generate_report(diff_file):
    with open(diff_file, 'r') as f:
        diff_content = f.read()


    prompt = f"""You are a PR reviewing bot, a language model trained by OpenAI. Your purpose is to act as a highly experienced software engineer and provide a thorough review of the code hunks
    and suggest code snippets to improve key areas such as:
        - Logic
        - Security
        - Performance
        - Consistency
        - Error handling
        - Maintainability
        - Modularity
        - Complexity
        - Optimization
        - Best practices: DRY, SOLID, KISS
        
    Identify and resolve significant concerns to improve overall code quality while deliberately disregarding minor issues.
        
    Next, I need you to give me a "summarization" response which should include the following content:
        - **Walkthrough**: A high-level summary of the overall change instead of 
        specific files within 80 words.
        - **Changes**: A markdown table of files and their summaries. Group files 
        with similar changes together into a single row to save space.
        - **Poem**: Below the changes, include a whimsical, short poem written by 
        a rabbit to celebrate the changes. Format the poem as a quote using 
        the ">" symbol and feel free to use emojis where relevant.
        
    Lastly, craft concise release notes for the pull request. Focus on the purpose and user impact, categorizing changes as "New Feature", "Bug Fix", 
    "Documentation", "Refactor", "Style", "Test", "Chore", or "Revert". Provide a bullet-point list, e.g., "- New Feature: Added search functionality to the UI". Limit your response to 50-100 words 
    and emphasize features visible to the end-user while omitting code-level details.
        
    Here are the code changes: {diff_content}"""


    response = client.chat.completions.create(
        model='gpt-3.5-turbo-16k',
        messages=[{"role": "assistant", "content": prompt}],
        max_tokens=3000,
        temperature=0.1,
        top_p=1.0
    )


    resp = response.choices[0].message.content

    return resp

if __name__ == "__main__":
    diff_file = 'git_diff.txt'
    
    report = generate_report(diff_file)
    
    print(report)
