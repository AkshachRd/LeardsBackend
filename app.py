from flask import Flask, redirect, url_for, request
from flask_cors import CORS, cross_origin
from wordParser import parse_word
import json
import git

app = Flask(__name__)
cors = CORS(app, resources={r"/": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def get_word_example():
    if request.method == 'POST':
        word = request.json['word']
        return json.dumps(parse_word(word))


@app.route('/update_server', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def webhook():
    return 'Hello'
    if request.method == 'POST':
        repo = git.Repo('./')
        origin = repo.remotes.origin

        origin.pull()

        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


if __name__ == '__main__':
    app.run(debug=True)
