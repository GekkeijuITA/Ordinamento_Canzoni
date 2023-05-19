# Ordinamento_Canzoni :it:
Programma per ordinare in modo casuale canzoni distinte alternando canzoni italiane e straniere, progetto per un amico</br>
Utilizzo di ambiente Anaconda python 3.9
## Come funziona
1. Nella schermata principale premere per prima cosa il tasto in alto "Scegli cartella con le canzoni da ordinare"
2. Una volta scelta la cartella il programma stamperà le canzoni trovate
3. Premere il bottone in basso "Ordina canzoni" per iniziare il processo di ordinamento
4. A volte, a causa del fatto che non si riesca a trovare l'origine dell'autore, il programma chiederà l'origine dell'autore, premere il tasto corrispondente
5. A volte invece chiede di inserire il nome dell'autore se non riesce a trovarlo tra quelli precedentemente salvati nel file denominato "artists.json"
6. Sopra al bottone "Ordina canzoni" sarà scritto cosa sta facendo il programma in quel momento
7. Una volta che ha completato l'operazione si troveranno le canzoni ordinate: italiane e straniere ordinate senza canzoni degli stessi autori vicini
## Informazioni aggiuntive
1. Se si vuole interrompere il processo è consigliabile farlo durante la fase di analisi dei file premendo la X in alto a destra (Windows) o in alto a sinistra (MacOs) (o in qualunque altro metodo disponibile per chiudere un'applicazione)
2. A causa dei termini di uso delle API di MusicBrainz(database utilizzato per determinare la nazionalità dell'autore) il programma ci metterà circa 3 secondi per canzone per la fase di analisi
3. Se si vuole cambiare l'origine dell'autore o il nome stesso, basta cercarlo nel file "artists.json" e modificarlo
    - Italy => italia , Foreign => straniero
# :warning: Attenzione :warning:
1. Il programma non è perfetto, potrebbe capitare che non riesca a trovare l'origine dell'autore corretto, in quel caso bisogna inserirla manualmente
2. Il programma non è perfetto, potrebbe capitare che non riesca a trovare il nome dell'autore corretto, in quel caso bisogna inserirlo manualmente
3. Se ci sono più canzoni straniere di quelle italiane (o viceversa), è possibile che il programma ordini più canzoni dello stesso autore oppure della stessa origine

# Song_Sorter :uk:
Program to randomly sort distinct songs while alternating between Italian and foreign songs, a project for a friend</br>
Using Anaconda python 3.9 environmen
## How it works
1. On the main screen, first press the button at the top "Choose folder with songs to sort"
2. Once the folder is selected, the program will display the songs found
3. Press the button at the bottom "Sort songs" to start the sorting process
4. Sometimes, due to the inability to find the author's origin, the program will ask for the author's origin, press the corresponding button
5. Sometimes it asks to enter the author's name if it cannot find it among those previously saved in the file called "artists.json"
6. Above the "Sort songs" button, it will be written what the program is currently doing
7. Once it has completed the operation, the sorted songs will be found: Italian and foreign sorted without songs from the same authors nearby
## Additional information
1. If you want to interrupt the process, it is advisable to do so during the file analysis phase by pressing the X in the top right (Windows) or top left (MacOs) (or in any other method available to close an application)
2. Due to the terms of use of the MusicBrainz API (database used to determine the author's nationality), the program will take about 3 seconds per song for the analysis phase
3. If you want to change the author's origin or name itself, simply search for it in the "artists.json" file and modify it
    - Italy => italia, Foreign => foreign

# :warning: Warning :warning:
1. The program is not perfect, it may happen that it cannot find the correct origin of the author, in that case it must be entered manually
2. The program is not perfect, it may happen that it cannot find the correct name of the author, in that case it must be entered manually
3. If there are more foreign songs than Italian ones (or vice versa), it is possible that the program sorts more songs by the same author or of the same origin.
