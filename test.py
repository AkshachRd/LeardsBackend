from bs4 import BeautifulSoup
import requests

with open("index.html", "r") as f:
    session = requests.Session()
    response = session.get("https://en.wiktionary.org/wiki/forest?printable=yes")

    soup = BeautifulSoup(response.text.replace('>\n<', '><'), 'html.parser')

    contents = soup.find_all('ul')[10]
    j = []

    prev_end = 0
    while contents.text.find('/', prev_end):
        transcription_start_index = contents.text.find('/', prev_end)
        if transcription_start_index < prev_end:
            break
        transcription_end_index = contents.text.find('/', transcription_start_index + 1)
        print((transcription_start_index, transcription_end_index))
        j.append(
            contents.text[transcription_start_index:transcription_end_index + 1])
        #if transcription_end_index + 1 < prev_end:
          #  break
        prev_end = transcription_end_index + 1
    print(j)