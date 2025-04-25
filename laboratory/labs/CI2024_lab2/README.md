# Lab 2: Solving the Traveling Salesman Problem (TSP)

## Introduction

In **Lab 2**, we tackled the **Traveling Salesman Problem (TSP)**, a classic optimization challenge that seeks the shortest possible route visiting a set of cities exactly once and returning to the origin city. To approach this problem, we implemented and compared two distinct algorithms:

1. **Genetic Algorithm (GA)**: A slower yet more accurate evolutionary algorithm inspired by natural selection.
2. **Greedy Algorithm**: A fast but approximate heuristic-based method that quickly generates a feasible solution.

The objective was to evaluate the performance of both algorithms across various datasets, analyzing the final tour cost and the number of steps required to reach the solution.

## Algorithms Overview

### 1. Genetic Algorithm (GA)
  - **Initialization**: Generates an initial population of random tours.
  - **Selection**: Chooses parent tours based on fitness (tour cost).
  - **Crossover**: Combines parent tours to produce offspring.
  - **Mutation**: Introduces random variations to offspring tours.
  - **Elitism**: Preserves a subset of the best tours across generations.
  - **Termination**: Repeats the process for a predefined number of generations or until convergence.

### 2. Greedy Algorithm
  - Starts from the first city.
  - At each step, selects the nearest unvisited city.
  - Continues until all cities are visited, then returns to the starting city.

## Datasets
We evaluated both algorithms on the following TSP instances, each representing a different geographical region with varying numbers of cities:

| Instance          | Number of Cities |
|-------------------|-------------------|
| `italy`       | 46                |
| `vanuatu`     | 8                 |
| `russia`      | 167               |
| `us`          | 326               |
| `china`       | 726               |

## Results

### Genetic Algorithm (GA) Results

| Instance          | Number of Cities | Best Cost (km) | First Generation EA |
|-------------------|-------------------|----------------|----------------------|
| `italy`    | 46                | 4,319.7        | 535                  |
| `vanuatu`  | 8                 | 1,345.54       | 3                    |
| `russia`   | 167               | 49,424.43      | 927                  |
| `us`       | 326               | 76,928.6       | 924                  |
| `china`    | 726               | 228,161.52     | 976                  |

### Greedy Algorithm Results

| Instance          | Number of Cities | Best Cost (km) | First Step Greedy |
|-------------------|-------------------|----------------|-------------------|
| `italy`    | 46                | 4,436.03       | 46                |
| `vanuatu`  | 8                 | 1,475.53       | 8                 |
| `russia`   | 167               | 42,334.16      | 167               |
| `us`       | 326               | 48,050.03      | 326               |
| `china`    | 726               | 63,962.92      | 726               |

## Analysis

### Comparative Performance

1. **Italy (`46` cities)**
   - **GA**: 4,319.7 km
   - **Greedy**: 4,436.03 km
   - **Observation**: The Genetic Algorithm outperformed the Greedy Algorithm, achieving a lower tour cost despite the relatively small dataset size.

2. **Vanuatu (`8` cities)**
   - **GA**: 1,345.54 km
   - **Greedy**: 1,475.53 km
   - **Observation**: The Genetic Algorithm provided a better solution, reducing the tour cost by approximately 130 km compared to the Greedy approach.

3. **Russia (`167` cities)**
   - **GA**: 49,424.43 km
   - **Greedy**: 42,334.16 km
   - **Observation**: Contrary to expectations, the Greedy Algorithm achieved a lower tour cost than the Genetic Algorithm in this moderately sized dataset.

4. **United States (`326` cities)**
   - **GA**: 76,928.6 km
   - **Greedy**: 48,050.03 km
   - **Observation**: The Greedy Algorithm significantly outperformed the Genetic Algorithm, achieving a substantially lower tour cost.

5. **China (`726` cities)**
   - **GA**: 228,161.52 km
   - **Greedy**: 63,962.92 km
   - **Observation**: The Greedy Algorithm vastly outperformed the Genetic Algorithm, reducing the tour cost by nearly 78,198.6 km.

## References

- [Traveling Salesman Problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem)
- [Genetic Algorithms](https://en.wikipedia.org/wiki/Genetic_algorithm)
- [Greedy Algorithms](https://en.wikipedia.org/wiki/Greedy_algorithm)

---
