Ecco un esempio di report in formato Markdown per documentare il processo di determinazione dei costi delle funzioni in base ai benchmark:

---

# **Report: Determinazione dei Costi delle Funzioni**
### **Progetto di Regressione Simbolica**

---

## **Introduzione**
Nel contesto del progetto di regressione simbolica, abbiamo assegnato un costo relativo a ciascuna funzione matematica utilizzata. Questo costo è stato determinato in base ai tempi di esecuzione medi delle funzioni, misurati tramite benchmark su un array di grandi dimensioni (\(10^6\) elementi). 

L'obiettivo è favorire funzioni rapide e penalizzare quelle più lente durante la costruzione degli alberi sintattici.

---

## **Benchmark dei Tempi**
Le operazioni sono state eseguite su un array casuale di dimensione \(10^6\). I tempi medi di esecuzione sono riportati nella seguente tabella:

| **Operatore** | **Tempo Misurato (s)** | **Categoria**        |
|---------------|-------------------------|----------------------|
| `neg`         | 0.000511               | Molto Rapido         |
| `abs`         | 0.000554               | Molto Rapido         |
| `pow2`        | 0.000658               | Rapido               |
| `add`         | 0.000690               | Rapido               |
| `mul`         | 0.000690               | Rapido               |
| `div`         | 0.001776               | Medio                |
| `sqrt`        | 0.001789               | Medio                |
| `log`         | 0.004349               | Complesso            |
| `pow`         | 0.010379               | Molto Complesso      |
| `mod`         | 0.011584               | Molto Complesso      |

---

## **Formula di Normalizzazione**
Per calcolare i costi relativi delle funzioni, abbiamo utilizzato la seguente formula di normalizzazione:

\[
\text{Costo Normalizzato} = \frac{\text{Tempo Misurato}}{\text{Tempo Massimo}}
\]

Dove il **tempo massimo** è il valore più alto misurato: \( \text{mod} = 0.011584 \, \text{s} \).

---

## **Costi Normalizzati**
La tabella seguente mostra i costi normalizzati per ciascun operatore, calcolati in base ai tempi misurati:

| **Operatore** | **Tempo Misurato (s)** | **Costo Normalizzato** |
|---------------|-------------------------|-------------------------|
| `neg`         | 0.000511               | 0.0441                 |
| `abs`         | 0.000554               | 0.0478                 |
| `pow2`        | 0.000658               | 0.0568                 |
| `add`         | 0.000690               | 0.0595                 |
| `mul`         | 0.000690               | 0.0595                 |
| `div`         | 0.001776               | 0.1533                 |
| `sqrt`        | 0.001789               | 0.1544                 |
| `log`         | 0.004349               | 0.3753                 |
| `pow`         | 0.010379               | 0.8958                 |
| `mod`         | 0.011584               | 1.0000                 |

---

## **Visualizzazione**
Ecco un grafico che confronta i tempi misurati e i costi normalizzati:

```mermaid
bar
    title Tempi e Costi Normalizzati
    "neg" : 0.000511, 0.0441
    "abs" : 0.000554, 0.0478
    "pow2" : 0.000658, 0.0568
    "add" : 0.000690, 0.0595
    "mul" : 0.000690, 0.0595
    "div" : 0.001776, 0.1533
    "sqrt" : 0.001789, 0.1544
    "log" : 0.004349, 0.3753
    "pow" : 0.010379, 0.8958
    "mod" : 0.011584, 1.0000
```

---

## **Conclusione**
Grazie al benchmark, abbiamo stabilito un costo relativo per ogni funzione matematica, normalizzato rispetto al tempo massimo. Questo approccio consente di:

1. Favorire operatori più rapidi (es. `neg`, `abs`, `pow2`).
2. Penalizzare operatori più complessi e costosi (es. `mod`, `pow`).

Questa classificazione verrà integrata nella funzione di fitness per influenzare positivamente la costruzione degli alberi sintattici.

---

### **Riferimenti**
- [Documentazione NumPy](https://numpy.org/doc/)

