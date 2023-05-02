import os
import eyed3
import time
import musicbrainzngs as mb
from tqdm import tqdm
import logging
import urllib.request

SONGS_PATH = "Canzoni/"
ext = ".mp3"

def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False

if not connect():
    print("No connection!")
    exit()

eyed3.log.setLevel(logging.CRITICAL)

def searchArtist(author):
    time.sleep(2) # NECESSARIO
    # Imposta il tuo User-Agent
    mb.set_useragent("Ordinamento_Canzoni", "0.1")
    # Cerca gli artisti con il nome "The Beatles"
    result = mb.search_artists(author)
    # Recupera le informazioni sull'artista utilizzando il primo risultato della ricerca
    artist_id = result["artist-list"][0]["id"]
    artist_info = mb.get_artist_by_id(artist_id)
    # Stampa il nome dell'artista e la sua nazionalità
    #print(artist_info['artist']['name'])

for filename in tqdm(os.listdir(SONGS_PATH)):
    f = os.path.join(SONGS_PATH , filename)
    # checking if it is a file
    if not (os.path.isfile(f)) and f.endswith(ext):
        print(f + " not a file")
    else:
        audiofile = eyed3.load(f)
        if audiofile.tag is None:
            if not audiofile.tag:
                audiofile.initTag()
        if audiofile.tag.artist is None:
            artist = input("Per favore inserisci il nome dell'artista per questa canzone (%s): " %os.path.splitext(f)[0].split("/")[1])
            audiofile.tag.artist = artist
            audiofile.tag.save()
        if audiofile is not None:
            searchArtist(audiofile.tag.artist)
