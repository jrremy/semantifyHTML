import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
from playwright.sync_api import sync_playwright
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)
cors = CORS(app, origins='*')

def convert_to_semantic(html):
    soup = BeautifulSoup(html, 'html.parser')
    changes = []

    def log_change(tag, new_name):
        changes.append({
            'original_tag': tag.name,
            'new_tag': new_name,
            'content': tag.text.strip()
        })
        tag.name = new_name

    # Replace <div> elements with semantic alternatives if the tag name is in their class
    for div in soup.find_all('div'):
        if 'header' in div.get('class', []):
            log_change(div, 'header')
        elif 'footer' in div.get('class', []):
            log_change(div, 'footer')
        elif 'main' in div.get('class', []):
            log_change(div, 'main')
        elif 'nav' in div.get('class', []):
            log_change(div, 'nav')

    # Convert <b> tags to <strong>
    for b_tag in soup.find_all('b'):
        log_change(b_tag, 'strong')

    # Convert <i> tags to <em>
    for i_tag in soup.find_all('i'):
        log_change(i_tag, 'em')

    # Convert <span> tags used as block elements into <p>
    for span_tag in soup.find_all('span'):
        if 'block' in span_tag.get('class', []):  # Example condition
            log_change(span_tag, 'p')

    # Can add more rules here depending on specific use case
    
    modified_html = soup.prettify()
    return modified_html, changes

@app.route("/convert", methods=['POST'])
def convert():
    input_html = request.json.get('html', '')
    semantic_html, changes = convert_to_semantic(input_html)
    return jsonify({"semantic": semantic_html, "changes": changes})

def generate_explanation(original_tag, new_tag):
    prompt = f"Explain why the HTML tag '{original_tag}' was changed to '{new_tag}' in a brief and clear way."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )
    return response.choices[0].text.strip()

@app.route('/explanation', methods=['POST'])
def get_explanation():
    data = request.json
    original_tag = data['original_tag']
    new_tag = data['new_tag']
    explanation = generate_explanation(original_tag, new_tag)
    return jsonify({'explanation': explanation})


@app.route("/load", methods=['POST'])
def load_url():
    url = request.json.get('url', '')
    try:
        html_content = load_full_page_html(url)
        soup = BeautifulSoup(html_content, 'html.parser')
        return jsonify({"content": soup.prettify()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def load_full_page_html(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Launch headless browser
        page = browser.new_page()
        page.goto(url)
        # Wait for the content to load
        page.wait_for_load_state("networkidle")
        # Get the full page content after JavaScript execution
        content = page.content()
        browser.close()
        return content

if __name__ == "__main__":
    app.run(debug=True, port=8080)