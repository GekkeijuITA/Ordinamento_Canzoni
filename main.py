import os
import random
from tkinter import Tk
from tkinter.filedialog import askdirectory

def shuffle(array):
    random.shuffle(array)
    return array

# Definisci il percorso della cartella delle canzoni
#SONGS_PATH = askdirectory(title = "Seleziona la cartella da cui prendere i file")
SONGS_PATH = "Prova/"
ext = ".txt"
i = 1
songs = []
# Definisci la lista delle canzoni
for filename in os.listdir(SONGS_PATH):
    f = os.path.join(SONGS_PATH , filename)
    # checking if it is a file
    if os.path.isfile(f) and f.endswith(ext):
        songs.append(f)

if len(songs) == 0:
    print("Nessuna canzone trovata")
    exit()

songs = shuffle(songs)

for filename in songs:
    #f = os.path.join(SONGS_PATH , filename)
    f = filename
    #print(os.path.splitext(f))
    fileName = os.path.splitext(f)[0].split("/")[1]

    if(i < 10):
        newPrefix = "py" + "00" + str(i)
    elif(i < 100):
        newPrefix = "py" + "0" + str(i)
    else: # MASSIMO DI 999 FILE
        newPrefix = "py" + str(i)

    old_name = os.path.splitext(f)[0] + ext

    if("py" in fileName):
        fileName = fileName.split("_")[1]

    new_name = SONGS_PATH + newPrefix + "_" + fileName + ext

    os.rename(old_name, new_name)
    i += 1