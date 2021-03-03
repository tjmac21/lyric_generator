import configparser
import requests
from bs4 import BeautifulSoup

def getAccessToken():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['Client_Access_Token']['token']

token = getAccessToken()

def searchMusicArtist(name):
    api_url = "https://api.genius.com/search?q={}".format(name)
    headers = {"authorization": token}
    r = requests.get(api_url, headers=headers)
    print(len(r.json()["response"]["hits"]))
    return r.json()

def searchPopularSongs(name):
    id = searchMusicArtist(name)
    try:
        id = id["response"]["hits"][0]["result"]["primary_artist"]["id"]
    except:
        pass
    api_url = "https://api.genius.com/artists/{}/songs".format(id)
    print(api_url)
    headers = {"authorization": token}
    params = {
        "sort": "popularity",
        "per_page": 10
    }
    r = requests.get(api_url, headers=headers, params=params)
    return r.json()

def scrapeLyricText(name):
    songs = searchPopularSongs(name)
    try:
        songs = songs["response"]["songs"]
    except:
        pass
    lyrics_url = []
    for song in songs:
        lyrics_url.append(song["url"])

    song_lyrics = []
    for url in lyrics_url:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, features='lxml')
        
        div = soup.select("div[class='lyrics']")
        if len(div) == 0:
            print(url)
            continue
        a_tags = div[0].find_all('a')

        curr_lyrics =  []
        for a_tag in a_tags:
            if len(a_tag.text) > 0 and a_tag.text[0] != "[":
                curr_lyrics.append(a_tag.text.replace('\n', ' '))
        song_lyrics.append(curr_lyrics)
    return song_lyrics

lyrics = scrapeLyricText("drake")
print(len(lyrics))



