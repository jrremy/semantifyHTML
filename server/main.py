from flask import Flask, jsonify, request
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
from playwright.sync_api import sync_playwright

app = Flask(__name__)
cors = CORS(app, origins='*')

def convert_to_semantic(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Convert <div> elements that have a specific role into <section>
    for div in soup.find_all('div'):
        if 'header' in div.get('class', []):
            div.name = 'header'
        elif 'footer' in div.get('class', []):
            div.name = 'footer'
        elif 'main' in div.get('class', []):
            div.name = 'main'
        elif 'nav' in div.get('class', []):
            div.name = 'nav'
        else:
            div.name = 'section'

    # Convert <b> tags to <strong>
    for b_tag in soup.find_all('b'):
        b_tag.name = 'strong'

    # Convert <i> tags to <em>
    for i_tag in soup.find_all('i'):
        i_tag.name = 'em'

    # Convert <span> tags used as block elements into <p>
    for span_tag in soup.find_all('span'):
        if 'block' in span_tag.get('class', []):  # Example condition
            span_tag.name = 'p'

    # Can add more rules here depending on specific use case

    return soup.prettify()

@app.route("/convert", methods=['POST'])
def convert():
    input_html = request.json.get('html', '')
    semantic_html = convert_to_semantic(input_html)
    return jsonify({"semantic": semantic_html})

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