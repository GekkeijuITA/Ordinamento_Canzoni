import customtkinter as ctk
from customtkinter import filedialog
import tkinter as tk
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
import threading
import sys
import json

SONGS_PATH = ""
ext = ".mp3"
key = ""
divisor = "-"
pref = 1
songsITA = []
songsSTR = []
songs = []
dialog = None
textbox = None
progressbar = None
app = None
button_2 = None

eyed3.log.setLevel(logging.CRITICAL)

def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host)  # Python 3.x
        return True
    except:
        return False

class GUI_Thread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        global dialog
        global textbox
        global progressbar
        global app
        global labelProgress
        global button_2

        # Modes: "System" (standard), "Dark", "Light"
        ctk.set_appearance_mode("dark")
        # Themes: "blue" (standard), "green", "dark-blue"
        ctk.set_default_color_theme("blue")

        app = ctk.CTk()
        app.geometry("600x480")
        app.title("Ordinamento Canzoni")

        frame_1 = ctk.CTkFrame(master=app)
        frame_1.pack(pady=20, padx=60, fill="both", expand=True)

        label_1 = ctk.CTkLabel(
            master=frame_1, justify=ctk.LEFT, text="Ordina canzoni", font=("Roboto", 24))
        label_1.pack(pady=10, padx=10)

        # SCELTA CANZONI

        button_1 = ctk.CTkButton(
            master=app, command=GUI_Thread.choose_folder, text="Scegli cartella con le canzoni da ordinare")
        button_1.pack(pady=10, padx=10)

        textbox = ctk.CTkTextbox(master=app)
        textbox.pack(pady=10, padx=10, fill="both", expand=True)

        # BARRA PROGRESSO
        labelProgress = ctk.CTkLabel(master=app , text="0/0")
        labelProgress.pack(pady=10, padx=10)
        progressbar = ctk.CTkProgressBar(master=app)
        progressbar.pack(padx=20, pady=10)
        progressbar.set(0)

        button_2 = ctk.CTkButton(master=app , command=Logic_Thread.sortSongs , text="Ordina canzoni")
        button_2.pack(pady=10, padx=10)

        # SCELTA DESTINAZIONE, FUSIONE E ORDINAMENTO

        app.mainloop()

        pass

    def pop_up(message , title):
        global dialog
        dialog = ctk.CTkInputDialog(text=message, title=title)
        dialog.get_input()


    def labelProgressUpdate(message , tot , countNum):
        labelProgress.configure(text=message + str(countNum) + "/" + str(tot))
        if tot != 0:
            progressbar.set(count/tot)
        else:
            progressbar.set(0)
        app.update()

    def get_songs():
        for filename in os.listdir(SONGS_PATH):
            f = os.path.join(SONGS_PATH, filename)
            if os.path.isfile(f) and f.endswith(ext):
                songs.append(f)


    def get_title(path):
        return os.path.basename(path)


    def write_textbox():
        i = 0
        textbox.configure(state="normal")
        textbox.delete(1.0, "end")
        if len(songs) == 0:
            textbox.insert("1.0", "Nessuna canzone trovata")
        else:
            for song in songs:
                textbox.insert(str(i)+".0", "• " + GUI_Thread.get_title(song)+"\n")
        textbox.configure(state="disabled")
        labelProgress.configure(text="0/" + str(len(songs)))

    def pop_up_input(message):
        global dialog
        dialog = ctk.CTkInputDialog(text=message, title="Attenzione!")
        ######## AUTOCOMPLETE HERE ########
        return dialog.get_input()
    
    def choose_folder():
        global SONGS_PATH
        SONGS_PATH = filedialog.askdirectory()
        songs.clear()
        GUI_Thread.get_songs()
        GUI_Thread.write_textbox()

class Logic_Thread:

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        Logic_Thread.sortSongs()
    
    def sort(songs):
        """
        Ordina un array di canzoni in modo che non ci siano due canzoni dello stesso artista in sequenza.
        """
        random.shuffle(songs)  # mischia le canzoni in modo casuale
        sorted_songs = []
        last_artist = None
        count = 0

        for song in songs:
            current_artist = Logic_Thread.searchArtist(song)
            if last_artist != current_artist:
                sorted_songs.append(song)
                last_artist = current_artist
            else:
                random.shuffle(songs)
                return Logic_Thread.sort(songs)
            count += 1
            songArray = "italiane"
            if(songs == songsSTR):
                songArray = "straniere"

            GUI_Thread.labelProgressUpdate("Sto ordinando le canzoni " + songArray + ": ", len(songs) , count)
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

    def searchInJson(string,fileName="artists.json"):
        """
        Cerca nel file json se è presente l'autore
        """
        print("Searching... " + re.sub('[^0-9a-zA-Z]+',' ',string))
        file = open(fileName)
        data = json.load(file)
        index = 0
        for i in data["artists"]:
            if re.search(re.sub('[^0-9a-zA-Z]+',' ',string), i["name"], re.IGNORECASE):
                return index
            index += 1
        return -1

    def addArtistToJson(name,country,fileName="artists.json"):
        """
        Aggiunge l'artista nella nostra "cache" senza ripetizioni
        """
        with open(fileName,'r+',encoding='utf-8') as file:
            file_data = json.load(file)
            alreadyIn = False
            for tuple in file_data["artists"]:
                if tuple["name"] == name:
                    alreadyIn = True
                    break
            if not alreadyIn:
                file_data["artists"].append({"name":name,"area":country})
                file.seek(0)
                json.dump(file_data,file,indent=4,ensure_ascii=False)

    # Store artists name
    def storeArtists(inputtemp):
        global dialog
        # print(fileName)
        filemp3 = TinyTag.get(inputtemp)
        artist = filemp3.artist
        audiofile = eyed3.load(inputtemp)

        if not audiofile.tag:
            audiofile.initTag()

        file = open("artists.json")
        data = json.load(file)

        if(artist == None or artist == ""):
            filenametemp = os.path.basename(inputtemp)
            index = Logic_Thread.searchInJson(filenametemp)
            if index != -1:
                audiofile.tag.artist = data["artists"][index]["name"]
            else:    
                artist = GUI_Thread.pop_up_input("Per favore inserisci il nome dell'artista per questa canzone (" + filenametemp + "): ") 
                audiofile.tag.artist = Logic_Thread.searchArtist(artist)["name"]
            audiofile.tag.save()

        index = Logic_Thread.searchInJson(artist)
        
        if index != -1:
            if data["artists"][index]["area"] == 'Italy':
                songsITA.append(inputtemp)
            else:
                songsSTR.append(inputtemp)
        else:
            artistInputTemp = artist
            artist = Logic_Thread.searchArtist(artist)

            while artist is None:
                artist = GUI_Thread.pop_up_input("Chiedo scusa, non ho trovato nessun artista con questo nome(" + artistInputTemp + ") per questa canzone (" + filenametemp +  "), riprova: ")
                artistInputTemp = artist
                artist = Logic_Thread.searchArtist(artist)

                if artist is not None:
                    audiofile.tag.artist = artist
                    audiofile.tag.save()

            if 'area' not in artist:
                answ = GUI_Thread.pop_up_input("Origine del cantante " + artist["name"] + " sconosciuta, è italiano(i) o straniero(s): ")
                while answ != 'i' and answ != 's':
                    answ = GUI_Thread.pop_up_input("ERRORE, CARATTERE NON VALIDO! Origine del cantante " + artist["name"] + " sconosciuta, è italiano(i) o straniero(s): ")
                if answ == 'i':
                    songsITA.append(inputtemp)
                    Logic_Thread.addArtistToJson(artist["name"],"Italy")
                elif answ == 's':
                    songsSTR.append(inputtemp)
                    Logic_Thread.addArtistToJson(artist["name"],"Foreign")
            
            elif(artist['area']['name'] == 'Italy'):
                songsITA.append(inputtemp)
                Logic_Thread.addArtistToJson(artist["name"],"Italy")
            else:
                songsSTR.append(inputtemp)
                Logic_Thread.addArtistToJson(artist["name"],"Foreign")

    def sortSongs():
        global pref
        global songsITA
        global songsSTR
        global songs
        global key
        global divisor
        global ext
        global SONGS_PATH
        global count

        button_2.configure(state="disabled")

        count = 0

        for song in songs:
            count += 1
            GUI_Thread.labelProgressUpdate("Analizzando le canzoni: " , len(songs) , count)
            Logic_Thread.storeArtists(song)

        if len(songsITA) == 0 or len(songsSTR) == 0:
            print("Nessuna canzone trovata")
            GUI_Thread.pop_up("Nessuna canzone trovata", "Attenzione!")
            return

        print("Shuffling songsITA")
        songsITA = Logic_Thread.sort(songsITA)
        print("Shuffling songsSTR")
        songsSTR = Logic_Thread.sort(songsSTR)

        songs.clear()
        
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

        count = 0
        for filename in songs:
            f = filename
            fileName = os.path.basename(f)

            #Logic_Thread.storeArtists(f)
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

            new_name = SONGS_PATH + "/" + newPrefix + restName

            os.rename(old_name, new_name)
            pref += 1
            count += 1
            GUI_Thread.labelProgressUpdate("Sto ordinando le canzoni: " , len(songs) , count)
        labelProgress.configure(text="Operazione completata!")
        button_2.configure(state="normal")

# MAIN

if not connect():
    GUI_Thread.pop_up("Nessuna connessione a internet!" , "Errore")
    print("No connection!")

gui = GUI_Thread()
logic = Logic_Thread()

gui.run()
logic.run()