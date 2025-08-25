import os
import logging
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from openai import OpenAI
import redis
from typing import Optional

import parse_html, explanation

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
cors = CORS(app, origins='*')

# OpenAI setup to allow the option for AI-generated explanations for each HTML modification
openai_api_key: Optional[str] = os.environ.get("OPENAI_API_KEY")
openai_client: Optional[OpenAI] = None

if openai_api_key:
    try:
        openai_client = OpenAI(api_key=openai_api_key)
        # Test the connection
        openai_client.models.list()
        logger.info("OpenAI client initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing OpenAI client: {e}")
        openai_client = None
else:
    logger.warning("OpenAI API key is missing, OpenAI-related features will be unavailable.")

# Redis setup for caching AI-generated explanations
redis_client = None
redis_available = False

# Get Redis configuration from environment variables
redis_host = os.environ.get("REDIS_HOST", "localhost")
redis_port = int(os.environ.get("REDIS_PORT", 6379))

try:
    redis_client = redis.Redis(host=redis_host, port=redis_port, db=0, decode_responses=True)
    # Test the connection
    redis_client.ping()
    redis_available = True
    logger.info(f"Redis connection established successfully at {redis_host}:{redis_port}")
except (redis.ConnectionError, redis.TimeoutError) as e:
    logger.warning(f"Redis connection failed: {e}")
    redis_available = False
except Exception as e:
    logger.error(f"Unexpected Redis error: {e}")
    redis_available = False

@app.route("/convert", methods=['POST'])
def convert() -> Response:
    try:
        input_html = request.json.get('html', '')
        if not input_html:
            return jsonify({"error": "No HTML content provided"}), 400
            
        semantic_html, changes = parse_html.convert_to_semantic(input_html)
        logger.info(f"Converted HTML with {len(changes)} changes")
        return jsonify({"semantic": semantic_html, "changes": changes})
    except Exception as e:
        logger.error(f"Error in convert endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/explanation', methods=['POST'])
def generate_explanation() -> Response:
    try:
        data: dict = request.json
        original_tag: str = data.get('original_tag')
        new_tag: str = data.get('new_tag')

        if not original_tag or not new_tag:
            return jsonify({'error': 'Both original_tag and new_tag are required.'}), 400

        logger.info(f"Generating explanation for {original_tag} -> {new_tag}")
        
        explanation_stream = explanation.generate_explanation_stream(
            original_tag, new_tag, openai_client, redis_client, redis_available
        )

        return Response(explanation_stream, content_type='text/plain')
    except Exception as e:
        logger.error(f"Error in explanation endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/load", methods=['POST'])
def load_url() -> Response:
    try:
        url: str = request.json.get('url', '')
        if not url:
            return jsonify({"error": "No URL provided"}), 400
            
        logger.info(f"Loading HTML from URL: {url}")
        html_content = parse_html.load_full_page_html(url)
        return jsonify({"content": html_content})
    except Exception as e:
        logger.error(f"Error loading URL {url}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=['GET'])
def health_check() -> Response:
    """Health check endpoint to verify service status"""
    status = {
        "status": "healthy",
        "openai_available": openai_client is not None,
        "redis_available": redis_available,
        "timestamp": logging.Formatter().formatTime(logging.LogRecord("", 0, "", 0, "", (), None))
    }
    return jsonify(status)

if __name__ == "__main__":
    logger.info("Starting SemantifyHTML server...")
    app.run(host="0.0.0.0", port=8080, debug=False)