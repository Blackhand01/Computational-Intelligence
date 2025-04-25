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
