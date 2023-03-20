import os
import random
from tkinter import Tk
from tkinter.filedialog import askdirectory

# Definisci il percorso della cartella delle canzoni
#SONGS_PATH = askdirectory(title = "Seleziona la cartella da cui prendere i file")
SONGS_PATH = "Prova/"
ext = ".txt"
prefix = "0"
i = 1
# Definisci la lista delle canzoni
for filename in os.listdir(SONGS_PATH):
    f = os.path.join(SONGS_PATH , filename)
    # checking if it is a file
    if os.path.isfile(f) and f.endswith(ext):
        #print(os.path.splitext(f))
        fileName = os.path.splitext(f)[0].split("- ")[1]
        
        old_name = os.path.splitext(f)[0] + ext
        
        if(i < 10):
            new_name = SONGS_PATH + prefix + prefix + str(i) + "_" +  fileName + ext
        elif(i < 100):
            new_name = SONGS_PATH + prefix + str(i) + "_" + fileName + ext
        else: # MASSIMO DI 999 FILE
            new_name = SONGS_PATH + str(i) + "_" +  fileName + ext
        os.rename(old_name, new_name)
        i += 1