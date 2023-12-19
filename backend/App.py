from flask import Flask, jsonify, request
from flask_cors import CORS #pip install Flask flask-cors
import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/start_buscaminas', methods=['GET'])
def start_buscaminas():
    subprocess.Popen(["python", "buscaminas.py"])
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
