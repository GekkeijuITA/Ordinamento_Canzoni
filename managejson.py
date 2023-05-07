import json
import tkinter as tk
from ttkwidgets.autocomplete import AutocompleteCombobox

lista = []

file = open("artists.json")
data = json.load(file)
for i in data["artists"]:
    lista.append(i["name"])


def pop_up_input(message):
    global value

    top = tk.Toplevel(root)
    top.geometry("100x100")
    top.title("Attenzione!")
    tk.Label(top, text=message).grid()

    entry = AutocompleteCombobox(top, width=30, completevalues=lista)
    entry.grid()

    def getEntryValue():
        return entry.get()
    
    def save_and_destroy():
        global value
        value = getEntryValue()
        top.destroy()

    button = tk.Button(top, text="OK", command=save_and_destroy)
    button.grid()

    top.bind("<Return>", lambda event: save_and_destroy)

    top.wait_window()  # attendi che la finestra venga chiusa

    return value


def addArtistToJson(name, country, fileName="artists.json"):
    with open(fileName, 'r+') as file:
        file_data = json.load(file)
        alreadyIn = False
        for tuple in file_data["artists"]:
            if tuple["name"] == name:
                alreadyIn = True
                break
        if not alreadyIn:
            file_data["artists"].append({"name": name, "area": country})
            file.seek(0)
            json.dump(file_data, file, indent=4, ensure_ascii=False)


root = tk.Tk()
root.geometry("400x300")

frame = tk.Frame(root)
frame.pack(expand=True)

print(pop_up_input("Scrivi un autore"))

root.mainloop()
