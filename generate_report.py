import os
from dotenv import load_dotenv
from openai import Client


load_dotenv()
key = os.getenv("OPENAI_API_KEY")


client = Client(api_key=key)

def generate_report(diff_file):
    with open(diff_file, 'r') as f:
        diff_content = f.read()


    prompt = f"""
    I am going to give you a file that contains the output of a git diff command. You need to answer as a Software Engineer and tell me what the changes are, and 
    what new features have been added or removed inside the file (use the filenames while addressing any changes)
        
    Here are the code changes: {diff_content}"""


    response = client.chat.completions.create(
        model='gpt-3.5-turbo-16k',
        messages=[{"role": "assistant", "content": prompt}],
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
