import customtkinter as ctk
import customtkinter
from customtkinter import filedialog
import os

SONGS_PATH_IT = ""
SONGS_PATH_STR = ""
ext = ".mp3"
songs_it = []
songs_str = []


# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("dark")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("600x480")
app.title("Ordinamento Canzoni")

frame_1 = customtkinter.CTkFrame(master=app)
frame_1.pack(pady=20, padx=60, fill="both", expand=True)

label_1 = customtkinter.CTkLabel( master=frame_1, justify=customtkinter.LEFT, text="Ordina canzoni", font=("Roboto", 24))
label_1.pack(pady=10, padx=10)

# SCELTA CANZONI
tabview_1 = customtkinter.CTkTabview(master=frame_1, width=200, height=70)
tabview_1.pack(pady=10, padx=10)
tabview_1.add("Canzoni Italiane")
tabview_1.add("Canzoni Straniere")

button_1 = customtkinter.CTkButton(master=tabview_1.tab("Canzoni Italiane"), command=button_callback_it, text="Scegli cartella per le canzoni italiane")
button_1.pack(pady=10, padx=10)

textbox_1 = customtkinter.CTkTextbox(tabview_1.tab("Canzoni Italiane"))
textbox_1.pack(pady=10, padx=10, fill="both", expand=True)

button_2 = customtkinter.CTkButton(master=tabview_1.tab("Canzoni Straniere"), command=button_callback_str, text="Scegli cartella per le canzoni straniere")
button_2.pack(pady=10, padx=10)

textbox_2 = customtkinter.CTkTextbox(tabview_1.tab("Canzoni Straniere"))
textbox_2.pack(pady=10, padx=10, fill="both", expand=True)

# SCELTA DESTINAZIONE, FUSIONE E ORDINAMENTO

app.mainloop()
