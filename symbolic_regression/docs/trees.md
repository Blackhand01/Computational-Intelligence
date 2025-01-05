### **1. Dimensione di un Albero**
- **Definizione**: La dimensione di un albero è il numero totale di nodi che contiene, inclusa la radice e tutti i nodi interni e foglia.
- **Formula**:
  \[
  \text{Dimensione} = 1 + (\text{Dimensione del Sottoalbero Sinistro}) + (\text{Dimensione del Sottoalbero Destro})
  \]
- **Esempio**:
  - Un albero con una radice e due figli ha dimensione \(3\).
  - Se un sottoalbero contiene \(5\) nodi e un altro ne contiene \(3\), la dimensione totale è \(9\).

---

### **2. Altezza di un Albero**
- **Definizione**: L'altezza di un albero è la lunghezza del percorso più lungo dalla radice a una foglia (inclusi i livelli attraversati).
- **Formula**:
  \[
  \text{Altezza} = 1 + \max(\text{Altezza del Sottoalbero Sinistro}, \text{Altezza del Sottoalbero Destro})
  \]
- **Caratteristiche**:
  - Un albero con un solo nodo (la radice) ha altezza \(1\).
  - Gli alberi bilanciati hanno altezza minima per una data dimensione.
  - Alberi degenerati (come una lista) hanno altezza massima.

---

### **3. Profondità di un Nodo**
- **Definizione**: La profondità di un nodo è la distanza (numero di archi) tra quel nodo e la radice dell'albero.
- **Formula**:
  \[
  \text{Profondità del Nodo} = 1 + (\text{Profondità del Nodo Genitore})
  \]
- **Caratteristiche**:
  - La radice ha profondità \(0\) (o \(1\) in alcune convenzioni).
  - Le foglie possono avere profondità diverse a seconda della struttura dell'albero.

---

### **4. Ampiezza di un Albero**
- **Definizione**: L'ampiezza di un albero è il numero massimo di nodi presenti a un livello qualsiasi.
- **Caratteristiche**:
  - Alberi bilanciati tendono ad avere ampiezza maggiore a metà della loro altezza.
  - Alberi degenerati (simili a una lista) hanno ampiezza \(1\) a ogni livello.

---

### **Esempio Completo**
Supponiamo di avere questo albero binario:

```
         A
       /   \
      B     C
     / \   / \
    D   E F   G
```

1. **Dimensione**:
   - Numero totale di nodi: \(7\) (A, B, C, D, E, F, G).

2. **Altezza**:
   - Il percorso più lungo dalla radice a una foglia è \(A \to B \to D\) (o qualsiasi altro percorso completo).
   - Altezza: \(3\).

3. **Profondità**:
   - Nodo \(A\): \(0\) (radice).
   - Nodo \(B\): \(1\).
   - Nodo \(D\): \(2\).

4. **Ampiezza**:
   - Livello \(0\): \(1\) nodo (\(A\)).
   - Livello \(1\): \(2\) nodi (\(B, C\)).
   - Livello \(2\): \(4\) nodi (\(D, E, F, G\)).
   - Ampiezza massima: \(4\).

---

### **Confronto Visivo**
| **Caratteristica** | **Descrizione**                                      | **Esempio**                  |
|--------------------|------------------------------------------------------|------------------------------|
| **Dimensione**     | Numero totale di nodi nell'albero.                   | \(7\)                        |
| **Altezza**        | Percorso più lungo dalla radice a una foglia.        | \(3\)                        |
| **Profondità**     | Distanza di un nodo dalla radice.                    | Nodo \(D\): \(2\)            |
| **Ampiezza**       | Numero massimo di nodi in un livello.                | Livello \(2\): \(4\) nodi    |

