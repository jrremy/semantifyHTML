from flask import Flask, jsonify, request
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
import re

app = Flask(__name__)
cors = CORS(app, origins='*')

# Define the mapping between non-semantic classes/tags and semantic tags
tag_mapping = {
    'div': {
        'nav': 'nav',
        'header': 'header',
        'footer': 'footer',
        'main': 'main',
        'section': 'section',
        'article': 'article',
        'title': 'h1',
        'post-title': 'h2',
        'post-body': 'p',
        'section-header': 'h1',
        'section-content': 'p',
        'nav-item': 'li'
    },
    'a': {
        'default': 'a'
    },
    'span': {
        'highlight': 'mark',
        'important': 'strong',
        'emphasis': 'em'
    }
}

# Function to replace non-semantic tags with semantic tags
def convert_to_semantic(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Example 1: Convert <div> elements that have a specific role into <section>
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

    # Example 2: Convert <b> tags to <strong>
    for b_tag in soup.find_all('b'):
        b_tag.name = 'strong'

    # Example 3: Convert <i> tags to <em>
    for i_tag in soup.find_all('i'):
        i_tag.name = 'em'

    # Example 4: Convert <span> tags used as block elements into <p>
    for span_tag in soup.find_all('span'):
        if 'block' in span_tag.get('class', []):  # Example condition
            span_tag.name = 'p'

    # You can add more rules here depending on your specific use case

    # Return the modified HTML content
    return soup.prettify()

@app.route("/convert", methods=['POST'])
def convert():
    input_html = request.json.get('html', '')
    semantic_html = convert_to_semantic(input_html)
    return jsonify({"semantic": semantic_html})

@app.route("/load", methods=['POST'])
def load_url():
    url = request.json.get('url', '')
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the HTML content from the response
        html_content = response.text

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        return jsonify({"content": soup.prettify()})

if __name__ == "__main__":
    app.run(debug=True, port=8080)