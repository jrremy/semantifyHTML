from flask import Flask, jsonify, request
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)
cors = CORS(app, origins='*')

model_name = "t5-small"
generator = pipeline("text2text-generation", model=model_name)

def preprocess_html(html):
    # Replace < and > with special tokens to prevent model confusion
    return html.replace('<', ' < ').replace('>', ' > ')

def postprocess_html(text):
    # Replace special tokens back to HTML tags
    return text.replace(' < ', '<').replace(' > ', '>')

@app.route("/convert", methods=['POST'])
def convert_to_semantic():
    input_html = request.json.get('html', '')
    input_text = f"translate non-semantic HTML to semantic HTML: {preprocess_html(input_html)}"
    result = generator(input_text, max_length=512)
    semantic_html = postprocess_html(result[0]['generated_text'])
    return jsonify({"semantic": semantic_html})

if __name__ == "__main__":
    app.run(debug=True, port=8080)