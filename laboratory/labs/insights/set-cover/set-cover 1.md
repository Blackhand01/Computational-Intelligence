# Problema del Set Cover

## Introduzione

Questo notebook affronta la risoluzione del **problema del Set Cover** (Set Cover Problem). Nel problema del Set Cover, si ha un insieme universo di elementi e una collezione di sottoinsiemi di questo universo. L'obiettivo è selezionare un sottoinsieme di questi sottoinsiemi in modo che ogni elemento dell'universo sia coperto da almeno uno dei sottoinsiemi selezionati, minimizzando al contempo il costo totale dei sottoinsiemi scelti.

La differenza tra file set-cover 1.1 e 1.2 è l'introduzione di un parametro di strength (forza) per controllare la probabilità di mutazione, che può essere regolata dinamicamente in base ai risultati della ricerca.
---
  
## Struttura del Notebook

### 1. Inizializzazione dei Dati

In questa sezione, vengono inizializzati i parametri e i dati necessari per il problema:

- **UNIVERSE_SIZE**: Dimensione dell'universo di elementi (1000 elementi).
- **NUM_SETS**: Numero totale di sottoinsiemi disponibili (200 sottoinsiemi).
- **DENSITY**: Densità di copertura degli elementi nei sottoinsiemi (10%).

```python
from itertools import accumulate
import numpy as np
from matplotlib import pyplot as plt
from icecream import ic

## Reproducible Initialization

# Se si desidera ottenere risultati riproducibili, utilizzare `rng` (e riavviare il kernel); per risultati non riproducibili, utilizzare `np.random`.
UNIVERSE_SIZE = 1000
NUM_SETS = 200
DENSITY = 0.1

rng = np.random.Generator(np.random.PCG64([UNIVERSE_SIZE, NUM_SETS, int(10_000 * DENSITY)]))
# DON'T EDIT THESE LINES!

SETS = np.random.random((NUM_SETS, UNIVERSE_SIZE)) < DENSITY
for s in range(UNIVERSE_SIZE):
    if not np.any(SETS[:, s]):
        SETS[np.random.randint(NUM_SETS), s] = True
COSTS = np.power(SETS.sum(axis=1), 1.1)
```

### 2. Funzioni di Supporto

#### `valid(solution)`

Verifica se una soluzione candidata copre l'intero universo.

```python
def valid(solution):
    """Verifica se la soluzione è valida (cioè copre tutto l'universo)"""
    phenotype = np.logical_or.reduce(SETS[solution])
    return np.all(phenotype)
```

#### `cost(solution)`

Calcola il costo totale di una soluzione candidata.

```python
def cost(solution):
    """Restituisce il costo di una soluzione (da minimizzare)"""
    return COSTS[solution].sum()
```

### 3. Algoritmi di Ottimizzazione

#### 3.1. Algoritmo di Random Hill Climber (RHMC)

L'algoritmo RHMC inizia con una soluzione casuale e, ad ogni iterazione, applica una mutazione multipla alla soluzione. Se la nuova soluzione è migliore (ovvero, ha un costo inferiore e copre l'intero universo), viene accettata.

##### 3.1.1. Funzioni di Mutazione

- **Multiple Mutation**: Applica una mutazione a più sottoinsiemi basata su una probabilità fissa (1%).

```python
def multiple_mutation(solution: np.ndarray) -> np.ndarray:
    mask = rng.random(NUM_SETS) < 0.01
    new_sol = np.logical_xor(solution, mask)
    return new_sol
```

##### 3.1.2. Funzione di Fitness

Valuta una soluzione candidata basandosi sulla sua validità e costo.

```python
def fitness(solution: np.ndarray):
    return (valid(solution), -cost(solution))
```

##### 3.1.3. Esecuzione dell'Algoritmo RHMC

Inizializza una soluzione casuale e applica iterativamente mutazioni, accettando solo quelle che migliorano la soluzione.

```python
solution = rng.random(NUM_SETS) < 0.3
solution_fitness = fitness(solution)
history = [float(solution_fitness[1])]
ic(fitness(solution))

tweak = multiple_mutation

for steps in range(10_000):
    new_solution = tweak(solution)
    f = fitness(new_solution)
    history.append(float(f[1]))

    if f > solution_fitness:
        solution = new_solution
        solution_fitness = fitness(solution)
        # ic(fitness(solution))

# ic(solution)
ic(fitness(solution))
plt.figure(figsize=(14, 8))
plt.plot(
    range(len(history)),
    list(accumulate(history, max)),
    color="red",
)
_ = plt.scatter(range(len(history)), history, marker=".")
```

#### 3.2. Algoritmo di RHMC Migliorato con Forza di Mutazione Dinamica

Questa versione introduce un meccanismo per adattare dinamicamente la probabilità di mutazione (`strength`) basato sui progressi dell'algoritmo, utilizzando un buffer per monitorare gli ultimi miglioramenti.

##### 3.2.1. Mutazione con Forza Dinamica

Modifica un numero variabile di sottoinsiemi basato su una probabilità regolabile.

```python
def multiple_mutation_strength(solution: np.ndarray, strength: float = 0.3) -> np.ndarray:
    mask = rng.random(NUM_SETS) < strength
    if not np.any(mask):
        mask[np.random.randint(NUM_SETS)] = True
    new_sol = np.logical_xor(solution, mask)
    return new_sol
```

##### 3.2.2. Esecuzione dell'Algoritmo Migliorato

Introduce un buffer per adattare la forza della mutazione in base ai miglioramenti recenti.

```python
strength = 0.5
buffer = list()
BUFFER_SIZE = 50

solution = rng.random(NUM_SETS) < 0.3
solution_fitness = fitness(solution)
history = [float(solution_fitness[1])]
ic(fitness(solution))

for steps in range(10_000):
    new_solution = multiple_mutation_strength(solution, strength)
    f = fitness(new_solution)

    history.append(float(f[1]))
    buffer.append(f > solution_fitness)
    buffer = buffer[-BUFFER_SIZE:]
    if sum(buffer) > 10:
        strength *= 1.1
    elif sum(buffer) < 10:
        strength /= 1.1

    if f > solution_fitness:
        solution = new_solution
        solution_fitness = fitness(solution)

ic(fitness(solution))

plt.figure(figsize=(14, 8))
plt.plot(
    range(len(history)),
    list(accumulate(history, max)),
    color="red",
)
_ = plt.scatter(range(len(history)), history, marker=".")
```

---
  
## Risultati

I risultati riportati rappresentano l'output di diverse esecuzioni degli algoritmi di ottimizzazione per il **problema del Set Cover**. Di seguito, vengono spiegati i risultati passo dopo passo.

### Risultati di **Random Hill Climber (RHMC) Senza Strength**:

1. **Prima esecuzione dell'algoritmo**:

    ```plaintext
    ic| valid(solution): np.True_
        cost(solution): np.float64(31699.621793222723)
    ```

    - **Validità della soluzione**: `True` indica che la soluzione copre tutto l'universo.
    - **Costo della soluzione**: `31699.621793222723` è il costo totale della soluzione trovata.
    - Questo indica che l'algoritmo ha trovato una soluzione valida con un costo iniziale significativo.

2. **Seconda esecuzione dell'algoritmo**:

    ```plaintext
    ic| valid(solution): np.True_
        cost(solution): np.float64(17236.738758112828)
    ```

    - **Validità della soluzione**: `True`.
    - **Costo della soluzione**: `17236.738758112828` è il costo totale della soluzione ottimale trovata.
    - Questa esecuzione mostra un miglioramento significativo nella qualità della soluzione.

3. **Terza esecuzione dell'algoritmo**:

    ```plaintext
    ic| fitness(solution): (np.False_, np.float64(-9326.880789813478))
    ic| fitness(solution): (np.False_, np.float64(-0.0))
    ```

    - **Validità della soluzione**: `False` indica che la soluzione non copre tutto l'universo.
    - **Costo della soluzione**: `-9326.880789813478` e `-0.0` rappresentano soluzioni non valide con costi negativi proporzionali alla violazione dei vincoli.
    - Queste esecuzioni evidenziano che l'algoritmo può generare soluzioni non valide, specialmente in iterazioni avanzate.

### Risultati di **RHMC Migliorato con Forza di Mutazione Dinamica**:

1. **Prima esecuzione dell'algoritmo**:

    ```plaintext
    ic| fitness(solution): (np.False_, np.float64(-10136.740089273946))
    ```

    - **Validità della soluzione**: `False`.
    - **Costo della soluzione**: `-10136.740089273946` indica una soluzione non valida con una significativa violazione dei vincoli.

2. **Seconda esecuzione dell'algoritmo**:

    ```plaintext
    ic| fitness(solution): (np.True_, np.float64(-5670.735744409689))
    ```

    - **Validità della soluzione**: `True`.
    - **Costo della soluzione**: `-5670.735744409689` è il costo totale della soluzione ottimale trovata.
    - Questa esecuzione mostra che l'algoritmo migliorato è in grado di trovare soluzioni valide con costi inferiori rispetto alla versione standard.

### Valutazione della **best_solution**:

```plaintext
ic| evaluate(best_solution): np.True_
    cost(best_solution): np.float64(-5670.735744409689)
```

- **Soluzione migliore**: `-5670.735744409689`.
- **Validità della soluzione**: `True`.
- La soluzione ottimale è stata trovata con un costo significativamente inferiore, indicando un'efficacia superiore dell'algoritmo migliorato.

### Riepilogo Generale:

- **Algoritmo RHMC Senza Strength**:
  - Ha trovato soluzioni valide con costi variabili, raggiungendo un costo minimo di **17236.738758112828**.
  - In alcune iterazioni avanzate, l'algoritmo ha generato soluzioni non valide.
  
- **Algoritmo RHMC Migliorato con Forza di Mutazione Dinamica**:
  - Ha trovato soluzioni valide con costi inferiori, raggiungendo un costo minimo di **-5670.735744409689**.
  - L'introduzione del meccanismo dinamico di adattamento della forza di mutazione ha migliorato l'efficienza nella ricerca di soluzioni ottimali.

---
  
## Differenze tra i Due Algoritmi di Risoluzione

Le due versioni degli algoritmi presentano differenze significative nella gestione delle mutazioni e nell'adattamento della ricerca, migliorando l'efficacia complessiva nella risoluzione del problema del Set Cover.

### 1. **Funzioni di Mutazione**

- **RHMC Standard**:
  - **Multiple Mutation**: Applica una mutazione a più sottoinsiemi basata su una probabilità fissa (1%).
  
  ```python
  def multiple_mutation(solution: np.ndarray) -> np.ndarray:
      mask = rng.random(NUM_SETS) < 0.01
      new_sol = np.logical_xor(solution, mask)
      return new_sol
  ```
  
- **RHMC Migliorato**:
  - **Multiple Mutation with Dynamic Strength**: Introduce un parametro `strength` che controlla la probabilità di mutazione, adattandola dinamicamente in base ai progressi dell'algoritmo.
  
  ```python
  def multiple_mutation_strength(solution: np.ndarray, strength: float = 0.3) -> np.ndarray:
      mask = rng.random(NUM_SETS) < strength
      if not np.any(mask):
          mask[np.random.randint(NUM_SETS)] = True
      new_sol = np.logical_xor(solution, mask)
      return new_sol
  ```

### 2. **Adattamento della Forza di Mutazione**

- **RHMC Standard**:
  - Utilizza una probabilità di mutazione fissa, senza alcun meccanismo di adattamento durante l'esecuzione dell'algoritmo.
  
- **RHMC Migliorato**:
  - Implementa un meccanismo dinamico che adatta la probabilità di mutazione (`strength`) in base ai risultati recenti, utilizzando un buffer.
  - Se la maggior parte delle ultime mutazioni ha portato a miglioramenti, aumenta la forza di mutazione per esplorare ulteriormente lo spazio delle soluzioni.
  - Se poche mutazioni hanno portato a miglioramenti, riduce la forza di mutazione per raffinare la ricerca.
  
  ```python
  buffer = list()
  BUFFER_SIZE = 50

  for steps in range(10_000):
      new_solution = multiple_mutation_strength(solution, strength)
      f = fitness(new_solution)

      history.append(float(f[1]))
      buffer.append(f > solution_fitness)
      buffer = buffer[-BUFFER_SIZE:]
      if sum(buffer) > 10:
          strength *= 1.1
      elif sum(buffer) < 10:
          strength /= 1.1

      if f > solution_fitness:
          solution = new_solution
          solution_fitness = fitness(solution)
  ```

### 3. **Buffer per il Controllo dell'Evoluzione**

- **RHMC Standard**:
  - Non utilizza un buffer. La decisione di accettare una nuova soluzione si basa esclusivamente sul confronto diretto con la soluzione corrente.
  
- **RHMC Migliorato**:
  - Introduce un buffer che memorizza le ultime `BUFFER_SIZE` valutazioni delle mutazioni.
  - Utilizza il buffer per determinare se aumentare o diminuire la forza di mutazione, basandosi sulla frequenza dei miglioramenti recenti.
  
  ```python
  buffer = list()
  buffer.append(f > solution_fitness)
  buffer = buffer[-BUFFER_SIZE:]
  if sum(buffer) > 10:
      strength *= 1.1
  elif sum(buffer) < 10:
      strength /= 1.1
  ```

### 4. **Criterio di Ottimizzazione**

- **RHMC Standard**:
  - Accetta solo mutazioni che migliorano la soluzione corrente, senza ulteriori ottimizzazioni o adattamenti.
  
- **RHMC Migliorato**:
  - Oltre ad accettare mutazioni migliorative, adatta dinamicamente la probabilità di mutazione per bilanciare esplorazione ed esploitazione.
  - Questo permette una ricerca più efficace, evitando di rimanere bloccati in massimi locali e migliorando la capacità di trovare soluzioni ottimali.

### 5. **Output e Visualizzazione**

L'idea del grafico è mostrare come la fitness della soluzione cambia man mano che l'algoritmo esegue piccoli cambiamenti ("mutazioni") alla soluzione corrente. 

- Se la linea rossa mostra un andamento discendente, significa che l'algoritmo sta trovando soluzioni con costi progressivamente più bassi, avvicinandosi a una buona soluzione.
- Se la linea è piatta, potrebbe indicare che l'algoritmo ha raggiunto un massimo locale e non è in grado di trovare una soluzione migliore.
![alt text](<img/set-cover 1.1.png>)
![alt text](<img/set-cover 1.2.png>)

- **Asse delle x**: rappresenta il numero di iterazioni (o "steps") dell'algoritmo. Ogni punto sull'asse delle x corrisponde a un tentativo dell'algoritmo di migliorare la soluzione corrente.
  
- **Asse delle y**: rappresenta il **valore della fitness** della soluzione, che nel caso del problema di Set Cover è misurata dal costo della soluzione (da minimizzare). Poiché l'algoritmo cerca di trovare una soluzione con costo più basso, il valore sull'asse delle y dovrebbe diminuire man mano che l'algoritmo migliora la soluzione.

- **Linea rossa**: rappresenta il miglior **valore massimo accumulato** della fitness fino a quel punto. L'algoritmo tiene traccia della migliore soluzione trovata finora, e la linea rossa rappresenta il valore della fitness della soluzione migliore fino a quel momento.
  
- **Punti**: i punti nel grafico rappresentano i valori della fitness di ogni soluzione tentata ad ogni iterazione. Questo mostra come l'algoritmo esplora diverse soluzioni, alcune delle quali possono essere peggiori o migliori rispetto alla soluzione corrente.



### In sintesi:
Il grafico fornisce una visione chiara di come l'algoritmo si comporta durante l'ottimizzazione del problema di Set Cover, mostrando se sta facendo progressi e se sta trovando soluzioni con costi via via minori nel corso delle iterazioni.
  
## Risultati Finali

Il grafico finale mostra come l'algoritmo **RHMC Migliorato con Forza di Mutazione Dinamica**, grazie alla sua capacità di adattare dinamicamente la probabilità di mutazione, riesca a trovare soluzioni valide con un costo inferiore rispetto all'algoritmo **RHMC Standard**. Questo evidenzia l'efficacia delle strategie di tweaking e adattamento nella ricerca di soluzioni ottimali per problemi complessi di ottimizzazione combinatoria come il **problema del Set Cover**.

---
  
## Conclusione

Questo notebook esplora diverse varianti di algoritmi euristici per risolvere il **problema del Set Cover**. Ogni approccio propone strategie per migliorare progressivamente la qualità delle soluzioni, dimostrando l'efficacia di tecniche avanzate come l'adattamento dinamico della forza di mutazione nella risoluzione di problemi complessi di ottimizzazione combinatoria. L'algoritmo migliorato ha mostrato una maggiore efficienza e capacità di trovare soluzioni ottimali rispetto alla versione standard, sottolineando l'importanza di strategie di adattamento nella ricerca euristica.

---
  