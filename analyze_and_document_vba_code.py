import os
import re
import spacy
from transformers import T5Tokenizer, TFT5ForConditionalGeneration

# Ensure sentencepiece is installed
try:
    import sentencepiece
except ImportError:
    print("Installing sentencepiece...")
    os.system('pip install sentencepiece')

# Initialize SpaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize T5 model and tokenizer
tokenizer = T5Tokenizer.from_pretrained('t5-base')
model = TFT5ForConditionalGeneration.from_pretrained('t5-base')

def extract_functions_from_bas(bas_path):
    with open(bas_path, 'r') as file:
        content = file.read()
        # Match both Functions and Subs
        functions = re.findall(r'(Function|Sub)\s+(\w+)\(', content)
        return functions, content

def generate_function_description(func_name, function_code):
    # Remove excess whitespace and extract relevant parts of the function
    function_code = function_code.strip()
    
    # Summarize the first two sentences using SpaCy
    doc = nlp(function_code)
    first_two_sentences = " ".join(sent.text for sent in list(doc.sents)[:2])
    
    # Use T5 for summarization
    input_text = f"summarize: {first_two_sentences}"
    input_ids = tokenizer.encode(input_text, return_tensors="tf", max_length=512, truncation=True)
    
    output = model.generate(input_ids, max_length=150, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(output[0], skip_special_tokens=True)
    
    return f"The function {func_name} performs: {summary}"

def process_vba_functions(bas_path):
    vba_functions, content = extract_functions_from_bas(bas_path)
    for func_type, func_name in vba_functions:
        # Extract the code of the specific function
        func_code_match = re.search(rf'{func_type}\s+{func_name}\(.*?\nEnd {func_type}', content, re.DOTALL)
        if func_code_match:
            function_code = func_code_match.group()
            function_description = generate_function_description(func_name, function_code)
            print(function_description)

# Example usage
if __name__ == "__main__":
    bas_path = r"D:\SG Hackathon\macro_code.bas"
    process_vba_functions(bas_path)
