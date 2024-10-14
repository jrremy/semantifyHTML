import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
from playwright.sync_api import sync_playwright
from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

app = Flask(__name__)
cors = CORS(app, origins='*')

def convert_to_semantic(html):
    soup = BeautifulSoup(html, 'html.parser')
    changes = []

    def log_change(tag, new_name):
        # Get classes and id, if available
        classes = ' '.join(tag.get('class', []))
        tag_id = tag.get('id', '')

        # Construct original tag HTML
        original_tag_parts = [f'<{tag.name}']
        if classes:
            original_tag_parts.append(f'class="{classes}"')
        if tag_id:
            original_tag_parts.append(f'id="{tag_id}"')
        original_tag_html = ' '.join(original_tag_parts) + '>'

        # Construct new tag HTML
        new_tag_parts = [f'<{new_name}']
        if classes:
            new_tag_parts.append(f'class="{classes}"')
        if tag_id:
            new_tag_parts.append(f'id="{tag_id}"')
        new_tag_html = ' '.join(new_tag_parts) + '>'

        # Check if this change already exists in the changes list
        for change in changes:
            if change['original_tag'] == original_tag_html and change['new_tag'] == new_tag_html:
                # If it exists, increment the frequency
                change['frequency'] += 1
                break
        else:
            # If it doesn't exist, add it with a frequency of 1
            changes.append({
                'original_tag': original_tag_html,
                'new_tag': new_tag_html,
                'frequency': 1
            })
        
        tag.name = new_name

    # Replace <div> elements with semantic alternatives if the tag name is in their class or id
    for div in soup.find_all('div'):
        if 'header' in div.get('class', []) or 'header' in div.get('id', []):
            log_change(div, 'header')
        elif 'footer' in div.get('class', []):
            log_change(div, 'footer')
        elif 'main' in div.get('class', []):
            log_change(div, 'main')
        elif 'nav' in div.get('class', []) or 'nav' in div.get('id', []):
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

@app.route('/explanation', methods=['POST'])
def generate_explanation():
    data = request.json
    original_tag = data.get('original_tag')
    new_tag = data.get('new_tag')

    if not original_tag or not new_tag:
        return jsonify({'error': 'Both original_tag and new_tag are required.'}), 400
    
    prompt = (
        f"The HTML tag '{original_tag}' was changed to '{new_tag}'. "
        f"Explain the purpose and specific function of the '{new_tag}' tag in HTML, including its impact on semantics, accessibility, and SEO. "
        f"Provide a concise and clear explanation, no more than a couple complete sentences."
    )
    
    def generate():
        try:
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield(chunk.choices[0].delta.content)
    
        except Exception as e:
            app.logger.error(f"Error during OpenAI request: {e}")
            yield jsonify({'error': 'There was an error processing your request.'}), 500
            
    return generate(), {'Content-Type': 'text/plain'}

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

@app.route("/load", methods=['POST'])
def load_url():
    url = request.json.get('url', '')
    try:
        html_content = load_full_page_html(url)
        soup = BeautifulSoup(html_content, 'html.parser')
        return jsonify({"content": soup.prettify()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8080)