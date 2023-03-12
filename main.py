import os
import random
from tkinter import Tk
from tkinter.filedialog import askdirectory

path = askdirectory(title = "Seleziona la cartella da cui prendere i file")
print("Percorso:")
print(path)