from flask import Flask, jsonify, request
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        data['name'] = 'Can'
        data['buu'] = '88993'
        response = jsonify(data)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
	

        return jsonify({'data': 'hello'})


if __name__ == '__main__':
    app.run('0.0.0.0', port= 80)
