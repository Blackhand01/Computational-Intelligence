# **Report: Determinazione dei Costi delle Funzioni**

## **Introduzione**
Nel contesto del progetto di regressione simbolica, abbiamo assegnato un costo relativo a ciascuna funzione matematica utilizzata. Questo costo è stato determinato in base a:
- **Tempi di esecuzione medi**, misurati tramite benchmark su un array di grandi dimensioni ($10^6$ elementi).
- **Unarità o binarità dell’operatore**: Sebbene questa caratteristica non influisca direttamente sul tempo computazionale, determina la complessità strutturale degli alberi sintattici:
  - Gli operatori binari aggiungono due nodi figli, aumentando la profondità e il numero totale di nodi.
  - Penalizzare gli operatori binari favorisce alberi più semplici e introduce una forma di regolarizzazione.

Per adattare dinamicamente la penalizzazione degli operatori binari in base alla complessità del problema, è stato introdotto un **fattore dinamico $k$**.

---

## **Benchmark dei Tempi**
Le operazioni sono state eseguite su un array casuale di dimensione $10^6$. I tempi medi di esecuzione per ciascun operatore sono riportati nella tabella seguente:

| **Operatore** | **Arity** | **Tempo Misurato (s)** | **Categoria**        |
|---------------|-----------|-------------------------|----------------------|
| `neg`         | Unario    | 0.000511               | Molto Rapido         |
| `abs`         | Unario    | 0.000554               | Molto Rapido         |
| `pow2`        | Unario    | 0.000658               | Rapido               |
| `add`         | Binario   | 0.000690               | Rapido               |
| `mul`         | Binario   | 0.000690               | Rapido               |
| `div`         | Binario   | 0.001776               | Medio                |
| `sqrt`        | Unario    | 0.001789               | Medio                |
| `ln`          | Unario    | 0.004349               | Complesso            |
| `pow`         | Binario   | 0.010379               | Molto Complesso      |
| `mod`         | Binario   | 0.011584               | Molto Complesso      |

---

## **Dynamic $k$: Penalizzazione Dinamica**
Il fattore dinamico $k$ è progettato per regolare i costi degli operatori binari durante l’evoluzione simbolica. 

### **1. Formula per $k$**
La penalizzazione dinamica è calcolata come:
$$
k = 1.0 + 0.5 \cdot \left( \text{fattore dimensione} + \text{fattore complessità} + \text{fattore evoluzione} \right)
$$
Dove:
- **Fattore Dimensione**:
  $$
  \text{fattore dimensione} = \min\left(\frac{\text{dimensione dataset}}{10000}, 2.0\right)
  $$
  Questo valore cresce con la dimensione del dataset, riflettendo l’aumento della complessità computazionale per calcolare la fitness su un dataset più grande.

- **Fattore Complessità**:
  $$
  \text{fattore complessità} = \min\left(\frac{\text{numero massimo nodi albero}}{100}, 2.0\right)
  $$
  Questo valore cresce con la complessità strutturale degli alberi, penalizzando i costi degli operatori binari.

- **Fattore Evoluzione**:
  $$
  \text{fattore evoluzione} = \frac{\text{generazione corrente}}{\text{generazioni totali}}
  $$
  Questo valore aumenta linearmente con il progresso generazionale, incentivando la ricerca di soluzioni più semplici nelle fasi iniziali e soluzioni più complesse in quelle avanzate.

---

### **2. Esempio di Calcolo**
Supponiamo:
- **Dimensione del dataset**: $50,000$.
- **Numero massimo di nodi**: $200$.
- **Generazione corrente**: $10$.
- **Generazioni totali**: $50$.

I fattori sono calcolati come segue:
- Fattore Dimensione: $\min(50,000 / 10,000, 2.0) = 2.0$.
- Fattore Complessità: $\min(200 / 100, 2.0) = 2.0$.
- Fattore Evoluzione: $10 / 50 = 0.2$.

Il valore di $k$ è:
$$
k = 1.0 + 0.5 \cdot (2.0 + 2.0 + 0.2) = 3.1
$$

---

### **3. Influenza di $k$ sui Costi**
Il valore di $k$ è applicato solo agli operatori binari, moltiplicandone i costi normalizzati:
$$
\text{Costo Finale} =
\begin{cases}
\text{Costo Normalizzato} & \text{se Unario} \\
k \times \text{Costo Normalizzato} & \text{se Binario}
\end{cases}
$$

Con $k = 3.1$, i costi finali per alcuni operatori sono:
| **Operatore** | **Arity** | **Costo Normalizzato** | **Costo Finale** |
|---------------|-----------|-------------------------|------------------|
| `neg`         | Unario    | 0.0441                 | 0.0441           |
| `add`         | Binario   | 0.0595                 | 0.1845           |
| `pow`         | Binario   | 0.8958                 | 2.7760           |

---

## **Operator Benchmark Results (Averaged)**
I costi medi di esecuzione per gli operatori sono riportati nella tabella seguente:

| **Operatore** | **Tempo Misurato (s)** | **Costo Normalizzato** | **Costo Finale (con $k = 3.1$)** |
|---------------|-------------------------|-------------------------|----------------------------------|
| `pow2`        | 0.000509               | 0.0441                 | 0.1367                           |
| `abs`         | 0.000528               | 0.0458                 | 0.1420                           |
| `neg`         | 0.000600               | 0.0520                 | 0.1612                           |
| `min`         | 0.000702               | 0.0608                 | 0.1885                           |
| `max`         | 0.000713               | 0.0618                 | 0.1915                           |
| `mul`         | 0.000728               | 0.0631                 | 0.1966                           |
| `add`         | 0.000729               | 0.0632                 | 0.1969                           |
| `sub`         | 0.000734               | 0.0636                 | 0.1972                           |
| `pow3`        | 0.000783               | 0.0679                 | 0.2105                           |
| `div`         | 0.001731               | 0.1500                 | 0.4650                           |
| `sqrt`        | 0.001953               | 0.1693                 | 0.5252                           |
| `hypot`       | 0.002317               | 0.2008                 | 0.6225                           |
| `tanh`        | 0.003472               | 0.3009                 | 0.9338                           |
| `exp`         | 0.003939               | 0.3414                 | 1.0583                           |
| `ln`          | 0.004340               | 0.3761                 | 1.1667                           |
| `log2`        | 0.004577               | 0.3967                 | 1.2307                           |
| `tan`         | 0.004686               | 0.4061                 | 1.2609                           |
| `log10`       | 0.004817               | 0.4175                 | 1.2943                           |
| `cos`         | 0.008301               | 0.7194                 | 2.2282                           |
| `sin`         | 0.008305               | 0.7198                 | 2.2304                           |
| `pow`         | 0.010336               | 0.8958                 | 2.7760                           |
| `mod`         | 0.011538               | 1.0000                 | 3.1000                           |

---

## **Conclusione**
Dynamic $k$ permette di:
1. **Adattare i Costi Dinamicamente**:
   - Penalizzando maggiormente gli operatori binari nei problemi complessi e nei dataset di grandi dimensioni.
2. **Favorire Alberi Più Semplici**:
   - Nelle prime generazioni, si incentivano soluzioni semplici, riducendo il rischio di overfitting.
3. **Gestire la Complessità Progressivamente**:
   - Nelle generazioni successive, si bilancia la complessità computazionale per consentire la scoperta di soluzioni più espressive.

Dynamic $k$ rappresenta un elemento chiave per bilanciare efficienza e capacità espressiva nel framework di regressione simbolica.

---

### **Riferimenti**
- [Documentazione NumPy](https://numpy.org/doc/)
