import os
from dotenv import load_dotenv
from openai import Client


load_dotenv()
key = os.getenv("OPENAI_API_KEY")


client = Client(api_key=key)

def generate_report(diff_file):
    with open(diff_file, 'r') as f:
        diff_content = f.read()


    prompt = f""" Use the following git diff file and generate a summary of all the changes that have occurred as if you were a PR reviewer bot. 
    Here is the file: {diff_content}
       """
    
    
    response = client.chat.completions.create(
        model='gpt-3.5-turbo-16k',
        messages=[{"role": "user", "content": [{"type": "text", "text": prompt}]}],
        max_tokens=1000,
        temperature=0.2,
        top_p=1.0
    )
    
    
    content = response.choices[0].message.content
        
    return content

if __name__ == "__main__":
    import sys
    diff_file = sys.argv[1]
    report = generate_report(diff_file)
    print(report)
