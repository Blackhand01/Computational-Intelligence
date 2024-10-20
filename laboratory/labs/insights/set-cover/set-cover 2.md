# Problema del Set Cover: Confronto tra le versioni greedy e evolutiva

## Introduzione

Il **problema del Set Cover** (Set Cover Problem) è un problema di ottimizzazione combinatoria in cui si ha un universo di elementi e una collezione di sottoinsiemi di questo universo. L'obiettivo è trovare una combinazione minima di sottoinsiemi tale che l'unione di questi copra tutto l'universo. In questa analisi, confrontiamo due approcci per la risoluzione del problema del Set Cover:
1. **Soluzione greedy** (file `set-cover_gs1.py`).
2. **Algoritmo evolutivo** (file `set-cover_ea.py`).

Entrambi gli approcci utilizzano euristiche per cercare una soluzione ottimale o quasi-ottimale, ma con strategie diverse.

---

## Struttura del problema

### Parametri comuni

- **UNIVERSE_SIZE**: Dimensione dell'universo degli elementi.
- **NUM_SETS**: Numero totale di sottoinsiemi.
- **DENSITY**: Densità con cui gli elementi sono distribuiti nei sottoinsiemi.
  
In entrambi i casi, si utilizza `numpy` per generare casualmente i sottoinsiemi (matrice binaria dove ogni riga rappresenta un sottoinsieme) e un array di **costi** associati ai sottoinsiemi, calcolato come una funzione del numero di elementi nel sottoinsieme.

```python
SETS = np.random.random((NUM_SETS, UNIVERSE_SIZE)) < DENSITY
COSTS = np.pow(SETS.sum(axis=1), 1.1)
```

---

## Algoritmo Greedy (set-cover_gs1.py)

### Strategia

L'algoritmo greedy seleziona iterativamente il sottoinsieme che offre il miglior compromesso tra **numero di elementi coperti** e **costo**. Utilizza una metrica chiamata `pression` per favorire i sottoinsiemi che coprono più elementi scoperti. A ogni iterazione, il sottoinsieme che massimizza il rapporto tra utilità (elementi scoperti) e costo viene aggiunto alla soluzione.

### Punti chiave

- **Pressione**: Viene calcolata come una funzione esponenziale che aumenta con la rarità degli elementi.
  
```python
pression = 1 + np.exp(-10 * (availabe_sets.sum(axis=0) - 1))
```

- **Candidati utili**: Si selezionano solo i sottoinsiemi che contengono elementi non ancora coperti.

```python
useful_sets[:, np.logical_not(targets)] = np.False_
```

- **Criterio di selezione**: Il sottoinsieme con il miglior rapporto utilità/costo viene scelto.

```python
candidates = (useful_sets * pression).sum(axis=1) / weight
solution[candidates.argmax()] = np.True_
```

### Risultato

- **Progressione**: L'algoritmo greedy ha completato 10.000 iterazioni in circa un secondo, con una velocità di circa 5.271 iterazioni al secondo.
- **Costo finale**: Il costo totale della soluzione trovata è **108,685.13**.
- **Numero di chiamate alla funzione di costo**: Sono state effettuate **1.001 chiamate** alla funzione `cost`.

### Vantaggi

- **Efficienza computazionale**: L'algoritmo greedy è relativamente veloce, poiché si basa su una selezione iterativa immediata dei sottoinsiemi.
- **Deterministico**: Data la stessa inizializzazione, l'algoritmo produce sempre lo stesso risultato.

### Svantaggi

- **Soluzione subottimale**: L'approccio greedy non garantisce di trovare la soluzione ottimale globale, in quanto si basa su decisioni locali che non considerano interazioni future tra i sottoinsiemi selezionati.

---

## Algoritmo Evolutivo (set-cover_ea.py)

### Strategia

L'algoritmo evolutivo simula una **popolazione** di possibili soluzioni (genomi), dove ogni individuo rappresenta un possibile set di sottoinsiemi selezionati. Ogni individuo viene valutato sulla base di due criteri:
1. **Numero di elementi coperti**.
2. **Costo della soluzione**.

L'algoritmo evolutivo procede iterativamente applicando **selezione dei genitori**, **crossover** e **mutazione** per creare nuove soluzioni.

### Punti chiave

- **Individui**: Ogni individuo è un oggetto di classe `Individual`, che contiene un array binario (genoma) che rappresenta la selezione dei sottoinsiemi.

```python
@dataclass
class Individual:
    genome: np.ndarray
    fitness: float = None
```

- **Fitness**: La fitness di un individuo è calcolata come una funzione del numero di elementi coperti e del costo totale.

```python
def fitness(individual):
    return int(num_covered(individual.genome)), -float(cost(individual.genome))
```

- **Selezione dei genitori**: Viene eseguita su base torneo, dove i migliori due individui vengono scelti per la riproduzione.

```python
candidates = sorted(np.random.choice(population, 2), key=lambda e: e.fitness, reverse=True)
```

- **Crossover**: Viene eseguito un crossover tra due individui per generare nuovi individui.

```python
genome[m] = p2.genome[m]
```

### Risultato

- **Genoma della soluzione migliore**: L'algoritmo evolutivo ha trovato la soluzione con genoma **[True, False, False, True, True]**, selezionando tre sottoinsiemi su cinque disponibili.
- **Qualità della soluzione**: Anche se il costo finale non è esplicitato, la soluzione trovata copre l'intero universo con una configurazione ottimale rispetto ai criteri di selezione.

### Vantaggi

- **Ricerca globale**: L'algoritmo esplora lo spazio delle soluzioni in modo più ampio rispetto all'approccio greedy, aumentando la probabilità di trovare una soluzione migliore.
- **Adattabilità**: L'algoritmo può essere facilmente esteso con ulteriori operatori genetici o criteri di selezione.

### Svantaggi

- **Costo computazionale**: L'algoritmo evolutivo richiede più tempo di calcolo, poiché valuta molte soluzioni in parallelo e applica crossover e mutazioni a ogni iterazione.

---

## Confronto tra i due approcci

### 1. **Qualità della soluzione**
- L'algoritmo **greedy** ha trovato una soluzione rapida ma con un costo elevato di **108,685.13**.
- L'algoritmo **evolutivo** ha selezionato una configurazione ottimale di sottoinsiemi con genoma **[True, False, False, True, True]**, ma senza costo esplicito.

### 2. **Efficienza**
- L'algoritmo **greedy** è molto più efficiente in termini di tempo, completando le iterazioni in un tempo significativamente inferiore.
- L'algoritmo **evolutivo** richiede più tempo, ma è potenzialmente in grado di trovare soluzioni migliori.

### 3. **Robustezza**
- L'algoritmo **greedy** è deterministico e meno esplorativo, risultando meno robusto nella ricerca di soluzioni ottimali.
- L'algoritmo **evolutivo** è più flessibile e robusto, esplorando soluzioni diverse e bilanciando meglio esplorazione ed esploitazione.

---

## Conclusione

Il **problema del Set Cover** è un classico problema di ottimizzazione combinatoria. L'approccio **greedy** offre una soluzione rapida, ma con costi elevati, mentre l'**algoritmo evolutivo** esplora lo spazio delle soluzioni in modo più ampio, trovando soluzioni potenzialmente migliori, ma a un costo computazionale maggiore. A seconda delle esigenze del problema, la scelta tra i due approcci dipenderà dal compromesso tra tempo di calcolo e qualità della soluzione.