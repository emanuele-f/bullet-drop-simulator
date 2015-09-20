# bullet-drop-simulator
Un progetto per la simulazione fisica del moto dei proiettili.
Il simulatore è scritto in Python 2 ed utilizza la libreria wxPython 3 per la gestione del contenuto grafico.

Features
--------
- Impostare singolarmente i valori di velocità iniziale, angolo di lancio, gittata massima e gittata corrente
- Aggiungere ed eliminare ostacoli, controllandone la coordinata
- Visualizzazione in tempo reale dei dati della simulazione e della traiettoria del proiettile
- Calcolo automatico di velocità iniziale e angolo di lancio per la data gittata, impostabile anche graficamente tramite click
- In presenza di ostacoli, calcola velocità iniziale e angolo di lancio per la data gittata in modo da evitarli

Installazione
-------------
Il simulatore gira in ambiente Linux/Mac/Windows direttamente da sorgente, previa installazione e setup dell'ambiente python e della libreria wxPython.

Si rimanda ai siti ufficiali:

- https://www.python.org/
- http://www.wxpython.org/

In alternativa, limitatamente al sistema operativo Windows, saranno disponibili a breve eseguibili standalone, avviabili anche senza ambiente python.

Miglioramenti
-------------
Segue la lista di alcuni miglioramenti che potrebbero essere apportati in futuro:
- Calcolo automatico di velocità e angolo per la data gittata in presenza di ostacoli "fluttuanti". Il problema sembra
  richiedere l'utilizzo di strumenti di risoluzione di sistemi di disequazioni lineari più gestione OR logico:
  Per ogni ostacolo, si devono considerare i due punti superiori (2 disequazioni) e i due inferiori
  tenendo conto della possibilità che il vertice della parabola possa "appartenervi" (3 disequazioni + OR)
- Generalizzazione delle formule in modo indipendente dal punto iniziale, permettendo di fare lanci sia "avanti" che "indietro"
- Utilizzo di immagini da animare in sostituzione alle primitive grafiche per la rappresentazione degli oggetti
