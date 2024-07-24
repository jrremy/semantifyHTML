from flask import Flask, jsonify, request
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

app = Flask(__name__)
cors = CORS(app, origins='*')

tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-125M")
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-125M")

def transform_html(input_html):
    prompt = f"Transform the following HTML code into semantic HTML:\n{input_html}\nSemantic HTML:"
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
    attention_mask = inputs['attention_mask']
    input_ids = inputs['input_ids']
    
    outputs = model.generate(input_ids, max_length=2000, num_return_sequences=1, attention_mask=attention_mask, pad_token_id=tokenizer.eos_token_id)
    semantic_html = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return semantic_html.split("Semantic HTML:")[1].strip()

@app.route("/convert", methods=['POST'])
def convert_to_semantic():
    input_html = request.json.get('html', '')
    output_html = transform_html(input_html)
    return jsonify({"semantic": output_html})

if __name__ == "__main__":
    app.run(debug=True, port=8080)