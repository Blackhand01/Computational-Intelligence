# **Analisi del Problema \( $n^2 - 1$ \) Puzzle**

Il problema \( $n^2 - 1$ \) (ad esempio il Mystic Square) è un classico problema di ricerca nello spazio degli stati, in cui:

1. **Stato**: La configurazione della matrice $n \times n$.
2. **Azione**: Movimento della cella vuota in una delle direzioni valide (alto, basso, sinistra, destra).
3. **Stato Obiettivo**: La matrice ordinata in ordine crescente con il vuoto in basso a destra.

---

## **Spazio degli Stati**

Per un puzzle di dimensione $n^2 - 1$, il numero totale di stati possibili è $\frac{(n^2)!}{2}$, dato che solo metà delle configurazioni è risolvibile. 

- **Esempio**:
  - $3 \times 3$: $\frac{9!}{2} = 181,440$ stati.
  - $4 \times 4$: $\frac{16!}{2} \approx 10^{13}$ stati.

La dimensione dello spazio degli stati influisce direttamente sul costo temporale e spaziale degli algoritmi di ricerca.

---

## **Costi Temporali e Spaziali degli Algoritmi**

| **Algoritmo**             | **Complessità Temporale**   | **Complessità Spaziale** | **Pro**                             | **Contro**                        |
|---------------------------|-----------------------------|---------------------------|-------------------------------------|------------------------------------|
| **Breadth-First Search**  | $O(b^d)$                   | $O(b^d)$                 | Soluzione ottima (se costi uniformi) | Richiede memoria esponenziale.    |
| **Depth-First Search**    | $O(b^m)$                   | $O(m)$                   | Usa meno memoria rispetto a BFS.    | Non garantisce soluzioni ottime.  |
| **Iterative Deepening DFS** | $O(b^d)$                 | $O(d)$                   | Soluzione ottima e uso di poca memoria. | Ripete calcoli su livelli già esplorati. |
| **A*** (informata)        | $O(b^d)$                   | $O(b^d)$                 | Soluzioni ottime ed efficienti con buone euristiche. | Richiede calcoli euristici aggiuntivi. |

Dove:
- $b$: Fattore di ramificazione (numero medio di mosse per stato, tipicamente 2-4 per il puzzle $n^2 - 1$).
- $d$: Profondità della soluzione.
- $m$: Profondità massima dell’albero di ricerca.

---

## **Analisi per Algoritmo**

### **Breadth-First Search (BFS)**

- **Tempo**: Esamina sistematicamente tutti gli stati fino alla profondità $d$.
- **Spazio**: Deve mantenere tutti i nodi nella frontiera, $O(b^d)$.
- **Adatto a**: Puzzle piccoli o problemi dove è richiesta la soluzione ottima.

### **Depth-First Search (DFS)**

- **Tempo**: Esplora percorsi fino alla profondità $m$, $O(b^m)$.
- **Spazio**: Memorizza solo il percorso corrente, $O(m)$.
- **Adatto a**: Puzzle grandi, ma non garantisce soluzioni ottimali.

### **Iterative Deepening Depth-First Search (IDDFS)**

- **Tempo**: Combina DFS con limiti di profondità crescenti, $O(b^d)$.
- **Spazio**: Memorizza solo il percorso corrente, $O(d)$.
- **Adatto a**: Puzzle medi o grandi, quando è richiesta la soluzione ottima con bassa memoria.

### **A*** (informata)

- **Tempo**: Dipende dall’euristica; nel caso peggiore $O(b^d)$.
- **Spazio**: Memorizza tutti i nodi espansi nella frontiera, $O(b^d)$.
- **Adatto a**: Puzzle grandi, con una buona euristica.

---

## **Confronto delle Complessità**

| **Algoritmo**             | **Puzzle $3 \times 3$** | **Puzzle $4 \times 4$** |
|---------------------------|-------------------------|-------------------------|
| BFS                       | Elevato ($181,440$ stati) | Impraticabile ($10^{13}$ stati) |
| DFS                       | Dipende dalla profondità   | Molto inefficiente         |
| IDDFS                     | Migliore di BFS            | Troppo lento per $10^{13}$ stati |
| A* (con Manhattan)        | Gestibile                  | Elevato ma fattibile       |

---

## **Proprietà delle Euristiche di A*** 
- **Admissibilità**: Un’euristica $h(n)$ è ammissibile se non sovrastima mai il costo per raggiungere l’obiettivo. Garantisce soluzioni ottimali.
- **Consistenza**: $h(n)$ è consistente se per ogni nodo $n$ e successore $n_s$, vale $h(n) \leq \text{cost}(n, n_s) + h(n_s)$. Garantisce che un nodo espanso non venga riconsiderato.

---

## **Conclusioni**

- **Per puzzle $3 \times 3$**:
  - BFS o A* con euristica di Manhattan sono praticabili.
- **Per puzzle $4 \times 4$**:
  - BFS è impraticabile. A* con buone euristiche (ad esempio Manhattan) o IDDFS rappresentano le scelte migliori.

---