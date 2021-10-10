from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from englishwiktionaryparser import EnglishWiktionaryParser

main_blueprint = Blueprint('main_blueprint', __name__)


# parse a word from wiktionary
@main_blueprint.route('/word_parser', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type'])
def get_word():
    parser = EnglishWiktionaryParser()

    word_data = parser.fetch(request.args.get('word'))

    if word_data:
        return jsonify(word_data[0]), 200
    else:
        return jsonify({'message': 'Unknown word'}), 404


@main_blueprint.route('/')
def index():
    return 'Index'


@main_blueprint.route('/profile')
def profile():
    return 'Profile'
