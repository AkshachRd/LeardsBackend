from englishwiktionaryparser import EnglishWiktionaryParser

from src.services.parser import is_dictionary_empty

parser = EnglishWiktionaryParser()


def parse_word(word):
    fetched_word = parser.fetch(word)
    if fetched_word:
        return fetched_word[0]
    else:
        return None

    """
    if is_dictionary_empty(fetched_word):
        return None
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
        return fetched_word[0]
    """