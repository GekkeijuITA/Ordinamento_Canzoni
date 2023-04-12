import os
from tinytag import TinyTag

SONGS_PATH = "Canzoni/"
ext = ".mp3"

for filename in os.listdir(SONGS_PATH):
    f = os.path.join(SONGS_PATH , filename)
    # checking if it is a file
    if not (os.path.isfile(f) and f.endswith(ext)):
        print(f + " not a file")
    else:
        if(TinyTag.get(f).artist == None):
            print("Not every files has metadata: (" + f + ")")
            exit
        else:
            print(TinyTag.get(f).artist)
