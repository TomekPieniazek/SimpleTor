import requests
import json
import flask
from rsa_generation import generate_rsa_key_pair

app = flask.Flask(__name__)


@app.route('/')
def main():
    private_key, public_key = generate_rsa_key_pair()
    return json.dumps({
        "public_key": public_key.decode()

    })


@app.route('/ping')
def ping():
    return 'pong'


@app.route('/kys')
def test():
    response = requests.get('http://localhost:5000/api')
    return response.text


if __name__ == '__main__':
    app.run()