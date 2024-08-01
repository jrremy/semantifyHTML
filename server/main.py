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
    
    for tag, class_map in tag_mapping.items():
        for cls, new_tag in class_map.items():
            elements = soup.find_all(tag, class_=cls)
            for element in elements:
                element.name = new_tag
                if 'class' in element.attrs:
                    del element.attrs['class']
    
    # Wrap nav-item elements in a <ul> if they are not already wrapped
    for nav in soup.find_all('nav'):
        list_items = nav.find_all('li')
        if list_items:
            ul = soup.new_tag('ul')
            for li in list_items:
                ul.append(li.extract())
            nav.append(ul)
    
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