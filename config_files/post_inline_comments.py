import os
from dotenv import load_dotenv
from openai import Client


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
