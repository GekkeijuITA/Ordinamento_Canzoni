# Ordinamento_Canzoni
Programma per ordinare in modo casuale canzoni distinte alternando canzoni italiane e straniere, progetto per un amico</br>
Utilizzo di ambiente Anaconda python 3.9
## Come funziona
1. Nella schermata principale premere per prima cosa il tasto in alto "Scegli cartella con le canzoni da ordinare"
2. Una volta scelta la cartella il programma stamperà le canzoni trovate
3. Premere il bottone in basso "Ordina canzoni" per iniziare il processo di ordinamento
4. A volte, a causa del fatto che non si riesca a trovare l'origine dell'autore, il programma chiederà l'origine dell'autore con "i" per italiano e "s" per straniero, bisogna digitare la singola lettera e non tutta la parola (italiano/straniero)
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