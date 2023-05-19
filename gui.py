import customtkinter as ctk
from customtkinter import filedialog
import tkinter as tk
from tkinter import messagebox
from ttkwidgets.autocomplete import AutocompleteCombobox

import os
import eyed3
import urllib.request
import logging
import random
import re
import musicbrainzngs as mb
from tinytag import TinyTag
import time
import threading
import json
from fuzzywuzzy import fuzz


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
button_1 = None
fileJson = "artists.json"

eyed3.log.setLevel(logging.CRITICAL)

def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host)  # Python 3.x
        return True
    except:
        return False

class GUI_Thread(threading.Thread):

    def __init__(self, stop_event):
        super().__init__()
        self.stop_event = stop_event
    
    def run(self):
        while not self.stop_event.is_set():
            global dialog
            global textbox
            global progressbar
            global app
            global labelProgress
            global button_2
            global button_1
            global lista 

            lista = []
            
            file = open(fileJson, encoding='utf-8')
            data = json.load(file)
            for i in data["artists"]:
                lista.append(i["name"])

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

            button_2 = ctk.CTkButton(master=app , command=Logic_Thread.sortSongs , text="Ordina canzoni" , state="disabled")
            button_2.pack(pady=10, padx=10)
            
            logic_thread = Logic_Thread(self.stop_event)

            button_3 = ctk.CTkButton(master=app, command=logic_thread.stop_thread, text="Interrompi")
            button_3.pack(pady=10, padx=10)

            app.protocol("WM_DELETE_WINDOW", on_closing)

            app.mainloop()

            pass

    def pop_up(message , title):
        messagebox.showinfo(title=title, message=message)


    def labelProgressUpdate(message , tot , countNum):
        labelProgress.configure(text=message + str(countNum) + "/" + str(tot))
        if tot != 0:
            progressbar.set(count/tot)
        else:
            progressbar.set(0)
        app.update()

    def get_songs():
        """
        Prende tutte le canzoni nella cartella SONGS_PATH e le mette in un array.
        """
        for filename in os.listdir(SONGS_PATH):
            f = os.path.join(SONGS_PATH, filename)
            if os.path.isfile(f) and f.endswith(ext):
                songs.append(f)


    def get_title(path):
        return os.path.basename(path)


    def write_textbox():
        """
        Prende l'array songs e lo scrive nel textbox.
        """
        i = 0
        textbox.configure(state="normal")
        textbox.delete(1.0, "end")
        if len(songs) == 0:
            textbox.insert("1.0", "Nessuna canzone trovata")
        else:
            songs.sort(reverse=True)
            for song in songs:
                textbox.insert(str(i)+".0", "• " + GUI_Thread.get_title(song)+"\n")
        textbox.configure(state="disabled")
        labelProgress.configure(text="0/" + str(len(songs)))
    
    def pop_up_area(artistName):
        global value
        value = ""

        top = tk.Toplevel(app)
        top.geometry("220x190")
        top.title("Attenzione!")

        x = int(app.winfo_x() + (app.winfo_width() / 2 - top.winfo_width()))
        y = int(app.winfo_y() + (app.winfo_height() / 2 - top.winfo_height()))

        top.geometry("+{}+{}".format(x, y))

        label = tk.Label(top,text="Seleziona l'area di provenienza dell'artista: " + artistName)
        label.bind('<Configure>' , lambda e: label.config(wraplength=top.winfo_width()-10))
        label.grid()

        def save_and_destroy(valueB):
            global value
            value = valueB
            top.destroy()

        button_it = tk.Button(top,text="Italiano/a")
        button_it.configure(command=lambda: save_and_destroy("i"))
        button_it.grid()

        button_str = tk.Button(top,text="Straniero/a")
        button_str.configure(command=lambda: save_and_destroy("s"))
        button_str.grid()

        top.bind("<Return>" , lambda event: save_and_destroy)

        top.wait_window()  # attendi che la finestra venga chiusa

        return value    

    def pop_up_input(message):
        global value
        value = ""
        """
        Pop up per prendere in input il nome dell'autore con autocomplete, ritorna il valore inserito.
        """
        top = tk.Toplevel(app)
        top.geometry("220x190")
        top.title("Attenzione!")

        x = int(app.winfo_x() +( app.winfo_width() / 2 - top.winfo_width()))
        y = int(app.winfo_y() +( app.winfo_height() / 2 - top.winfo_height()))

        top.geometry("+{}+{}".format(x, y))

        label = tk.Label(top,text=message)
        label.bind('<Configure>' , lambda e: label.config(wraplength=top.winfo_width()-10))
        label.grid()

        entry = AutocompleteCombobox(top,width=30,completevalues=lista)
        entry.grid()

        def save_and_destroy():
            global value
            value = entry.get()
            top.destroy()

        button = tk.Button(top,text="OK",command=save_and_destroy)
        button.grid()

        top.bind("<Return>" , lambda event: save_and_destroy)

        top.wait_window()  # attendi che la finestra venga chiusa

        return value
    
    def choose_folder():
        global SONGS_PATH
        SONGS_PATH = filedialog.askdirectory()
        songs.clear()
        GUI_Thread.get_songs()
        GUI_Thread.write_textbox()
        button_2.configure(state="normal")

class Logic_Thread(threading.Thread):

    def __init__(self, stop_event):
        super().__init__()
        self.stop_event = stop_event

    def run(self):
        while not self.stop_event.is_set():
            Logic_Thread.sortSongs()
    
    def stop_thread(self):
        self.stop_event.set()
    
    def sortCustom(songs):
        """
        Ordina un array di canzoni in modo che non ci siano due canzoni dello stesso artista in sequenza.
        """
        global count

        random.shuffle(songs)  # mischia le canzoni in modo casuale
        sorted_songs = []
        last_artist = None

        count = 0

        # Controllo se l'array di canzoni contiene solo canzoni dello stesso artista
        artists = set([Logic_Thread.searchInJson(song) for song in songs])
        if len(artists) == 1:
            return songs

        for song in songs:
            current_artist = Logic_Thread.searchInJson(song)
            if last_artist != current_artist:
                sorted_songs.append(song)
                last_artist = current_artist
            else:
                random.shuffle(songs)
                return Logic_Thread.sortCustom(songs)

            count += 1
            songArray = "italiane"
            if(songs == songsSTR):
                songArray = "straniere"

            GUI_Thread.labelProgressUpdate("Sto ordinando le canzoni " + songArray + ": ", len(songs) , count)
        return sorted_songs


    def searchArtist(author):
        print("Searching artist..." , author)
        time.sleep(2)  # NECESSARIO
        # Imposta il tuo User-Agent
        mb.set_useragent("Ordinamento_Canzoni", "0.1")
        # Esegui la ricerca dell'artista
        result = mb.search_artists(author, area="Italy")
        if not result["artist-list"]:
            result = mb.search_artists(author)
        # Recupera le informazioni sull'artista utilizzando il primo risultato della ricerca
        artist_id = result["artist-list"][0]["id"]
        artist_info = mb.get_artist_by_id(artist_id)

        return artist_info['artist']

    def searchInJson(string,fileName=fileJson):
        """
        Cerca nel file json se è presente l'autore
        """
        file = open(fileName)
        data = json.load(file)
        index = 0
        ftArray = ["ft.","Ft.","FT.","fT.","Feat.","feat.","FEAT.","fEAT.","Featuring","featuring","FEATURING"]

        # Normalize the input string
        normalized_string = re.sub('[^0-9a-zA-Z]+',' ',string.lower()).replace(" ", "")

        # Try to match the normalized string to the artist names in the JSON file
        for i in data["artists"]:
            ft_element = [ele for ele in ftArray if(ele in i)]
            if bool(ft_element):
                if fuzz.partial_ratio(re.sub('[^0-9a-zA-Z]+',' ',i["name"].lower()).replace(" ", ""), normalized_string) >= 85:
                    return index
            else:
                if fuzz.partial_ratio(re.sub('[^0-9a-zA-Z]+',' ',i["name"].lower()).replace(" ", ""), normalized_string) >= 85:
                    return index
            index += 1

        return -1
    
    def addArtistToJson(name,country,fileName=fileJson):
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
        if artist == None or artist == "":
            artist = audiofile.tag.artist

        if not audiofile.tag:
            audiofile.initTag()

        file = open(fileJson)
        data = json.load(file)

        if(artist == None or artist == ""):
            filenametemp = os.path.basename(inputtemp)
            index = Logic_Thread.searchInJson(filenametemp)
            if index != -1:
                audiofile.tag.artist = data["artists"][index]["name"]
            else:    
                print("Sono qui: " + audiofile.tag.artist)
                artist = GUI_Thread.pop_up_input("Per favore inserisci il nome dell'artista per questa canzone (" + filenametemp + "): ") 
                while artist == "":
                    artist = GUI_Thread.pop_up_input("Per favore inserisci il nome dell'artista per questa canzone (" + filenametemp + "): ")
                audiofile.tag.artist = Logic_Thread.searchArtist(artist)["name"]
            audiofile.tag.save()
            index = Logic_Thread.searchInJson(inputtemp)
        else:
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
                while artist == "":
                    artist = GUI_Thread.pop_up_input("Chiedo scusa, non ho trovato nessun artista con questo nome(" + artistInputTemp + ") per questa canzone (" + filenametemp +  "), riprova: ")
                artistInputTemp = artist
                artist = Logic_Thread.searchArtist(artist)

                if artist is not None:
                    audiofile.tag.artist = artist
                    audiofile.tag.save()

            if 'area' not in artist:
                answ = GUI_Thread.pop_up_area(artist["name"])
                while answ != 'i' and answ != 's' :
                    answ = GUI_Thread.pop_up_area(artist["name"])
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

        button_1.configure(state="disabled")
        button_2.configure(state="disabled")

        songs.clear()
        GUI_Thread.get_songs()

        count = 0

        for song in songs:
            count += 1
            GUI_Thread.labelProgressUpdate("Analizzando le canzoni: " , len(songs) , count)
            Logic_Thread.storeArtists(song)

        if len(songsITA) == 0 and len(songsSTR) == 0:
            print("Nessuna canzone trovata")
            GUI_Thread.pop_up("Nessuna canzone trovata", "Attenzione!")
            return

        print("Shuffling songsITA")
        count = 0
        songsITA = Logic_Thread.sortCustom(songsITA)

        print("Shuffling songsSTR")
        count = 0
        songsSTR = Logic_Thread.sortCustom(songsSTR)

        songs.clear()
        
        i = 0
        j = 0

        while i < len(songsITA) and j < len(songsSTR):
            songs.append(songsITA[i])
            i += 1
            songs.append(songsSTR[j])
            j += 1

        while i < len(songsITA):
            songs.append(songsITA[i])
            i += 1
        
        while j < len(songsSTR):
            songs.append(songsSTR[j])
            j += 1
            

        count = 0
        pref = 1
        for filename in songs:
            f = filename
            fileName = os.path.basename(f)
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

        button_2.configure(state="normal")
        button_1.configure(state="normal")

        songs.clear()
        GUI_Thread.get_songs()
        songs.sort(reverse=True)
        GUI_Thread.write_textbox()

        labelProgress.configure(text="Operazione completata!")

# MAIN
while not connect():
    GUI_Thread.pop_up("Nessuna connessione a internet!" , "Errore")

# Ricava il percorso della directory in cui si trova il file eseguibile
exe_dir = os.path.dirname(os.path.abspath(__file__))

# Crea il percorso completo del file "artists.json"
artists_path = os.path.join(exe_dir, fileJson)

if not os.path.exists(artists_path):
    with open(artists_path, "w", encoding="utf-8") as f:
        json.dump({"artists": []}, f)

stop_event = threading.Event()

gui = GUI_Thread(stop_event)
logic = Logic_Thread(stop_event)

gui.start()
logic.start()

def on_closing():
    stop_event.set()
    app.quit()