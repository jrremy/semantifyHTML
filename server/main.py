import os
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from openai import OpenAI
import redis
from typing import Optional

import parse_html, explanation

app = Flask(__name__)
cors = CORS(app, origins='*')

# OpenAI setup to allow the option for AI-generated explanations for each HTML modification
openai_api_key: Optional[str] = os.environ.get("OPENAI_API_KEY")
openai_client: Optional[OpenAI] = None

if openai_api_key:
    try:
        openai_client = OpenAI(api_key=openai_api_key)
    except Exception as e:
        print(f"Error initializing OpenAI client: {e}")
else:
    print("OpenAI API key is missing, OpenAI-related features will be unavailable.")

# Redis setup for caching AI-generated explanations
redis_client = None
redis_available = True

try:
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
    # Test the connection
    redis_client.ping()
except (redis.ConnectionError, redis.TimeoutError):
    redis_available = False

@app.route("/convert", methods=['POST'])
def convert() -> Response:
    input_html = request.json.get('html', '')
    semantic_html, changes = parse_html.convert_to_semantic(input_html)
    return jsonify({"semantic": semantic_html, "changes": changes})

@app.route('/explanation', methods=['POST'])
def generate_explanation() -> Response:
    data: dict = request.json
    original_tag: str = data.get('original_tag')
    new_tag: str = data.get('new_tag')

    if not original_tag or not new_tag:
        return jsonify({'error': 'Both original_tag and new_tag are required.'}), 400

    # Use the function from explanation.py to generate and stream the explanation
    explanation_stream = explanation.generate_explanation_stream(
        original_tag, new_tag, openai_client, redis_client, redis_available
    )

    return Response(explanation_stream, content_type='text/plain')

@app.route("/load", methods=['POST'])
def load_url() -> Response:
    url: str = request.json.get('url', '')
    try:
        html_content = parse_html.load_full_page_html(url)
        return jsonify({"content": html_content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8080)