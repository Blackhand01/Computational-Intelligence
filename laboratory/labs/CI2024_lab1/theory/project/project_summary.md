Ecco le informazioni riguardanti il progetto di regressione simbolica, basate sulle fonti fornite:

**Obiettivo del Progetto**

*   L'obiettivo principale del progetto è di creare un sistema che, dati dei punti di dati *X* e *Y*, sia in grado di trovare una formula matematica che li colleghi. Questo processo è definito **regressione simbolica**.
*   Il sistema deve leggere i dati forniti e produrre un'**espressione simbolica** come risultato.
*   La funzione finale deve accettare un array NumPy e restituire un array NumPy, utilizzando **solo le funzioni di NumPy**.
*   La formula finale deve essere efficiente e facilmente valutabile.

**Implementazione e Funzionalità**

*   Il progetto richiede la creazione di una funzione `f` che prende in input un array NumPy e restituisce un array NumPy. Questa funzione deve implementare la formula trovata per la regressione simbolica.
*   È possibile usare tutte le funzioni e gli elementi forniti da NumPy per creare il programma. NumPy supporta tutti gli operatori standard ed è in grado di effettuare valutazioni in parallelo.
*   Non è consentito l'uso di librerie esterne a meno che non si specifichi il loro uso e se ne conosca perfettamente il funzionamento interno.
*   La formula finale deve essere autonoma, senza dipendere da librerie esterne, con le eccezioni dette.
*   Le funzioni devono essere scritte in modo tale da poter essere valutate utilizzando NumPy in modo rapido.
*   L'evaluazione della formula non deve essere eccessivamente costosa dal punto di vista computazionale.
*   La formula finale deve essere una sola formula NumPy, anche se lunga, e non può contenere cicli `while`.
*   Si possono utilizzare tecniche di programmazione genetica, algoritmi genetici cartesiani, o qualsiasi altro metodo visto in classe.
*   Il codice può essere anche molto lungo, ma è meglio se non ha un'eccessiva complessità.
*   Il codice deve essere **originale**, se si utilizza codice di terzi, è necessario dichiararlo nel report.
*  È consentito lavorare in gruppo, ma ogni membro deve essere in grado di spiegare ogni singola linea di codice prodotta dal gruppo.

**Dati di Input**

*   Verranno forniti diversi problemi con variabili e punti di dati (coppie *X* e *Y*).
*   Alcuni problemi saranno tratti dalla fisica, altri da casi reali, alcuni creati e altri potrebbero contenere rumore bianco, rendendo impossibile trovare una formula esatta.
*   I dati di training e di test sono generati con lo stesso processo, e si presume quindi che seguano la stessa distribuzione, anche se non è garantito. Se il programma si basa su questa assunzione, è necessario specificarlo nel report.
*   I dati sono memorizzati in file `.npz`, che contengono sia `x` (un array NumPy multidimensionale) che `y` (il risultato).

**Consegna e Valutazione**

*   Ogni gruppo deve fornire un file per ogni problema di regressione simbolica, contenente la funzione creata, con un nome che segue il formato `S[ID_STUDENTE].py`, dove `[ID_STUDENTE]` è il numero identificativo dello studente.
*   All'interno del repository, dovrebbe esserci una directory `src` per il codice e una directory `data` per i dati, anche se l'inclusione dei dati è opzionale.
*   La scadenza per la consegna è **una settimana prima dell'esame ufficiale**, ovvero 168 ore prima dell'inizio ufficiale dell'esame.
*   La valutazione si basa sull'errore quadratico medio (MSE) sui punti di test, che sono il doppio dei punti utilizzati nel training.
*   Verrà confrontata la performance con dei punti di riferimento che sono simili a quelli usati dai partecipanti.
*   Durante l'esame, verranno esaminati il report e il codice per porre domande specifiche.
*   L'autenticità del lavoro verrà verificata, e l'uso non autorizzato di codice di terzi comporta l'annullamento del progetto e la necessità di rifarlo l'anno successivo.

**Report**

*   Il report deve essere un file **PDF privato** inviato via email al docente e al collaboratore.
*   Nel report si possono attribuire meriti ai propri colleghi.
*   Si deve utilizzare Markdown per strutturare il testo e includere il codice sorgente.
*   Non ci si deve preoccupare della dimensione del PDF.
*   Il report deve essere autonomo, senza dipendere da link esterni.
*   Il report deve descrivere le idee alla base del programma.

**Repository**

*   Il repository deve essere pubblico e chiamato `ci_2024_project_work`.
*   All'interno del repository deve esserci un file chiamato `S[ID_STUDENTE].py`, dove `[ID_STUDENTE]` è il numero identificativo.
*   Si consiglia di includere un file `README` con commenti per aiutare a comprendere il codice.

**Note Aggiuntive**

*   Il codice deve essere di proprietà di chi lo consegna.
*   Se si usa codice di terzi, bisogna dichiararlo nel report e conoscerne il funzionamento interno.

Spero che questo riassunto sia completo e chiaro. Se hai altre domande, non esitare a chiedere.
