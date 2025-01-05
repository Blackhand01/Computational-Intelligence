# **Report: Scelta e Implementazione degli Operatori**

## **Introduzione**
Il file `definitions.py` definisce gli operatori matematici utilizzati nel framework di regressione simbolica. Tra questi, il logaritmo naturale è rappresentato correttamente come `ln`, mentre `log2` e `log10` rappresentano logaritmi con basi specifiche. Questa distinzione è fondamentale per garantire chiarezza e coerenza nell'implementazione degli operatori.

---

## **Motivazioni per la Scelta degli Operatori**

### **1. Operatori Logaritmici**
#### **`ln` - Logaritmo Naturale**
- Il logaritmo naturale ($\ln(x)$) è la funzione inversa dell’esponenziale con base $e$ (numero di Eulero, $e \approx 2.718$).
- Utilizzato frequentemente in modelli matematici, fisici e statistici.
- In Python, è implementato tramite `np.log`.

#### **`log2` e `log10` - Logaritmi Specifici**
- Rappresentano logaritmi con basi fisse:
  - `log2` ($\log_2(x)$): utile in informatica e teoria dell'informazione (ad esempio, calcolo di entropia).
  - `log10` ($\log_{10}(x)$): utilizzato in scale logaritmiche come decibel o pH.

Questa distinzione evita ambiguità e migliora l’espressività del framework.

---

### **2. Riduzione della Complessità Strutturale**
Operatori specifici come `pow2` e `pow3` riducono la complessità strutturale rispetto all’uso generico di `pow`.

#### **Senza Operatori Specifici**
Un albero che rappresenta $x^2 + x^3$ utilizzando solo `pow`:

```
        +
       / \
    pow   pow
    / \   / \
   x   2 x   3
```
- **Nodi totali**: 7.
- **Operatori binari**: 2.

#### **Con Operatori Specifici**
Un albero equivalente che utilizza `pow2` e `pow3`:

```
        +
       / \
    pow2 pow3
      |    |
      x    x
```
- **Nodi totali**: 5.
- **Operatori unari**: 2.

### **Vantaggi**
1. **Riduzione della complessità**: Alberi più compatti.
2. **Efficienza computazionale**: Calcoli più veloci con operatori unari.

---

### **3. Sicurezza Numerica**
Gli operatori potenzialmente instabili sono implementati come funzioni sicure (`safe_*`):
- **`safe_ln`**: Previene errori per $x \leq 0$.
- **`safe_divide`**: Gestisce divisioni per zero.
- **`safe_power`**: Limita la base e l’esponente per evitare overflow.

Questa implementazione garantisce robustezza e stabilità numerica.

---

### **4. Operatori Trigonometrici**
Gli operatori `sin`, `cos`, `tan`, `arcsin`, `arccos`, e `arctan` ampliano le capacità del framework per supportare modelli con fenomeni angolari o ciclici:
- **Applicazioni**:
  - Moto armonico semplice.
  - Onde sinusoidali in fisica.
  - Calcolo di angoli e distanze.

---

### **5. Regolazione Dinamica del Costo**
Il metodo `set_dynamic_k` bilancia i costi degli operatori in base a:
1. Dimensione del dataset.
2. Complessità degli alberi.
3. Progresso generazionale.

Questo approccio adatta dinamicamente il framework, favorendo soluzioni più semplici ed efficienti.

---

## **Conclusioni**
La progettazione del file `definitions.py` riflette un approccio sistematico per:
1. **Chiarezza e coerenza**:
   - La distinzione tra `ln`, `log2`, e `log10` garantisce interpretabilità.
2. **Riduzione della complessità**:
   - Gli operatori specifici semplificano la struttura degli alberi.
3. **Sicurezza numerica**:
   - Le funzioni `safe_*` prevengono errori numerici.
4. **Adattabilità**:
   - La regolazione dinamica dei costi ottimizza il framework per problemi di varia complessità.

Questo design bilancia flessibilità, stabilità e capacità espressiva, rendendo il framework adatto a una vasta gamma di applicazioni simboliche.
