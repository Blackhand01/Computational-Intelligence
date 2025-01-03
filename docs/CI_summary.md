**Riassunto in italiano dei contenuti principali delle slide di Computational Intelligence**  

Di seguito troverai un riassunto dei temi affrontati nelle slide. La sezione **più rilevante per l’esame** è quella sul **Reinforcement Learning (RL)**, ma per completezza vengono riassunti anche gli altri argomenti principali.

---

## 1. **Algoritmi di Ricerca Locale (Local Search)**  
- **Caratteristiche**:  
  - Non sono esaustivi. Ricercano soluzioni migliorando iterativamente una configurazione iniziale.  
  - Esempio paradigmatico: _Gradient Descent_ (in ambito continuo) o _Hill Climbing_ (in spazi discreti).  
- **Punti chiave**:  
  - Nelle **NP-hard problem** (dove la ricerca esaustiva è inaccessibile) gli algoritmi di ricerca locale esplorano lo spazio delle soluzioni mediante “mosse locali”, ovvero piccole modifiche (neighboring solutions).  
  - **Hill Climbing**, _Simulated Annealing_, _Tabu Search_ e _Iterated Local Search_ sono esempi di tecniche euristiche popolari.  
  - Si impiegano in problemi di ottimizzazione come l’_8 Queens Problem_, la pianificazione di orari (University Timetable) o i _Knapsack problems_.

---

## 2. **Ottimizzazione Evolutiva (Evolutionary Computation)**  
- **Fondamenti**:
  - Prende spunto da meccanismi biologici (selezione naturale, mutazione, crossover, ecc.).  
  - Si parte da una popolazione di soluzioni candidate (individui), si applicano operatori genetici per generare nuove soluzioni (offspring) e si decide chi sopravvive tra genitori e figli (survivor selection).  
- **Varianti principali**:
  - **Genetic Algorithms (GA)**: soluzioni rappresentate spesso con stringhe di bit.  
  - **Evolution Strategies (ES)**: focalizzate su ottimizzazione di parametri reali (Gaussiana come mutazione, “1/5 success rule”).  
  - **Evolutionary Programming (EP)**: inizialmente su macchine a stati finiti, poi generalizzato; spesso non usa crossover.  
  - **Genetic Programming (GP)**: evolve alberi sintattici (programmi) per eseguire compiti quali _symbolic regression_.  
  - **Differential Evolution (DE)** e **Particle Swarm Optimization (PSO)**: orientate all’ottimizzazione di vettori in \(\mathbb{R}^n\).  
- **Multi-Obiettivo (MOEA)**:
  - Obiettivi multipli potenzialmente in conflitto (es. velocità vs. costo).  
  - Uso del concetto di **Pareto optimality** e metodi per preservare la diversità (archivi di soluzioni non-dominated).  

---

## 3. **Reinforcement Learning (RL)**  
Questa è la sezione più importante per l’esame.

### 3.1 Introduzione e Concetti di Base
- **Definizione**:  
  Un agente apprende come comportarsi in un ambiente interagendo con esso, ricevendo ricompense (reward) scalari per le sue azioni. L’obiettivo è massimizzare il ritorno cumulato (somma delle ricompense, spesso scontate nel tempo).
- **Episodico vs. Continuo**:  
  - _Episodico_: ogni episodio inizia in uno stato e termina in uno stato terminale.  
  - _Continuo_: potenzialmente non c’è un “fine episodio” (l’ambiente non termina).
- **Markov Decision Process (MDP)**:  
  - Ambiente formalizzato come MDP, dove uno stato \(s\) contiene tutte le informazioni rilevanti in modo che “il futuro sia indipendente dal passato se noto il presente” (proprietà di Markov).  
  - L’agente sceglie un’azione \(a\), e con una certa probabilità transisce nello stato successivo \(s'\) e riceve una ricompensa \(r\).  
  - L’agente è descritto da una _policy_ \(\pi\), che può essere deterministica (\(\pi(s)=a\)) o stocastica (\(\pi(a|s)\)).

### 3.2 Value Function e Bellman Equations
- **State-Value Function \(v_\pi(s)\)**:  
  Valore atteso (expected return) partendo dallo stato \(s\) e seguendo la policy \(\pi\).
- **Action-Value Function \(q_\pi(s,a)\)**:  
  Valore atteso partendo dallo stato \(s\), eseguendo l’azione \(a\) e poi proseguendo secondo \(\pi\).
- **Bellman Equation**:  
  Relaziona il valore di uno stato all’attuale ricompensa più il valore (scontato) degli stati futuri. Forme principali:  
  \[
    v_\pi(s) = \mathbb{E}[\,r + \gamma\,v_\pi(s') \mid s,\,\pi\,].
  \]  
  - Ci sono versioni “optimal” per trovare \(v_*\) e \(q_*\).

### 3.3 Approcci Principali
1. **Dynamic Programming (DP)**:  
   - Necessita di un _modello_ dell’ambiente (transizioni e ricompense note).  
   - _Policy Iteration_ e _Value Iteration_ permettono di calcolare la policy ottima usando aggiornamenti iterativi (Bellman backups).
2. **Monte-Carlo (MC)**:  
   - Non necessita del modello, impara solo da episodi completi.  
   - Stima il valore di uno stato (\(v(s)\)) come media dei ritorni osservati quando si visita quello stato.
   - Funziona bene con episodi che terminano, ma deve attendere la fine dell’episodio per aggiornare le stime.
3. **Temporal-Difference (TD) Learning**:
   - Combina idee di DP e MC.  
   - Aggiorna stime di valore a ogni step (bootstrapping) usando un target parziale basato su \(v(s')\).  
   - Metodi popolari: **TD(0)**, **SARSA** e **Q-Learning**.  

### 3.4 On-Policy e Off-Policy
- **On-Policy (es. SARSA)**:  
  - L’agente apprende la funzione \(q_\pi(s,a)\) mentre segue la policy \(\pi\).  
  - Esempio: _SARSA_ aggiorna \(q\) usando la tripla \((s,a,r)\) e la successiva coppia \((s',a')\) con \(\varepsilon\)-greedy, così mantiene coerenza tra policy di comportamento e di valutazione.
- **Off-Policy (es. Q-Learning)**:  
  - L’agente apprende \(q_*(s,a)\) (relativo alla policy ottima) mentre segue una policy di esplorazione potenzialmente diversa (ad esempio \(\varepsilon\)-greedy).  
  - Esempio: _Q-Learning_ aggiorna  
    \[
      Q(s,a) \leftarrow Q(s,a) + \alpha \Big(r + \gamma \max_{a'} Q(s',a') - Q(s,a)\Big).
    \]  
  - È robusto e non ha bisogno di utilizzare la stessa policy di valutazione e di comportamento.

### 3.5 Altri Concetti Importanti
- **Esplorazione vs. Sfruttamento (Exploration vs. Exploitation)**:  
  - È fondamentale bilanciare il tentativo di “provare nuove azioni” (esplorazione) con il concentrarsi sulle azioni ritenute migliori (sfruttamento).
  - Strategie come \(\varepsilon\)-greedy gestiscono questo trade-off in modo semplice, riducendo gradualmente \(\varepsilon\).
- **Bias e Varianza in MC vs. TD**:  
  - MC ha stime non viziate ma con varianza alta;  
  - TD è più “biased” (perché “bootstrappa” da stime parziali) ma ha solitamente varianza minore e impara più velocemente nel caso Markoviano.
- **Applicazioni**:  
  - Giochi (Backgammon, Go, Atari) e problemi di controllo (robotica, gestione portafogli, network scheduling, ecc.).

---

## 4. **Altri Argomenti Principali**
- **Ricerca di Cammini (Path Search)**: _Breadth-First Search_, _Depth-First Search_, _Uniform-Cost Search_, _A\*_, ecc.  
- **Goal Trees & Problem Solving**: decomposizione di un problema complesso in sotto-obiettivi e regole esperte.  
- **Sistemi Esperti (Expert Systems)**: conoscenza codificata in regole di inferenza (if-then). Ora spesso superati in molti contesti da metodi di Machine Learning più flessibili.  
- **Genetic Programming (GP)**: specializzazione dei GA per evolvere strutture ad albero (programmi). Usato specialmente in “symbolic regression” o per generare codice in vari linguaggi.  
- **Diversity in Evolutionary Algorithms**: strategie per evitare la convergenza prematura (crowding, fitness sharing, nicchie, ecc.).  

---

## 5. **Consigli Finali e Conclusioni**
1. **Focalizzati sul RL**: comprendi bene l’impostazione MDP (stati, azioni, transizioni, ricompense), il concetto di policy e la differenza fra metodi on-policy e off-policy.  
2. **Conosci i Bellman Equations**: saper derivare e interpretare l’aggiornamento della funzione valore (o action-value) è cruciale.  
3. **Sapere differenziare** fra DP, MC e TD e i rispettivi pro/contro.  
4. **Ricordare** che l’esplorazione è essenziale: \(\varepsilon\)-greedy è la strategia più semplice, ma esistono alternative più sofisticate.  
5. **Algoritmi evolutivi**: conoscere almeno a grandi linee GA, ES, EP, GP, DE, PSO e i concetti base (crossover, mutazione, selezione, fitness).  

Questo riassunto copre i concetti chiave delle slide. Per l’esame, è importante soprattutto capire gli **schemi di aggiornamento (update)** di Monte-Carlo, SARSA e Q-Learning, oltre che saper spiegare bene la differenza tra **on-policy** e **off-policy** e come funziona la **stima delle funzioni valore** (state-value e action-value). Buono studio!

Ecco un riassunto completo delle fonti fornite, organizzato per argomento principale:

**Apprendimento per Rinforzo (Reinforcement Learning - RL)**

*   **Concetti di base:** L'apprendimento per rinforzo riguarda un agente che impara a interagire con un ambiente per massimizzare una ricompensa cumulativa. Gli ambienti sono spesso formalizzati come **Processi Decisionali di Markov (MDP)**, caratterizzati da stati, azioni, transizioni e ricompense. Un **MDP** è completamente osservabile e la proprietà di Markov stabilisce che lo stato successivo dipende solo dallo stato attuale e dall'azione eseguita. L'agente è guidato da una **policy**, che può essere deterministica o stocastica.
*   **Funzioni di valore:** La **funzione di valore dello stato** *V(s)* rappresenta il valore atteso della ricompensa cumulativa a partire dallo stato *s*, seguendo una certa policy. La **funzione di valore dell'azione** *Q(s, a)* rappresenta il valore atteso della ricompensa cumulativa eseguendo l'azione *a* nello stato *s*.
*   **Equazioni di Bellman:** Le equazioni di Bellman esprimono la relazione ricorsiva tra i valori degli stati. L'equazione per il valore ottimale di uno stato *V*(s)* è  *V*(s) = max\_a \[R(s, a) + γ ∑\_s' P(s' | s, a) V*(s') ].
*   **Algoritmi di RL:**
    *   **Programmazione Dinamica (DP):** Richiede un modello dell'ambiente ed utilizza *Value Iteration* e *Policy Iteration* per calcolare la policy ottimale.
    *   **Monte Carlo (MC):** Non richiede un modello, impara da episodi completi. Stima il valore di uno stato come media dei ritorni osservati quando si visita quello stato. Esistono varianti come *First-Visit MC* e *Every-Visit MC*.
    *   **Temporal Difference (TD):** Combina idee di DP e MC, aggiorna le stime dei valori a ogni step (bootstrapping). Il metodo principale è *TD(0)*.
    *   **SARSA:**  Un metodo *on-policy* che apprende la funzione *Q* mentre segue la policy.
    *   **Q-Learning:** Un metodo *off-policy* che cerca di apprendere la funzione di valore d'azione ottimale *Q*(s,a)* senza seguire una policy specifica.
*   **Esplorazione vs. Sfruttamento:** Un trade-off importante da gestire, spesso tramite strategie come la politica ε-greedy.
*   **Bias vs. Varianza:** MC ha stime non distorte ma con alta varianza, mentre TD introduce bias ma ha varianza minore.
*   **Applicazioni:** Giochi, robotica, gestione di portafogli.

**Algoritmi di Ricerca Locale**

*   Questi algoritmi migliorano iterativamente una soluzione tramite piccole modifiche, adatte a problemi NP-hard.
*   Esempi: *Hill Climbing*, *Simulated Annealing*, *Tabu Search* e *Iterated Local Search*.

**Ottimizzazione Evolutiva (Evolutionary Computation - EC)**

*   Si ispira ai meccanismi biologici per trovare soluzioni a problemi di ottimizzazione.
*   Algoritmi principali:
    *   **Algoritmi Genetici (GA):** Utilizzano stringhe di bit per rappresentare le soluzioni.
    *   **Strategie Evolutive (ES):** Ottimizzano parametri reali, spesso con mutazioni gaussiane.
    *   **Programmazione Evolutiva (EP):** Utilizza macchine a stati finiti, non sempre con crossover.
    *   **Programmazione Genetica (GP):** Evolve alberi sintattici (programmi) per compiti come la *regressione simbolica*.
    *   **Differential Evolution (DE):** Ottimizza vettori reali utilizzando crossover uniforme e mutazione differenziale.
    *   **Particle Swarm Optimization (PSO):** Simula il comportamento di uno sciame per trovare soluzioni.
*  **Multi-Obiettivo (MOEA):** Gestisce più obiettivi in conflitto usando il concetto di Pareto optimality.
*   La diversità è importante per evitare la convergenza prematura e si utilizzano tecniche come il *niching*.

**Minimax e Algoritmi di Gioco**

*   L'algoritmo **Minimax** è usato in giochi a due giocatori con informazione perfetta e somma zero, con l'obiettivo di minimizzare la perdita nel caso peggiore. Il *massimizzatore* cerca di massimizzare il proprio punteggio mentre il *minimizzatore* cerca di minimizzare il punteggio del massimizzatore.
*   La **potatura Alpha-Beta** è un'ottimizzazione di Minimax che riduce il numero di nodi valutati nell'albero di gioco.
*   I limiti di Minimax sono lo spazio degli stati e il fattore di ramificazione. Si usano quindi tecniche come le *funzioni di valutazione euristiche*, la *memorizzazione degli stati* e *database di aperture e finali*.
*   Esempi di applicazioni sono *Deep Blue* per gli scacchi e *AlphaGo* per il Go.

**Regressione Simbolica**

*   L'obiettivo è trovare una formula matematica che colleghi un input *X* ad un output *Y*.
*   La formula deve essere implementata con NumPy e deve essere efficiente, usando solo le funzioni disponibili in NumPy.
*   Le formule vengono valutate usando l'errore quadratico medio (MSE) su un set di test.

**Learning Classifier Systems (LCS)**

*   I sistemi LCS combinano l'apprendimento per rinforzo con algoritmi genetici per evolvere set di regole condizionali.
*   Le regole hanno una condizione e un'azione, che evolvono tramite algoritmi genetici.
*   Esistono due stili: Michigan e Pittsburgh.

**Altri Argomenti**

*   **Algoritmi di Ricerca di Cammini**: Breadth-First Search, Depth-First Search, Uniform-Cost Search, A*.
*   **Sistemi Esperti:** Conoscenza codificata in regole di inferenza (if-then).
*   **Logica Fuzzy**: Utile per gestire informazioni imprecise e vaghe, a differenza della probabilità che si occupa di incertezza.
*  **Diversità negli Algoritmi Evolutivi**: Tecniche per evitare la convergenza prematura.

**Dettagli sul Progetto**

*   Il progetto consiste nel creare un sistema di regressione simbolica che prende un array NumPy in input e restituisce un array NumPy in output, usando solo le funzioni NumPy.
*   Ogni gruppo deve fornire un file `.py` per ogni problema di regressione simbolica.
*   Il codice deve essere originale e comprensibile, con possibilità di utilizzare librerie esterne ma con piena conoscenza del loro funzionamento.
*   Il report deve essere in PDF, includere il codice sorgente e descrivere le idee alla base del programma.
*   La scadenza è 168 ore prima dell'esame ufficiale.
*   I dati sono generati in modo che training e test abbiano caratteristiche simili.
*   Le presentazioni sono parte integrante del corso.

Spero che questo riassunto completo sia utile. Ho evidenziato in **grassetto** i punti più rilevanti per facilitarne la comprensione.
