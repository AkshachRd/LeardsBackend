from wiktionaryparser import WiktionaryParser
from functions import is_dictionary_empty

parser = WiktionaryParser()
parser.set_default_language('english')

print(parser.fetch('asdasaфsda')[0])


print(is_dictionary_empty(parser.fetch('turn on')[0]))

