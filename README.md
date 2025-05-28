# Symbolic Regression - Modular Framework

**Author:** Stefano Roy Bisignano
**GitHub:** [@StefanoRoyBisignano](#)
**Year:** 2024-2025

---

## 📌 Overview

This repository documents the development of an advanced modular system for **Symbolic Regression**, designed to explore techniques such as **Genetic Programming**, **Local Search**, and **Memetic Algorithms**.

The main goal is to generate interpretable mathematical formulas by optimizing the Mean Squared Error (MSE), ensuring computational efficiency and full compatibility with NumPy.

---

## 🧠 Highlights

* **Genetic Programming (GP)** with advanced operators
* **Local Search Integration**: Hill Climbing, Tabu Search, Simulated Annealing
* **Memetic Approach**: combining GP and local search for enhanced solutions
* Fully modular and scalable system design
* Advanced visualizations for analysis and result interpretation

---

## 🚀 Application Domains

The system is designed for a wide range of applications, including:

![Application Domains]![image](https://github.com/user-attachments/assets/0101f2be-3d51-4ea1-9acc-4de7e5fa0af6)

---

## 🔍 Methodology

### 🎛️ Algorithms and Strategies

* Fitness function combining MSE and tree complexity
* Adaptive strategies balancing exploration and exploitation
* Early stopping to optimize resource utilization

### ⚙️ Optimized Parameters

| Parameter         | Value |
| ----------------- | ----- |
| Population Size   | 600   |
| Generations       | 50    |
| Max Tree Depth    | 7     |
| Tournament Size   | 10    |
| Mutation Rate     | 0.6   |
| Crossover Rate    | 0.4   |
| Elitism           | 10    |
| Early Stopping    | 20    |
| Fitness Threshold | 1.0   |
| Random Seed       | 42    |

---

## 🛠️ Project Structure

```
symbolic_regression/
├── core/
│   ├── tree.py
│   ├── safe_math.py
│   ├── evaluator.py
│   └── statistics.py
├── memetic/
│   ├── local_search.py
│   ├── mutation.py
│   ├── crossover.py
│   └── selection.py
├── utils/
│   ├── plotting.py
│   ├── logger.py
│   └── utils.py
├── memetic_config.py
└── main.py
```

---

## 🔬 Technical Workflow

1. **Data Loading**
2. **Initial Population Generation**
3. **Evolution Process**
4. **Result Storage**
5. **Visualization and Analysis**

---

## 🌍 Reinforcement Learning Integration

The system is designed for future integration with **Reinforcement Learning**, leveraging architectures like:

![RL Integration](https://github.com/user-attachments/assets/4789ede6-fb75-428f-9dd9-52407abd928f)


And standard agent-environment interaction models:

![RL Environment-Agent](https://github.com/user-attachments/assets/a7f120f4-59fc-4ca0-a22e-d5b48861881d)

