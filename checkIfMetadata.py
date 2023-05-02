import os
import eyed3
import eyed3

SONGS_PATH = "Prova/"
ext = ".mp3"

for filename in os.listdir(SONGS_PATH):
    f = os.path.join(SONGS_PATH , filename)
    # checking if it is a file
    if not (os.path.isfile(f)) and f.endswith(ext):
        print(f + " not a file")
    else:
        audiofile = eyed3.load(f)
        if audiofile.tag.artist is None:
            artist = input("Per favore inserisci il nome dell'artista per questa canzone (%s): " %os.path.splitext(f)[0].split("/")[1])
            audiofile.tag.artist = artist
            audiofile.tag.save()
        else:
            print(audiofile.tag.artist)
