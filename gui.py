import customtkinter as ctk
from customtkinter import filedialog
import os
import eyed3
import urllib.request
import logging
import random
import re
import musicbrainzngs as mb
from tinytag import TinyTag
import time
from tqdm import tqdm

SONGS_PATH = ""
ext = ".mp3"
key = ""
divisor = "-"
pref = 1
songsITA = []
songsSTR = []
songs = []

eyed3.log.setLevel(logging.CRITICAL)


def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host)  # Python 3.x
        return True
    except:
        return False


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

def sortSongs():
    global pref
    global songsITA
    global songsSTR
    global songs
    global key
    global divisor
    global ext
    global SONGS_PATH

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
    
    for filename in tqdm(songs):
        f = filename
        fileName = os.path.splitext(f)[0].split("/")[1]
        storeArtists(f)

        # Split fileName into old prefix and rest of file name
        if divisor in fileName:
            oldPrefix, restName = fileName.split(divisor, maxsplit=1)
        else:
            oldPrefix, restName = "", fileName

        if(pref < 10):
            newPrefix = key + "00" + str(pref)
        elif(pref < 100):
            newPrefix = key + "0" + str(pref)
        else:  # MAX 999 FILES
            newPrefix = key + str(pref)

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
        pref += 1

if not connect():
    print("No connection!")
    exit()


# Modes: "System" (standard), "Dark", "Light"
ctk.set_appearance_mode("dark")
# Themes: "blue" (standard), "green", "dark-blue"
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("600x480")
app.title("Ordinamento Canzoni")


def choose_folder():
    global SONGS_PATH
    SONGS_PATH = filedialog.askdirectory()
    get_songs()
    write_textbox()


def get_songs():
    for filename in os.listdir(SONGS_PATH):
        f = os.path.join(SONGS_PATH, filename)

        if os.path.isfile(f) and f.endswith(ext):
            songs.append(f)
            storeArtists(f)


def get_title(path):
    return os.path.basename(path)


def write_textbox():
    i = 0
    textbox.configure(state="normal")
    textbox.delete("1.0", "end")
    for song in songs:
        textbox.insert(str(i)+".0", "• " + get_title(song)+"\n")
    textbox.configure(state="disabled")


frame_1 = ctk.CTkFrame(master=app)
frame_1.pack(pady=20, padx=60, fill="both", expand=True)

label_1 = ctk.CTkLabel(
    master=frame_1, justify=ctk.LEFT, text="Ordina canzoni", font=("Roboto", 24))
label_1.pack(pady=10, padx=10)

# SCELTA CANZONI

button_1 = ctk.CTkButton(
    master=app, command=choose_folder, text="Scegli cartella con le canzoni da ordinare")
button_1.pack(pady=10, padx=10)

textbox = ctk.CTkTextbox(master=app)
textbox.pack(pady=10, padx=10, fill="both", expand=True)

button_2 = ctk.CTkButton(master=app , command=sortSongs , text="Ordina canzoni")
button_2.pack(pady=10, padx=10)

# SCELTA DESTINAZIONE, FUSIONE E ORDINAMENTO

app.mainloop()
