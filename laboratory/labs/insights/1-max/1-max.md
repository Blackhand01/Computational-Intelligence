
Questo notebook rappresenta un semplice esempio di un **problema di ottimizzazione iterativa**. 

## Descrizione del problema
Il problema in questione è un esempio classico di **ottimizzazione combinatoria**: partiamo da una lista di `0` e `1` (chiamata **soluzione**), e l'obiettivo è massimizzare il numero di `1` oppure di `0` nella lista, dove la lunghezza della lista è definita da una costante `PROBLEM_SIZE`.

L'obiettivo dell'algoritmo è trovare una soluzione "migliore" a partire da una soluzione iniziale casuale, eseguendo piccoli aggiustamenti (detti **"tweak"**) sulla soluzione corrente. Il concetto chiave è utilizzare una strategia di miglioramento locale, dove si esplora lo spazio delle soluzioni modificando iterativamente la soluzione corrente per migliorarla, valutando il progresso tramite una funzione di qualità.

---

## Flowchart del processo

Ecco un diagramma che illustra il flusso logico dell'algoritmo:

+---------------------------+
|   Generate initial random  |
|        solution            |
+---------------------------+
            |
            v
+---------------------------+
|     Evaluate quality of    |
|     the initial solution   |
+---------------------------+
            |
            v
+---------------------------+
|      Improve solution      |
|     by tweaking it         |
+---------------------------+
            |
            v
+---------------------------+
|  If new solution is better |
|      keep the tweak        |
+---------------------------+
            |
            v
+---------------------------+
| Repeat until the solution  |
| reaches the maximum score  |
+---------------------------+

---

## Spiegazione del codice


### 1. Funzione di qualità

```python
def quality(solution):
    return max(sum(solution), PROBLEM_SIZE - sum(solution))
```

Questa funzione valuta la **qualità** di una soluzione. La qualità di una soluzione è definita dal massimo tra la somma dei valori in `solution` e `PROBLEM_SIZE - sum(solution)`. In altre parole, si cerca di massimizzare il numero di `1` o il numero di `0` nella lista.

### 2. Funzione per modificare la soluzione (tweak)

```python
def tweak(solution):
    new_solution = solution[:]
    pos = random.randrange(PROBLEM_SIZE)
    new_solution[pos] = 1 - new_solution[pos]
    return new_solution
```

La funzione `tweak` sceglie una posizione casuale pos nella lista solution e inverte il valore in quella posizione (da `1` a `0` o da `0` a `1`). Questo processo di tweaking continua a modificare la lista fino a raggiungere una soluzione che massimizza il numero di 1 o 0.

### 3. Creazione della soluzione iniziale

```python
initial_solution = [random.randint(0, 1) for _ in range(PROBLEM_SIZE)]
ic(quality(initial_solution))
None
```

Qui generiamo una **soluzione iniziale casuale**, composta da `0` e `1` generati in modo casuale. La qualità della soluzione iniziale viene poi stampata per il debugging.

### 4. Prima strategia di miglioramento iterativo

```python
current_solution = initial_solution
steps = 0
ic(steps, quality(current_solution))
while quality(current_solution) < PROBLEM_SIZE:
    steps += 1
    solution = tweak(current_solution)
    if quality(solution) > quality(current_solution):
        current_solution = solution
ic(steps, quality(current_solution))
```

In questa sezione, utilizziamo una strategia semplice: partiamo dalla soluzione iniziale e iteriamo fino a trovare una soluzione che abbia la qualità massima (ovvero la somma dei valori sia uguale a `PROBLEM_SIZE`). A ogni iterazione, si esegue un tweak sulla soluzione corrente e, se la qualità della nuova soluzione è migliore, la soluzione viene aggiornata.

### 5. Seconda strategia con "inner loop"

```python
current_solution = initial_solution
steps = 0
ic(steps, quality(current_solution))
while quality(current_solution) < PROBLEM_SIZE:
    temp = current_solution[:]
    best_so_far = current_solution[:]
    for inner_step in range(10):
        steps += 1
        solution = tweak(current_solution)
        if quality(solution) > quality(best_so_far):
            best_so_far = solution
    if quality(best_so_far) > quality(current_solution):
        current_solution = best_so_far
ic(steps, quality(current_solution))
```

Questa strategia è leggermente più complessa e introduce un ciclo interno (`inner loop`). Invece di fare un singolo tweak a ogni passo, esploriamo più soluzioni vicine (10 per ogni ciclo). Alla fine del ciclo interno, aggiorniamo la soluzione corrente solo se troviamo una migliore.

---

## Analisi Risultati

### 1. **Qualità della soluzione iniziale**

```plaintext
ic| steps: 0, quality(current_solution): 54
```

La qualità della soluzione iniziale è `54`. Questo significa che nella lista casuale generata di 100 elementi (composta da `0` e `1`), ci sono 54 `1` (oppure 54 `0`, visto che il massimo tra questi due è la misura della qualità).


### 2. **Raggiungimento della soluzione ottimale (prima strategia)**

```plaintext
ic| steps: 272, quality(current_solution): 100
```

Dopo `272` passi (o tweak), l'algoritmo ha trovato una soluzione ottimale con una qualità pari a `100`. Questo significa che la lista è composta interamente da `1` o interamente da `0`, quindi è stata raggiunta una delle soluzioni massime possibili.


### 3. **Raggiungimento della soluzione ottimale (seconda strategia)**

```plaintext
ic| steps: 910, quality(current_solution): 100
```

Dopo `910` passi, l'algoritmo ha trovato nuovamente una soluzione ottimale con una qualità pari a `100`. Tuttavia, rispetto alla prima strategia, ha impiegato un numero maggiore di iterazioni (910 contro 272), poiché la seconda strategia esplora più soluzioni prima di accettare una modifica.


### Analisi delle due strategie

- **Prima strategia**: È più veloce nel trovare una soluzione ottimale (272 passi). Si basa sull'accettare immediatamente una modifica migliorativa alla soluzione corrente.
- **Seconda strategia**: Ha richiesto più iterazioni (910 passi) per trovare una soluzione ottimale, poiché esplora più soluzioni (10 per ogni ciclo) prima di accettare un miglioramento. Questa strategia, sebbene più lenta, può essere più robusta in scenari più complessi.
---

## Conclusione

Il notebook implementa due versioni di un algoritmo di ottimizzazione iterativa:
1. **Prima versione**: Ogni volta che una nuova soluzione è migliore di quella corrente, viene accettata immediatamente.
2. **Seconda versione**: Si esplorano diverse soluzioni prima di scegliere quella migliore.

In sintesi, entrambe le strategie hanno raggiunto lo stesso risultato (qualità `100`), ma la prima è stata più veloce in questo caso specifico.
