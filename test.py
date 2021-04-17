import json

from englishwiktionaryparser import EnglishWiktionaryParser

parser = EnglishWiktionaryParser()
word = parser.fetch('ass')
word = json.dumps(word)
print(word)