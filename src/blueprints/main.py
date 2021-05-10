import git
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from englishwiktionaryparser import EnglishWiktionaryParser

main = Blueprint('main', __name__)


# parse a word from wiktionary
@main.route('/parser')
@cross_origin(origin='*', headers=['Content-Type'])
def get_word():
    parser = EnglishWiktionaryParser()

    word = parser.fetch(request.args.get('word'))

    if word:
        return jsonify(word[0]), 200
    else:
        return jsonify({'message': 'Unknown word'}), 404


# an autopull from GitHub repo to PythonAnyWhere func
@main.route('/webhook', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def webhook():
    # TODO: Ха-ха, это не работает для приватных репозиториев, нужно сделать SSH ключ
    if request.method == 'POST':
        repo = git.Repo('./LeardsBackend')
        origin = repo.remotes.origin
        origin.pull()

        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


@main.route('/')
def index():
    return 'Index'


@main.route('/profile')
def profile():
    return 'Profile'
