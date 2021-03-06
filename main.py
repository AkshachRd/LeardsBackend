from flask import Blueprint, request
from flask_cors import cross_origin
from wordParser import parse_word
import json
import git
import os

main = Blueprint('main', __name__)


# parse a word from wiktionary
@main.route('/parser')
@cross_origin(origin='*', headers=['Content-Type'])
def get_word():
    word = request.args.get('word')
    return json.dumps(parse_word(word))


# an autopull from GitHub repo to PythonAnyWhere func
@main.route('/webhook', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('./LeardsBackend')
        origin = repo.remotes.origin
        origin.pull()
        os.system('cmd /c "python -m pip install -r requirements.txt"')

        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


@main.route('/')
def index():
    return 'Index'


@main.route('/profile')
def profile():
    return 'Profile'
