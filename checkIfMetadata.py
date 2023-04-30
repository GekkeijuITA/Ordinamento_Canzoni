import os
from tinytag import TinyTag
import eyed3

SONGS_PATH = "Prova/"
ext = ".mp3"

for filename in os.listdir(SONGS_PATH):
    f = os.path.join(SONGS_PATH , filename)
    # checking if it is a file
    if not (os.path.isfile(f)) and f.endswith(ext):
        print(f + " not a file")
    else:
        if(TinyTag.get(f).artist == None):
            print(f)
