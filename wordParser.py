from wiktionaryparser import WiktionaryParser

from services.parser import is_dictionary_empty

parser = WiktionaryParser()
parser.set_default_language('english')


def parse_word(word):
    fetched_word = parser.fetch(word)[0]

    if is_dictionary_empty(fetched_word):
        return 'null'
    else:
        # Audio
        uk_audio = None
        us_audio = None
        for audio in fetched_word['pronunciations']['audio']:
            if not (uk_audio and us_audio):
                if audio.find('En-uk') != -1:
                    uk_audio = audio
                if audio.find('En-us') != -1:
                    us_audio = audio
            else:
                break
        # Transcription
        uk_transcription = ''
        us_transcription = ''
        for text in fetched_word['pronunciations']['text']:
            substr_index = text.find('IPA:')
            if uk_transcription:
                if us_transcription:
                    break
                else:
                    if substr_index != -1:
                        for char in range(substr_index + 5, text.find('/', substr_index + 6) + 1):
                            us_transcription += text[char]
            else:
                if substr_index != -1:
                    for char in range(substr_index + 5, text.find('/', substr_index + 6) + 1):
                        uk_transcription += text[char]

        return {
            'word': word,
            'pronunciation': {
                'audioUK': uk_audio,
                'transcriptionUK': uk_transcription,
                'audioUS': us_audio,
                'transcriptionUS': us_transcription
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
        }
