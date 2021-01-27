from flask import Flask, redirect, url_for, request
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
cors = CORS(app, resources={r"/": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

wordExample = json.dumps({
        'word': 'Forest',
        'pronunciation': {
            'audioUK': 'https://upload.wikimedia.org/wikipedia/commons/a/ac/En-uk-forest.ogg',
            'transcriptionUK': '/ˈfɒɹɪst/',
            'audioUS': 'https://upload.wikimedia.org/wikipedia/commons/f/f6/En-us-forest.ogg',
            'transcriptionUS': '/ˈfɔɹɪst/'
        },
        'partsOfSpeech': {
            'noun': {
                'plural': 'Forests',
                'definitions': [
                    'A dense uncultivated tract of trees and undergrowth, larger than woods.',
                    [
                        'Any dense collection or amount.',
                        'a forest of criticism'
                    ],
                    '(historical) A defined area of land set aside in England as royal hunting ground or for other '
                    'privileged use; all such areas. ',
                    '(graph theory) A graph with no cycles; i.e., a graph made up of trees.',
                    '(computing, Microsoft Windows) A group of domains that are managed as a unit.',
                    'The colour forest green.'
                ],
                'meronyms': ['tree'],
                'derivedTerms': [
                    'Black Forest',
                    'Bracknell Forest',
                    'can\'t see the forest for the trees',
                    'Forest City',
                    'Forest County',
                    'forested',
                    'Forest Heath',
                    'forestial',
                    'forestlike',
                    'Peak Forest',
                    'rainforest',
                    'Sherwood Forest'
                ],
                'translation': 'Лес'
            },
            'verb': {
                'simplePresent': 'Forests',
                'presentParticiple': 'Foresting',
                'simple past': 'Forested',
                'pastParticiple': 'Forested',
                'definitions': ['(transitive) To cover an area with trees.'],
                'translation': None
            }
        }

    })


@app.route('/', methods=['GET', 'POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def get_word_example():
    if request.method == 'POST':
        word = request.json['word']
        return wordExample


if __name__ == '__main__':
    app.run(debug=True)
