import os
import random
import re
import customtkinter
from customtkinter import filedialog
import musicbrainzngs as mb
from tinytag import TinyTag
import time
import eyed3
from tqdm import tqdm
import urllib.request
import logging
eyed3.log.setLevel(logging.CRITICAL)


def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host)  # Python 3.x
        return True
    except:
        return False


if not connect():
    print("No connection!")
    exit()


def sort(songs):
    """
    Ordina un array di canzoni in modo che non ci siano due canzoni dello stesso artista in sequenza.
    """
    random.shuffle(songs)  # mischia le canzoni in modo casuale
    sorted_songs = []
    last_artist = None
    for song in songs:
        current_artist = searchArtist(song)
        if last_artist != current_artist:
            sorted_songs.append(song)
            last_artist = current_artist
        else:
            random.shuffle(songs)
            return sort(songs)
    return sorted_songs


def searchArtist(author):
    time.sleep(2)  # NECESSARIO
    # Imposta il tuo User-Agent
    mb.set_useragent("Ordinamento_Canzoni", "0.1")
    # Cerca gli artisti con il nome "The Beatles"
    result = mb.search_artists(author)
    # Recupera le informazioni sull'artista utilizzando il primo risultato della ricerca
    artist_id = result["artist-list"][0]["id"]
    artist_info = mb.get_artist_by_id(artist_id)
    # Stampa il nome dell'artista e la sua nazionalità
    return artist_info['artist']

# Store artists name


def storeArtists(inputtemp):
    # print(fileName)
    filemp3 = TinyTag.get(inputtemp)
    artist = filemp3.artist
    if(artist == None or artist == ""):
        audiofile = eyed3.load(inputtemp)
        filenametemp = os.path.basename(inputtemp)
        artist = input(
            "Per favore inserisci il nome dell'artista per questa canzone (" + filenametemp + "): ")
        audiofile.tag.artist = artist
        audiofile.tag.save()

    artist = searchArtist(artist)
    if 'area' not in artist:
        answ = input("Origine del cantante " +
                     artist["name"] + " sconosciuta, è italiano(i) o straniero(s): ")
        while answ != 'i' and answ != 's':
            answ = input("ERRORE, CARATTERE NON VALIDO! Origine del cantante " +
                         artist["name"] + " sconosciuta, è italiano(i) o straniero(s): ")
        if answ == 'i':
            songsITA.append(inputtemp)
        elif answ == 's':
            songsSTR.append(inputtemp)
    elif(artist['area']['name'] == 'Italy'):
        songsITA.append(inputtemp)
    else:
        songsSTR.append(inputtemp)


# Define songs's folder path
#SONGS_PATH = filedialog.askdirectory("Seleziona la cartella da cui prendere i file")
SONGS_PATH = "Canzoni/"
ext = ".mp3"
key = ""
divisor = "-"
i = 1
songs = []
songsITA = []
songsSTR = []

# Define songs list
for filename in os.listdir(SONGS_PATH):
    f = os.path.join(SONGS_PATH, filename)
    # checking if it is a file
    if os.path.isfile(f) and f.endswith(ext):
        print("Analazying: " + f + " ...")
        storeArtists(f)
        # songs.append(f)


if len(songsITA) == 0 or len(songsSTR) == 0:
    print("Nessuna canzone trovata")
    exit()

print("Shuffling songsITA")
songsITA = sort(songsITA)
print("Shuffling songsSTR")
songsSTR = sort(songsSTR)

is_italian = True
while songsITA or songsSTR:
    if len(songsITA) > 0:
        if is_italian:
            songs.append(songsITA.pop(0))
            is_italian = False
    else:
        is_italian = False
    if len(songsSTR) > 0:
        if not is_italian:
            songs.append(songsSTR.pop(0))
            is_italian = True
    else:
        is_italian = True

for song in songs:
    print(song)

#songs = shuffle(songs)

for filename in tqdm(songs):
    f = filename
    fileName = os.path.splitext(f)[0].split("/")[1]
    storeArtists(f)

    # Split fileName into old prefix and rest of file name
    if divisor in fileName:
        oldPrefix, restName = fileName.split(divisor, maxsplit=1)
    else:
        oldPrefix, restName = "", fileName

    if(i < 10):
        newPrefix = key + "00" + str(i)
    elif(i < 100):
        newPrefix = key + "0" + str(i)
    else:  # MAX 999 FILES
        newPrefix = key + str(i)

    old_name = os.path.splitext(f)[0] + ext

    if(re.search(r'\b' + re.escape(key) + r'\b', fileName)):
        # Key is present as whole word, so use only the new prefix
        newPrefix += divisor
        oldPrefix = ""
    else:
        # Key is not present as whole word, so keep the old prefix
        newPrefix = oldPrefix.split(key)[0] + newPrefix + divisor

    new_name = SONGS_PATH + newPrefix + restName + ext

    os.rename(old_name, new_name)
    i += 1
