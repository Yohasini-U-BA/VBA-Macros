import openai
import os

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_vba_function(vba_code):
    prompt = f"""
    Analyze the following VBA function and explain its functionality in simple, human-readable terms. 
    Focus on:
    1. What the function does
    2. Its inputs
    3. Its output
    4. The step-by-step process it follows
    
    VBA Code:
    {vba_code}
    
    Provide the explanation in a way that someone with no programming knowledge can understand.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert in VBA and explaining technical concepts to non-technical people."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

def read_bas_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Example usage
file_path = r"D:\SG Hackathon\macro_code.bas"
vba_code = read_bas_file(file_path)

explanation = analyze_vba_function(vba_code)

# Write explanation to a file
with open("D:\SG Hackathon\documentation.txt", 'w') as f:
    f.write(explanation)

print("Explanation has been written to "D:\SG Hackathon\documentation.txt"")
