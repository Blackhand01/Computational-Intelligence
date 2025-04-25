# Lab 3: Bidirectional A* Search Puzzle Solver

In this project, I completed Lab 3 by implementing a puzzle solver based on the bidirectional A* search algorithm. The goal was to use an efficient approach to solve NxN puzzles (like 3x3 or 4x4), maximizing efficiency in terms of nodes explored versus solution quality.

---

## **State Space**

For a puzzle of size $n^2 - 1$, the total number of possible states is $\frac{(n^2)!}{2}$, as only half of the configurations are solvable.

- **Example:**
  - $3 \times 3$: $\frac{9!}{2} = 181,440$ states.
  - $4 \times 4$: $\frac{16!}{2} \approx 10^{13}$ states.

The size of the state space directly impacts the time and space complexity of search algorithms.
---


### Algorithm Structure
1. **Initial Randomization:** The puzzle state is randomized by performing random moves. The system checks if the generated state is solvable using inversion counting.
2. **Heuristic:** Manhattan distance was chosen as the cost function to estimate the distance to the goal state.
3. **Bidirectional Search:** Two A* searches work simultaneously:
   - One progresses from the initial state toward the goal state.
   - The other starts from the goal state and moves toward the initial state.
4. **Meeting Frontiers:** When the two searches meet, the path is reconstructed by merging the forward and backward solutions.
---

### Results
#### 3x3 Puzzle
- **Solution found in:** 22 steps
- **Quality (Number of steps):** 22
- **Cost (Nodes evaluated):** 296
- **Efficiency (Quality / Cost):** 0.074324

#### 4x4 Puzzle
- **Solution found in:** 52 steps
- **Quality (Number of steps):** 52
- **Cost (Nodes evaluated):** 276746
- **Efficiency (Quality / Cost):** 0.000188

