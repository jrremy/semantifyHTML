from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, origins='*')

@app.route("/convert", methods=['POST'])
def convert_to_semantic():
    input_html = request.json.get('html', '')
    output_html = "completed"
    return jsonify({"semantic": output_html})

if __name__ == "__main__":
    app.run(debug=True, port=8080)