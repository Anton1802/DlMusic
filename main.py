#! /usr/bin/python3

import requests
from bs4 import BeautifulSoup
import urllib.request
import difflib
from progress.bar import IncrementalBar
import csv


def similarity(word1, word2):
    normalized1 = word1.lower()
    normalized2 = word2.lower()
    matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
    return matcher.ratio()


with open('shazam.csv', newline="") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        author_search = row['Artist'].replace('"', '')
        string_search = row['Title'].replace('"', '')
        result_request = requests.get(
         f"https://savemusic.me/search/{string_search}/"
        )

        soup = BeautifulSoup(result_request.text, 'lxml')
        music_artists = soup.find_all("span", class_="music-artist")
        music_titles = soup.find_all("span", class_="music-title")
        download_a = soup.find_all("a", rel="nofollow")

        artists = []
        titles = []
        links = []

        for ln in download_a:
            links.append(ln.attrs['href'])

        for art in music_artists:
            artists.append(art.get_text())
        for title in music_titles:
            titles.append(title.get_text())

        bar = IncrementalBar("Search: ", max=len(music_titles))

        for cnt in range(0, len(music_titles)):
            bar.next()
            if similarity(author_search, artists[cnt]) > 0.50:
                if similarity(string_search, titles[cnt]) > 0.50:
                    url_download = "https://savemusic.me" + links[cnt]
                    file_name = "music/" + titles[cnt] + ".mp3"

        try:
            url_download
        except NameError:
            bar.finish()
            print('Link not finded!')
        else:
            if urllib.request.urlretrieve(url_download, file_name):
                print("\n Download completed!")
            else:
                print("\n Download failed!")

for i in range(5):
    print("Привет")
