import os
import random
import re
from tkinter import Tk
from tkinter.filedialog import askdirectory

def shuffle(array):
    random.shuffle(array)
    return array



# Define songs's folder path
#SONGS_PATH = askdirectory(title = "Seleziona la cartella da cui prendere i file")
SONGS_PATH = "Prova/"
ext = ".txt"
key = "py"
divisor = "%"
i = 1
songs = []

# Define songs list
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
    f = filename
    fileName = os.path.splitext(f)[0].split("/")[1]

    # Split fileName into old prefix and rest of file name
    if divisor in fileName:
        oldPrefix, restName = fileName.split(divisor, maxsplit=1)
    else:
        oldPrefix, restName = "", fileName


    if(i < 10):
        newPrefix = key + "00" + str(i)
    elif(i < 100):
        newPrefix = key + "0" + str(i)
    else: # MAX 999 FILES
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