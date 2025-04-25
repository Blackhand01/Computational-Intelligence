# Chapter 1


## 🏷 **2. Local Search Algorithms**  
**Local search algorithms** are optimization techniques that improve a solution **by iterating over an existing one**.  

💡 **Main Examples:**  
1. **Stochastic Gradient Descent (SGD):** Iterative optimization used in machine learning.  
2. **Hill Climbing:** Gradually improves the current solution step by step.  
3. **Simulated Annealing:** Introduces randomness and "cooling" to escape local minima.  
4. **Tabu Search:** Avoids repeating previous solutions by keeping a short-term memory.  
5. **Genetic Algorithms:** Simulate natural selection to find optimal solutions.  
6. **Particle Swarm Optimization:** Inspired by collective behavior (e.g., bird flocks).  
7. **Nelder-Mead Simplex:** A derivative-free optimization method for complex problems.  

⚠️ **Warning:**  
These algorithms do not always guarantee the **global optimum**, but they provide **good solutions** with an **acceptable computational cost**.  

---

## 🏷 **3. Problem Classification**  
🔹 **Constraint Satisfaction (CSP)**  
   - Goal: Find **any valid solution** (e.g., Sudoku, 8-Queens).  
   - Methods: **Backtracking, Constraint Propagation**.  

🔹 **Optimization**  
   - Goal: Find **the best solution** (e.g., shortest path, minimal cost).  
   - Methods: **Local search, Genetic algorithms, A\***.  

---

## 🤖 **4. Computational Complexity and NP Problems**  
🔹 **NP Problems (Nondeterministic Polynomial-time)**  
   - Problems that can be solved in **polynomial time if the solution is known**.  
   - **NP-Hard:** At least as difficult as NP problems (e.g., *3-SAT*).  
   - **NP-Complete:** NP problems that are also NP-Hard (e.g., *8-Queens*, *Hamiltonian Path*).  

💡 **P vs. NP Dilemma**  
   - If \( P = NP \), hard problems like **factorization** could be solved quickly.  
   - Consequences: Cryptography and cybersecurity would be at risk.  

---

## 🎯 **5. Application Examples**  
### ♟ **Example: 8-Queens Problem**  
- Place 8 queens on a chessboard **without attacking each other**.  
- Type: **Constraint Satisfaction Problem (CSP)**.  
- Approach:  
  1. **Backtracking** → Explores all possible configurations.  
  2. **Heuristics** → Reduces the number of tested configurations.  

### 🏫 **Example: University Scheduling**  
- Creating an **optimal class timetable**, considering:  
  - **Hard constraints:** No overlapping exams.  
  - **Soft constraints:** Minimize empty time slots between lectures.  
- **Solution:** *Genetic Algorithms + Simulated Annealing*.  

---

## 🏷 **6. Black-Box Algorithms and Problem Modeling**  
🔹 **Black-Box Algorithms**  
   - The system is unknown and provides only **outputs given certain inputs**.  
   - Example: **Testing an AI engine without knowing its internal logic**.  

🔹 **Modeling Problems**  
   - Creating a model that correctly maps **inputs to outputs**.  
   - Techniques:  
     1. **Supervised Learning** (Regression, Neural Networks).  
     2. **What-if Analysis** (Simulations for business decisions).  
     3. **Artificial Life** (Simulating biological behaviors).  

---

## 🏔 **7. Fitness Landscape**  
A concept used in **optimization** and **evolutionary computation** to visualize solution quality.  

🔹 **Key Points:**  
- **Local vs. global optima:** Some algorithms may get stuck in **local minima**.  
- **Methods to overcome local optima:**  
  1. **Random mutation** (e.g., Genetic Algorithms).  
  2. **Simulated Annealing** (Controlled randomness).  
  3. **Swarm Intelligence** (e.g., Particle Swarm Optimization).  

---

## 📚 **8. Recommended Reading**  
📖 *The Atrocity Archives* by Charles Stross  
- Sci-fi novel that **mixes AI, computation theory, and Lovecraftian horror**.  
- **Mentions Church-Turing conjecture**: "If \( P = NP \), magic exists!" 😄  

---

### 🔥 **Conclusion**  
📌 This material covers **many key topics** in Computational Intelligence, including:  
- **Optimization and local search algorithms**.  
- **Computational problem classification**.  
- **Real-world problem modeling**.  
- **Advanced concepts like Fitness Landscape and Black-Box AI**.  

👉 **Want to explore a specific topic?** 🚀


# Chapter 2
### 🔍 **Fitness Landscapes and Local Search Algorithms**  
The concept of **Fitness Landscape** is fundamental in *Computational Intelligence*, especially in **local search and evolutionary optimization algorithms**.

---

## 🏔 **1. What are Fitness Landscapes?**  
A *Fitness Landscape* is a **geometric representation of solution quality** in a given optimization problem.

- Each **point** in the landscape represents a **solution**.  
- The **height** of the surface indicates the **fitness function value** (how good the solution is).  
- The **best solutions** are represented by **peaks (optima)**, while the **worst solutions** are found in **valleys**.  

📌 **Usefulness:**  
- Helps understand **how hard it is to optimize a problem**.  
- Allows selecting the best **search algorithm** to explore the landscape.  

---

## 🏷 **2. Local and Global Optima**  
🔹 **Global Optimum**:  
- The **highest peak** in the fitness landscape → **best possible solution**.

🔹 **Local Optima**:  
- **Higher points** on the surface, but **not the absolute maximum**.  
- Problem: **Many local search algorithms get stuck in local optima**.

📌 **Solutions to avoid local optima:**  
1. **Random mutation** → (e.g., Genetic algorithms)  
2. **Simulated annealing** → (e.g., Simulated Annealing)  
3. **Swarm Intelligence** → (e.g., Particle Swarm Optimization)

---

## 🔄 **3. Local Search Algorithms and Fitness Landscapes**  
Local search algorithms aim to **find a better solution** by moving through the fitness landscape.

### 📌 **Examples of Algorithms**  
1. **Hill Climbing**  
   - Iteratively modifies a solution to improve it.  
   - Problem: can get stuck in a *local optimum*.  

2. **Simulated Annealing**  
   - Introduces **random variations** to explore the space better.  
   - Allows escaping local optima by **accepting worse solutions** at first with some probability.  

3. **Genetic Algorithms**  
   - Use **natural selection and mutation** to explore the fitness landscape.  
   - Great for problems with multiple local optima (*multimodal problems*).  

4. **Particle Swarm Optimization (PSO)**  
   - Inspired by the behavior of bird flocks and fish schools.  
   - "Particles" explore the landscape based on their own experience and the experience of other individuals.  

5. **Tabu Search**  
   - Keeps a **list of forbidden moves (tabu)** to avoid cycles and improve exploration.  

---

## ⚠️ **4. Known Problems in Fitness Landscapes**  
📌 **Types of Fitness Landscapes that are difficult to explore:**  
- **Multimodal** → Multiple local optima → *Risk of getting stuck*.  
- **Valleys** → Low-quality solutions → *Hard to climb towards optima*.  
- **Ridges** → Narrow paths between peaks → *Difficult to cross without falling*.  
- **Needle in a Haystack** → "Flat" landscape with only one peak → *Random and hard to find*.  
- **Deceptive Landscapes** → Local optima look like global optima → *Traps for greedy algorithms*.  

---

## 📊 **5. Minimization vs Maximization**  
📌 **How to define the fitness function?**  
- **Mathematicians** and **operations researchers** tend to **minimize** a cost function.  
- **Evolutionary scientists and AI** often try to **maximize** a fitness function.  

🔀 **Common conversions:**  
- \( f(x) = -E(x) \) → Converts a minimization problem into maximization.  
- \( f(x) = K - E(x) \) → Introduces a reference value \( K \) to keep positive values.  
- \( f(x) = \frac{1}{E(x)} \) → Useful when the minimum is \( E(x) = 0 \).  

---

## 🔥 **Conclusion**  
- **Fitness Landscapes** are useful tools to understand the **difficulty of an optimization problem**.  
- **Local search algorithms** aim to **find better solutions** by exploring the landscape.  
- **Complex problems** require **advanced strategies** (mutations, heuristics, hybrid algorithms).

# Chapter 3

### 🔍 **Exploration vs. Exploitation: The Learning Dilemma**  
The concept of **Exploration and Exploitation** is crucial in **decision theory**, *Reinforcement Learning*, **optimization methods**, and even in **evolutionary biology**.

---

## ⚖️ **1. The Exploration vs. Exploitation Dilemma**  
🔹 **Exploration**:  
- Searching for **new information** to **discover** better strategies.  
- Exploring the **solution landscape** without knowing if it will improve the result.  
- *Example:* Trying a new restaurant instead of always going to the same one.  

🔹 **Exploitation**:  
- Making the most of **what is already known** to gain an immediate benefit.  
- Based on **past experiences** to **maximize short-term gains**.  
- *Example:* Ordering the dish you know is the best instead of trying something new.  

📌 **Dilemma:**  
- **Too much exploration** → Wasting time and resources on unnecessary experiments.  
- **Too much exploitation** → Risk of getting stuck in a suboptimal solution.  

---

## 🎰 **2. The Multi-Armed Bandit Problem**  
A classic example to illustrate the dilemma is the **Multi-Armed Bandit Problem**.

🎰 **Scenario:**  
- You are in a casino with **multiple slot machines** (multi-armed bandits).  
- Each machine has an **unknown average payout**.  
- You must decide **which machines to play to maximize your winnings**.  

🛠 **Possible Strategies:**  
1. **Exploration** → Test all the slots to find out which pays the most.  
2. **Exploitation** → Keep playing the slot that has paid the best so far.  

⚠️ **Problem:**  
- **Payouts are only estimates** → **A less played slot might be better!**  
- The optimal strategy is to **balance exploration and exploitation**.

---

## 🤖 **3. Applications in AI and Computational Intelligence**  
📌 **The dilemma is crucial in many areas, including:**

1️⃣ **Reinforcement Learning (RL)**  
   - An agent must **explore** new actions or **exploit** strategies already learned.  
   - Example: **Q-Learning** uses a \( Q(s, a) \) function to choose the best actions but still needs exploration to improve the strategy.  

2️⃣ **Optimization and Evolutionary Algorithms**  
   - **Genetic Algorithms**: Random mutations (*exploration*) vs selecting the best solutions (*exploitation*).  
   - **Simulated Annealing**: Starts with **high exploration**, then gradually switches to **exploitation**.  

3️⃣ **Graph Search (Pathfinding, A\*)**  
   - **A\*** balances search between actual cost \( g(n) \) and a heuristic estimate \( h(n) \).  
   - **Dijkstra** uses only **exploitation**, while **Greedy Best-First Search** uses only **exploration**.  

4️⃣ **Recommendation Systems (Netflix, YouTube, Spotify)**  
   - **Exploration**: Suggest new and unseen content.  
   - **Exploitation**: Suggest content the user has already liked.  

---

## 📊 **4. Strategies for Balancing Exploration and Exploitation**  
🔹 **ϵ-Greedy Policy**  
   - With probability \( \epsilon \), the agent **explores** randomly.  
   - With probability \( 1 - \epsilon \), it **exploits** the best known option.  
   - *Example:* **ϵ = 0.1** → 10% of the time it tries new actions.  

🔹 **Upper Confidence Bound (UCB)**  
   - Balances exploration and exploitation **adaptively**, increasing exploration when uncertainty is high.  

🔹 **Thompson Sampling**  
   - Uses **probability distributions** to decide between exploration and exploitation.  

---

## 🌍 **5. Connections with Biology and Artificial Intelligence**  
📌 **Biology:**  
- **Natural evolution** balances exploration (*random mutations*) and exploitation (*natural selection*).  
- **Social organisms** explore new resources but also exploit those already known.  

📌 **AI & Machine Learning:**  
- **Deep Learning**: Neural network training can **experiment with new configurations** (*exploration*) or refine existing weights (*exploitation*).  

📌 **Economics and Finance:**  
- **Investments**: Balancing **safe actions (exploitation)** with **high-risk, innovative investments (exploration)**.  

---

## 🔥 **Conclusion**  
- The **Exploration vs. Exploitation** dilemma is omnipresent in **AI, optimization, and biology**.  
- A good balance between **discovering new opportunities** and **exploiting current knowledge** is **key for optimal decisions**.  
- **Strategies like ϵ-Greedy, UCB, and Thompson Sampling** help manage this trade-off.


# Chapter 4

### 🔍 **Hill Climbing: Local Search Algorithm**  
**Hill Climbing** is a **local search algorithm** used for optimization and artificial intelligence. It is a **greedy** method that iteratively improves a solution by **exploring neighboring solutions** and only accepting improvements.

---

## ⚡ **1. Basic Concepts**  
### 📌 **Key Features:**
- **Local search algorithm** → Works on a single solution, not a population.  
- **Greedy** → Only accepts better solutions compared to the current one.  
- **Does not use gradients** → Unlike *gradient descent*, it works on discrete spaces as well.

### 📌 **Basic Structure of the Algorithm:**
1️⃣ **Initialization** → Start with a random solution.  
2️⃣ **Generate neighbors** → Explore **similar solutions**.  
3️⃣ **Evaluation** → Choose the best available neighbor.  
4️⃣ **Termination** → Stops when:
   - No improvements are found (*local optimum*).  
   - A maximum number of iterations is reached.  
   - A stopping condition is met (*maximum time*).  

---

## 🔄 **2. Types of Hill Climbing**  
### 🏷 **Main Variants**
1️⃣ **First-Improvement Hill Climber (Random Mutation Hill Climber, RMHC)**  
   - Chooses the first improvement it finds.  
   - Faster but can get stuck in local optima.

2️⃣ **Steepest-Ascent Hill Climber**  
   - Evaluates **all neighbors** and picks the best one.  
   - More effective but computationally more expensive.

3️⃣ **Stochastic Hill Climbing**  
   - Chooses a neighbor **randomly**, with a higher probability for better ones.  
   - Avoids getting stuck in local optima, but is less efficient.

### 🛠 **Improvements and Techniques to Avoid Problems**
📌 **To escape local optima**:
- **Random restarts** → If stuck, restart from scratch.  
- **Simulated Annealing** → Accept temporary worsened solutions to escape local optima.  
- **Tabu Search** → Keeps a memory of visited states to avoid cycles.

---

## 🎰 **3. Applications and Common Problems**  
### 📌 **Problems Solvable with Hill Climbing**
🔹 **Knapsack Problem**  
   - Select objects with weight and value constraints.  
   - Hill Climbing improves an initial solution iteratively.  

🔹 **One-Max Problem**  
   - Optimize a binary string to maximize the number of "1"s.  
   - Used as a benchmark to compare algorithms.  

🔹 **Set Cover Problem**  
   - Find the smallest subset of sets that covers a domain.  
   - **NP-Complete** problem, Hill Climbing can find approximate solutions.  

🔹 **Optimization Functions (Continuous Spaces)**  
   - Extend Hill Climbing to continuous spaces with **Gaussian Mutation** and evolutionary strategies.

---

## ⚠️ **4. Problems of Hill Climbing**  
📌 **Limitations:**
1. **Local Optima** → The algorithm stops as soon as it finds a local maximum.  
2. **Plateau** → A region with no significant improvements, can slow down the search.  
3. **Deception** → Misleading fitness functions lead in the wrong direction.  

📌 **Solutions:**
- **Stochastic methods** (*Random Restart, Simulated Annealing*).  
- **Multi-start Hill Climbing** (*Iterated Local Search*).  
- **Evolutionary methods** (*Genetic Algorithms, Evolution Strategies*).

---

## 🔥 **Conclusion**  
**Hill Climbing** is a powerful yet simple technique for optimization. However, it can be improved with advanced strategies to avoid getting stuck in local optima.

🚀 **Question for you:**  
If you had to solve a **university timetable optimization problem**, which variant of Hill Climbing would you use and why?

# Chapter 5

### 🔥 **Simulated Annealing (SA)**  
**Simulated Annealing (SA)** is a **global optimization algorithm** inspired by the **metallurgical annealing process**, formalized in the 1980s by **Kirkpatrick et al.**. It is a variant of **Hill Climbing**, but with the ability to temporarily accept worse solutions to **avoid local optima**.

---

## 📌 **1. Basic Principle**  
Simulated Annealing is inspired by **metal annealing**, a process where a material is heated and then slowly cooled to reach a stable, optimal state.

🔹 **Analogy with optimization**:  
- **High temperature** → The system freely explores the solution space.  
- **Low temperature** → The system stabilizes on an optimal solution.  

📌 **Key difference from Hill Climbing**:  
- Hill Climbing accepts **only improvements**.  
- Simulated Annealing accepts **temporary worsened solutions**, with a probability depending on the temperature.

---

## 🔄 **2. How the Algorithm Works**  
### 📌 **Simulated Annealing Steps**  
1️⃣ **Initialization**  
   - Start with a random initial solution.  
   - Set an initial high temperature \( T \).

2️⃣ **Generate a new solution**  
   - Generate a new solution in the vicinity of the current solution.

3️⃣ **Accept the new solution**  
   - If the new solution is **better**, it is accepted.  
   - If it is **worse**, it can be accepted with probability:  
     \[
     p = e^{-\frac{\Delta f}{T}}
     \]
     where:
     - \( \Delta f = f(s') - f(s) \) is the difference in quality between the new and old solution.  
     - \( T \) is the current temperature.

4️⃣ **Update the temperature**  
   - Gradually reduce the temperature following a **schedule**.

5️⃣ **Termination condition**  
   - The process stops when the temperature reaches a minimum value or after a maximum number of iterations.

---

## ⚡ **3. Cooling Strategy**  
The **cooling schedule** is crucial for the algorithm's success.

📌 **Common strategies**:  
- **Exponential**: \( T_{k+1} = \alpha T_k \), with \( \alpha \) close to 1 (e.g., 0.99).  
- **Linear**: \( T_{k+1} = T_k - \beta \).  
- **Logarithmic**: \( T_{k+1} = \frac{T_0}{1 + k} \), slower but guarantees theoretical convergence.

💡 **Trade-off**:  
- **Slow cooling** → More exploration, but requires more time.  
- **Fast cooling** → Less exploration, but might stop at a local optimum.

---

## 🎯 **4. Applications and Advantages**  
📌 **Application examples**:  
1. **Combinatorial optimization** → NP-hard problems like the *Traveling Salesman Problem (TSP)*.  
2. **Machine Learning** → Hyperparameter optimization in machine learning models.  
3. **Industrial design** → Optimization of electronic circuit layout.  
4. **Scheduling** → Creating optimized schedules for businesses or universities.

📌 **Advantages over Hill Climbing**:  
✅ **Avoids local optima** by accepting temporary worsened solutions.  
✅ **Works on both continuous and discrete search spaces**.  
✅ **Adapts to complex problems with many variables**.

📌 **Disadvantages**:  
❌ **Requires choosing a good temperature schedule**.  
❌ **Does not guarantee finding the global optimum**.

---

## 🔥 **Conclusion**  
Simulated Annealing is a versatile algorithm for complex optimization problems. The key to its success lies in the proper management of the temperature.


# Chapter 6
### 🔍 **Continuous Search Spaces and Evolutionary Strategies**  
In **continuous optimization problems**, the solutions are not discrete but belong to a **continuous domain** (e.g., real numbers). Algorithms like **classic Hill Climbing** don't work well in these scenarios, so specific techniques, such as **Evolution Strategies (ES)**, are used.

---

## 📌 **1. Optimization in Continuous Search Spaces**  
🔹 **Definition:**  
In a **continuous search space**, each solution is represented by a list of **real numbers** (*floating point*).  

🔹 **Examples of problems in continuous spaces:**  
- **Optimization of hyperparameters in machine learning models**.  
- **Trajectory control in robotics**.  
- **Physical simulations and modeling of complex systems**.  

📌 **Main challenge:**  
Discrete methods **cannot be used directly** because the moves between neighbors are less defined. **Random mutations and adaptation strategies** become crucial.

---

## 🚀 **2. Evolution Strategies (ES)**  
🔹 **Evolution Strategies (ES)** are a family of optimization algorithms for continuous spaces, based on:
- **Gaussian mutation** \( x' = x + N(0, s) \).
- **Fitness-based selection**.
- **Self-adaptation of parameters**.

📌 **Main variants of ES:**
1. **(1+1)-ES** → One parent, one child per generation.  
2. **(1+λ)-ES** → One parent, multiple children per generation.  
3. **(μ,λ)-ES** → Multiple parents, multiple children (comma strategy).  
4. **(μ+λ)-ES** → Multiple parents, multiple children (plus strategy).

---

## 🔄 **3. Details of Evolution Strategies**  
### 📌 **(1+1)-ES (First-Improvement Hill Climber)**  
- A version of Hill Climbing with **Gaussian mutations**.  
- Each element of the solution is modified by:  
  \[
  x_i' = x_i + N(0, s)
  \]  
  where \( s \) is the *mutation step*.  
- If the new candidate is **better**, it is accepted.

📌 **1/5 Success Rule**  
- If more than **20%** of mutations are beneficial, **decrease \( s \)**.  
- If fewer than **20%** are beneficial, **increase \( s \)**.  
- Maintains a good balance between **exploration and exploitation**.

---

### 📌 **(1+λ)-ES and (1,λ)-ES**  
- **(1+λ)-ES:** The parent remains in memory and can be chosen for the next iteration.  
- **(1,λ)-ES:** The parent is always replaced by the best solution among the children.

📌 **Comma vs Plus Strategy**  
| Strategy | Parent Replacement | Advantages | Disadvantages |  
|----------|--------------------|------------|---------------|  
| **(μ,λ)-ES** | Only the best children replace parents (comma) | Avoids stagnation risk | Can lose good solutions quickly |  
| **(μ+λ)-ES** | The best between parents and children survive (plus) | Preserves good solutions longer | May become less exploratory |

---

## 🔄 **4. Self-Adaptation of Mutation**  
📌 **Self-adaptation of the step \( s \)**  
- **Problem:** Dynamically choosing \( s \) to avoid too small steps (slow convergence) or too large steps (unnecessary jumps).  
- **Solution:** **Self-adaptation**, where \( s \) is optimized alongside the solution.

📌 **Advanced strategies:**  
1. **Self-adaptation for each variable** → Different \( s_i \) for each variable.  
2. **Global learning rates** → Two learning rates to control global mutation and specific variables.  
3. **Covariance Matrix Adaptation (CMA-ES)** → Models correlations between variables for more efficient search.

---

## 🔥 **5. Comparison with Other Algorithms**  
| Algorithm | Search Space | Strategies | When to use it? |  
|-----------|--------------|------------|-----------------|  
| **Hill Climbing** | Discrete | Pure exploitation | When the problem is well-modeled with few local optima |  
| **Simulated Annealing** | Discrete or continuous | Decreasing exploration | When avoiding local optima without a population |  
| **Evolution Strategies (ES)** | Continuous | Selection, mutation, and adaptation | When working with real numbers and seeking self-adaptation strategies |  
| **Genetic Algorithms** | Discrete or continuous | Crossover and mutation | When solutions need exploratory combinations of traits |

---

## 🎯 **6. Applications of Evolution Strategies**  
✅ **Deep neural network optimization** (for tuning hyperparameters).  
✅ **Robotics** → Improving trajectories and movements.  
✅ **Computer Vision** → Optimizing filters and image segmentation.  
✅ **Financial modeling** → Trading strategies based on stochastic simulations.

---

## 🔥 **Conclusion**  
📌 In continuous problems, **Evolution Strategies** outperform Hill Climbing due to **Gaussian mutation, self-adaptation, and population management**.


# Chapter 7
### 🔍 **Traits, Genetic Selection, and Evolutionary Algorithms**  
In **evolutionary methods**, the concept of **traits** plays a fundamental role. Natural selection favors **phenotypes** that increase fitness, and **genetic operators** must maintain the correspondence between **genotype and phenotype**.

---

## 📌 **1. Key Concepts**  
🔹 **Traits (Phenotypic Traits)**  
- **Traits associated with high fitness** lead to **greater reproductive success**.  
- **Genetic operators** (mutation, crossover) act at the **genotype level**, but they must maintain **phenotypic significance**.  
- Traits must be **heritable** for evolutionary selection to function.

🔹 **State Space vs. Problem Space**  
- The **genotype encoding** and **genetic operators** are **interconnected**.  
- The **fitness landscape** describes the **state space**, not directly the **problem space**.

---

## 🧬 **2. Evolutionary Algorithms and Main Components**  
**Evolutionary Algorithms (EA)** are optimization methods inspired by natural selection.

📌 **Phases of an EA:**
1. **Initialization** → Creation of the initial population.  
2. **Parent Selection** → The fittest individuals have a higher chance of reproducing.  
3. **Reproduction** → Application of genetic operators (*crossover*, *mutation*).  
4. **New Generation Selection** → Individuals with **better fitness** survive.

📌 **Parents and Offspring:**
- **Available genetic material** → Parents selected for reproduction.  
- **Fitness-proportional selection** → The stronger the individual, the higher the probability of reproduction.

---

## 🎰 **3. Selection Strategies in EAs**  
### 📌 **Selection Methods**  
1️⃣ **Fitness-Proportional Selection (Roulette Wheel)**  
   - The selection probability is proportional to fitness \( f_i \).  
   - Problem: **Low selection pressure in large populations**.

2️⃣ **Rank-Based Selection**  
   - Rank the population and select based on rank, not absolute fitness.  
   - **Advantage:** Avoids disproportionate fitness problems.

3️⃣ **Tournament Selection**  
   - Randomly select \( \tau \) individuals and choose the best.  
   - **Advantage:** Does not require global sorting.

4️⃣ **Uniform Selection**  
   - Each individual has an equal probability of being selected.  
   - **Used in Evolution Strategies (ES)** to maintain diversity.

📌 **Variants of Fitness-Proportional Selection:**  
- **Windowing** → Normalizes fitness by subtracting the lowest value.  
- **Sigma Scaling** → Balances selection considering population variance.

---

## 🔄 **4. Population Management Models**  
📌 **Two main models:**  
1️⃣ **Generational Model (μ, λ)**  
   - The entire population is replaced every generation.  
   - **Typical in Genetic Algorithms (GA)**.  
   - **Example:** \( \lambda = 7\mu \) (7 offspring per parent).

2️⃣ **Steady-State Model (μ+λ)**  
   - Offspring compete against parents for survival.  
   - **Used in Evolution Strategies (ES)**, maintains more diversity.  
   - **Example:** \( \mu > \lambda \), such as \( \mu = 30, \lambda = 20 \).

📌 **What happens with aging?**  
- **Generational Model** → Maximum age = 1.  
- **Steady-State Model** → Maximum age = ∞.  
- **Mixed strategies** → Combine **conditioned aging** with elitism.

---

## 🧬 **5. Genetic Operators: Crossover and Mutation**  
📌 **Crossover: Genetic recombination**  
- **1-point crossover** → One cut point, offspring combine sections.  
- **2-point crossover** → Two cut points, more structured exchange.  
- **Uniform crossover** → Each gene is inherited randomly from a parent.

📌 **Mutation: Random variation**  
- **Bit Flip (for binary strings)** → Change 0 ↔ 1.  
- **Gaussian Mutation (for real numbers)** → Adds a random variation.  
- **Swap Mutation (for permutations)** → Swaps two elements.  
- **Scramble Mutation** → Randomly reorders a subsequence.

📌 **Effect of mutations**  
- **Small mutations** → Favor **local exploitation**.  
- **Large mutations** → Favor **global exploration**.

---

## 🚀 **6. Applications of EAs**  
✅ **Combinatorial optimization** (Traveling Salesman Problem, Set Cover).  
✅ **Machine Learning** (hyperparameter optimization).  
✅ **Robotics** (evolution of control strategies).  
✅ **Biological modeling** (evolutionary simulations).

📌 **Difference with other approaches**  
| Approach | Type of Space | Strategies |  
|----------|---------------|------------|  
| **Hill Climbing** | Discrete | Pure exploitation |  
| **Simulated Annealing** | Discrete or continuous | Adaptive exploration |  
| **Evolution Strategies** | Continuous | Mutation and selection |  
| **Genetic Algorithms** | Discrete | Crossover and mutation |

---

## 🔥 **Conclusion**  
📌 **Evolutionary Algorithms (EA)** combine **selection, crossover, and mutation** to iteratively improve solutions. Strategies like **elitism, rank-based selection, and self-adaptive mutation** enhance convergence.



# Chapter 8

### 🔍 **Evolutionary Programming (EP): Evolution-Based Optimization**  
**Evolutionary Programming (EP)** is an **evolutionary optimization technique** developed in the 1960s by **D. Fogel**, initially applied to **prediction based on Finite State Machines (FSM)**. Unlike **Genetic Algorithms (GA)** and **Evolution Strategies (ES)**, EP focuses on **mutation** without the use of **crossover**.

---

## 📌 **1. Key Characteristics of EP**  
🔹 **Origins and Philosophy:**  
- **Originally designed to study intelligence** as the **capacity for adaptation**.  
- **Based on environmental prediction** as a prerequisite for adaptation.

🔹 **Key Elements:**  
| Component | Evolutionary Programming |  
|-----------|--------------------------|  
| **Representation** | Real number vectors or FSMs |  
| **Recombination** | None (No crossover) |  
| **Mutation** | Gaussian perturbation |  
| **Population Model** | **Steady-State** \((\mu + \mu)\) |  
| **Parent Selection** | Deterministic |  
| **Survival Selection** | **Q-tournament** |

🔹 **Difference from other EAs:**  
- **No crossover** → Unlike GA, EP does not use crossover, relying exclusively on mutations.  
- **Limited self-adaptation** → Unlike ES, parameter adaptation is not internal to the system.  
- **Closer to evolutionary strategies** → Over time, EP absorbed characteristics from ES.

---

## 🧬 **2. EP Evolution: From FSMs to Numerical Optimization**  
📌 **Historical EP: Prediction with FSMs**  
- **Finite State Machines (FSM)** were evolved to predict data sequences.  
- An FSM had:  
  - **States \( S \)**  
  - **Input \( I \)**  
  - **Output \( O \)**  
  - **Transition function** \( \delta : S \times I \to S \times O \).

📌 **Modern EP: Numerical Optimization**  
- EP was later adapted for **numerical problems**, with **real-number vector representation**.  
- **Mutation as the primary operator**:  
  - Each element of the solution is perturbed with a **Gaussian mutation**:  
    \[
    x' = x + N(0, \sigma)
    \]  
  - Where \( \sigma \) is the **mutation step** (variance of the distribution).

---

## 🔄 **3. EP Process**  
📌 **EP Evolution Phases**  
1️⃣ **Initialization** → Creation of a population of random solutions.  
2️⃣ **Offspring Generation** → Each individual generates an offspring by applying **mutations**.  
3️⃣ **Survival Selection** → **Q-Tournament Selection**:  
   - **q individuals are selected randomly** and the best one is chosen.  
   - **Favors stronger individuals**, but maintains diversity.  
4️⃣ **Iteration until stopping criterion** → Maximum time or population convergence.

---

## ⚖️ **4. Comparison with Other Evolutionary Algorithms**  
📌 **Differences with ES and GA**  
| Algorithm | Crossover | Mutation | Parameter Adaptation | Selection |  
|-----------|-----------|----------|----------------------|-----------|  
| **GA** | ✅ Yes | ✅ Yes | ❌ No | Fitness-Proportional |  
| **ES** | ❌ No | ✅ Yes | ✅ Self-Adaptive | Deterministic |  
| **EP** | ❌ No | ✅ Yes | ❌ No | **Q-Tournament** |

📌 **When to Choose EP?**  
- **When crossover doesn’t make sense** (e.g., evolution of FSMs).  
- **When you want a simple mutation-based approach**.  
- **When the problem is highly stochastic**, and crossover might reduce diversity.

---

## 🎯 **5. Applications of EP**  
✅ **Sequential prediction** (e.g., learning patterns in data).  
✅ **Optimization of non-differentiable functions**.  
✅ **Evolution of game strategies** (e.g., neural networks for checkers).  
✅ **Biological simulations** (environmental adaptation models).

📌 **Real Example:**  
- An **EP-evolved program** learned to play **checkers** without expert knowledge, defeating **99.61% of human players** after 6 months of evolution.

---

## 🔥 **Conclusion**  
📌 **Evolutionary Programming** is a powerful optimization method based on **Gaussian mutation and tournament selection**. It does not use crossover and is particularly effective for **prediction problems and numerical optimization**.


# Chapter 9

### 🔍 **Evolutionary Programming (EP): Evolution-Based Optimization**  
**Evolutionary Programming (EP)** is an **evolutionary optimization technique** developed in the 1960s by **D. Fogel**, initially applied to **prediction based on Finite State Machines (FSM)**. Unlike **Genetic Algorithms (GA)** and **Evolution Strategies (ES)**, EP focuses on **mutation** without the use of **crossover**.

---

## 📌 **1. Key Characteristics of EP**  
🔹 **Origins and Philosophy:**  
- **Originally designed to study intelligence** as the **capacity for adaptation**.  
- **Based on environmental prediction** as a prerequisite for adaptation.

🔹 **Key Elements:**  
| Component | Evolutionary Programming |  
|-----------|--------------------------|  
| **Representation** | Real number vectors or FSMs |  
| **Recombination** | None (No crossover) |  
| **Mutation** | Gaussian perturbation |  
| **Population Model** | **Steady-State** \((\mu + \mu)\) |  
| **Parent Selection** | Deterministic |  
| **Survival Selection** | **Q-tournament** |

🔹 **Difference from other EAs:**  
- **No crossover** → Unlike GA, EP does not use crossover, relying exclusively on mutations.  
- **Limited self-adaptation** → Unlike ES, parameter adaptation is not internal to the system.  
- **Closer to evolutionary strategies** → Over time, EP absorbed characteristics from ES.

---

## 🧬 **2. EP Evolution: From FSMs to Numerical Optimization**  
📌 **Historical EP: Prediction with FSMs**  
- **Finite State Machines (FSM)** were evolved to predict data sequences.  
- An FSM had:  
  - **States \( S \)**  
  - **Input \( I \)**  
  - **Output \( O \)**  
  - **Transition function** \( \delta : S \times I \to S \times O \).

📌 **Modern EP: Numerical Optimization**  
- EP was later adapted for **numerical problems**, with **real-number vector representation**.  
- **Mutation as the primary operator**:  
  - Each element of the solution is perturbed with a **Gaussian mutation**:  
    \[
    x' = x + N(0, \sigma)
    \]  
  - Where \( \sigma \) is the **mutation step** (variance of the distribution).

---

## 🔄 **3. EP Process**  
📌 **EP Evolution Phases**  
1️⃣ **Initialization** → Creation of a population of random solutions.  
2️⃣ **Offspring Generation** → Each individual generates an offspring by applying **mutations**.  
3️⃣ **Survival Selection** → **Q-Tournament Selection**:  
   - **q individuals are selected randomly** and the best one is chosen.  
   - **Favors stronger individuals**, but maintains diversity.  
4️⃣ **Iteration until stopping criterion** → Maximum time or population convergence.

---

## ⚖️ **4. Comparison with Other Evolutionary Algorithms**  
📌 **Differences with ES and GA**  
| Algorithm | Crossover | Mutation | Parameter Adaptation | Selection |  
|-----------|-----------|----------|----------------------|-----------|  
| **GA** | ✅ Yes | ✅ Yes | ❌ No | Fitness-Proportional |  
| **ES** | ❌ No | ✅ Yes | ✅ Self-Adaptive | Deterministic |  
| **EP** | ❌ No | ✅ Yes | ❌ No | **Q-Tournament** |

📌 **When to Choose EP?**  
- **When crossover doesn’t make sense** (e.g., evolution of FSMs).  
- **When you want a simple mutation-based approach**.  
- **When the problem is highly stochastic**, and crossover might reduce diversity.

---

## 🎯 **5. Applications of EP**  
✅ **Sequential prediction** (e.g., learning patterns in data).  
✅ **Optimization of non-differentiable functions**.  
✅ **Evolution of game strategies** (e.g., neural networks for checkers).  
✅ **Biological simulations** (environmental adaptation models).

📌 **Real Example:**  
- An **EP-evolved program** learned to play **checkers** without expert knowledge, defeating **99.61% of human players** after 6 months of evolution.

---

## 🔥 **Conclusion**  
📌 **Evolutionary Programming** is a powerful optimization method based on **Gaussian mutation and tournament selection**. It does not use crossover and is particularly effective for **prediction problems and numerical optimization**.

🚀 **Question for you:**  
If you had to optimize a **financial trading strategy**, would you use **EP or Genetic Algorithms**? Why?

# Chapter 10
### 🔍 **Multi-Objective Evolutionary Algorithms (MOEA)**  
**Multi-Objective Evolutionary Algorithms (MOEA)** are a class of evolutionary optimization algorithms designed to solve **problems with multiple conflicting objectives**. Unlike standard optimization algorithms, MOEAs aim to find **a set of optimal solutions** rather than a single solution.

---

## 📌 **1. Multi-Objective Problems**  
A multi-objective problem has **multiple objective functions** to optimize simultaneously.  

🔹 **Examples of multi-objective problems:**  
1. **Buying a car** → Optimize **speed vs. price vs. reliability**.  
2. **Engineering design** → **Lightness vs. Strength**.  
3. **Investment management** → **Maximize return vs. Minimize risk**.  

📌 **Two key challenges:**  
1. **Finding a good set of solutions**.  
2. **Selecting the best solution for a specific application**.  

---

## ⚖️ **2. Pareto Optimality and Dominance**  
📌 **Concept of Dominance:**  
- A solution \( x \) **dominates** \( y \) if:  
  1. \( x \) is better than \( y \) in at least one objective.  
  2. \( x \) is not worse than \( y \) in all other objectives.  
- A **non-dominated set of solutions** is called the **Pareto-optimal set**.  
- The **Pareto-optimal front** is the graphical representation of the optimal set.

🔹 **Example:**  
If we want to **minimize cost** and **maximize quality**, an economical but poor solution **does not dominate** an expensive but high-quality solution.

---

## 🔄 **3. Evolutionary Strategies in MOEAs**  
📌 **Approaches to maintaining population diversity:**  
- **Fitness Sharing** → Penalizes solutions that are too close to each other.  
- **Niching** → Divides the space into regions and limits occupation.  
- **Elitist Archives** → Maintains a secondary population with the best non-dominated solutions.

📌 **Common methods in MOEAs:**  
1️⃣ **NSGA-II (Non-Dominated Sorting Genetic Algorithm II)**  
   - Sorting solutions based on Pareto dominance.  
   - Uses crowding distance to maintain diversity.

2️⃣ **SPEA2 (Strength Pareto Evolutionary Algorithm 2)**  
   - Maintains an elitist archive of non-dominated solutions.  
   - Uses a fitness mechanism based on dominance.

3️⃣ **PAES (Pareto Archived Evolution Strategy)**  
   - Algorithm based on Evolution Strategies.  
   - Maintains a limited archive to ensure diversity.

---

## 🎯 **4. Advantages of the Evolutionary Approach in MOEAs**  
📌 **Why use Evolutionary Algorithms (EA) in multi-objective problems?**  
✅ **Parallel search** → The population simultaneously explores many possible solutions.  
✅ **No need for a priori weighting** → Objectives do not need to be balanced before optimization.  
✅ **Handles non-convex Pareto fronts** → Works even for problems with complex shapes.  
✅ **Maintains diversity** → EAs can find multiple diverse, high-quality solutions.

📌 **When to avoid MOEA?**  
❌ If the problem has **few objectives** and they can be combined with weights.  
❌ If the **fitness calculation is very expensive**, as EAs require many evaluations.

---

## 🚀 **5. Applications of MOEAs**  
✅ **Industrial optimization** → Aircraft design with trade-offs between weight, cost, and strength.  
✅ **Bioinformatics** → Drug design optimizing efficacy and toxicity.  
✅ **Finance** → Creation of portfolios balanced between risk and return.  
✅ **Robotics** → Control optimization between **energy consumption and performance**.

---

## 🔥 **Conclusion**  
📌 **Multi-Objective Evolutionary Algorithms (MOEA)** are powerful tools for solving complex problems with **multiple conflicting objectives**. **Pareto dominance** and the use of **evolutionary strategies** enable finding a **set of optimal solutions**, allowing users to choose the one best suited for their problem.

# Chapter 11

### 1. **Motivation and Context**  
- **Diversity in Nature and EAs:**  
  - **Nature:** The vast diversity of forms (ranging from species variety to Darwin's "Tree of Life") is essential for reducing competition and exploiting different ecological niches.  
  - **Evolutionary Algorithms (EAs):** Similarly, promoting diversity in EAs is crucial to avoid **premature convergence** (when the population gets stuck in suboptimal solutions) and to make the most of the search space.

- **Definition of Diversity:**  
  - Diversity can be evaluated at different levels:  
    - **Genotype:** The internal representation of the individual (e.g., edit distance, frequency of subtrees in GP).  
    - **Phenotype:** The actual solution obtained from transforming the genotype (often linked to performance on the problem).  
    - **Fitness:** The measured value indicating how well a solution solves the problem, although it might not capture structural variation by itself.

---

### 2. **Mechanisms and Strategies to Promote Diversity**  
Methods for promoting diversity can be classified based on the type of information (genotype, phenotype, lineage) and the level at which they intervene (selection, reproduction, replacement). Here are some examples:

- **Population Structure-Based Techniques:**  
  - **Island Model:** The population is divided into subpopulations (islands) that evolve in isolation with occasional exchange of individuals.  
  - **Segregation:** Similar to the island model, but with periodic merging of subpopulations to reduce selective pressure and encourage new explorations.

- **Niching Techniques (Creating Niches):**  
  - **Fitness Sharing:** Modifies the fitness function to penalize solutions that are too similar, lowering their value in overcrowded areas.  
  - **Clearing:** Within a niche (defined by a radius or similarity threshold), only the best \( k \) individuals retain their fitness, while the rest are "reset."  
  - **Crowding & Deterministic Crowding:** Techniques where offspring primarily compete with parents or similar individuals, thereby maintaining diverse areas of search.

- **Other Specific Approaches:**  
  - **Lexicase Selection:** Randomly orders fitness components and compares individuals lexicographically to select those performing well on different sub-objectives.  
  - **Restricted Tournament Selection:** Compares a new individual with the most similar one from a random subset, favoring the survival of different solutions.  
  - **Diversifiers and Random Immigrants:** Randomly introduce new individuals to "inject" novelty into the population.  
  - **Extinction:** In convergence situations, a significant portion of the population is eliminated to make room for new individuals and stimulate exploration.

- **Lineage and Genotype-Based Approaches:**  
  - **Lineage-Based Methodologies:** Use information about the birth history of individuals (time, position in the population) to promote diversity, regardless of their current state.  
  - **Genotypic Distances:** Calculate metrics (e.g., Levenshtein distance, entropy) to assess how different two individuals are, then apply these to modify selection probabilities.

---

### 3. **Measuring Diversity**  
- **Metrics and Concepts:**  
  - **Diversity** is often defined in terms of distance from a set or an individual.  
  - Measurements can be based on:  
    - **Genotype:** Measuring direct variation in the internal representation.  
    - **Phenotype:** Using, for example, the distance between solutions or variability in behaviors.  
    - **Fitness:** While less direct, it can be considered as a proxy if different fitness values imply structurally different solutions.

- **Challenges:**  
  - Defining "similarity" and "diversity" is problematic and heavily depends on the problem nature and the representation of individuals.

---

### 4. **Hints and Practical Tips**  
- **Check Need vs. Problem Composition:**  
  - Often, problems in EAs are caused by poorly designed fitness functions; before implementing mechanisms to increase diversity, it is helpful to verify whether the problem is formulated correctly.  
  - Running multi-start experiments can reveal if intrinsic diversity is sufficient.

- **Practical Suggestions to Promote Diversity:**  
  - **Periodic Extinction:** A "breath of fresh air" to remove overly dominated solutions.  
  - **Lexicase Selection:** Particularly effective when fitness is an aggregate of multiple components.  
  - **Island or Segregation Models:** Useful for exploiting different niches if managed properly (e.g., well-calibrated migrations).  
  - **Fitness Holes and Real Niching:** Tactics that directly modify selection probabilities based on local density.

---

### 5. **Conclusion**  
- **Final Objective:**  
  - Optimization aims to find better solutions in the shortest time possible; promoting diversity is a **means** to avoid premature convergence and allow for better exploration of the search space.  
- **Diversity Mechanisms:**  
  - The techniques presented operate at different levels (genotype, phenotype, lineage) and can be implemented explicitly (fitness sharing, clearing) or implicitly (island model, crowding).  
- **Choosing the Technique:**  
  - It strongly depends on the problem, the structure of the fitness function, and the availability of a reliable metric to measure diversity.

---

# Chapter 12
### 🔍 **Searching for a Path and Problem Solving in Computational Intelligence**  
**Path Search** is a fundamental concept in *Computational Intelligence*, used to **solve problems** by finding a sequence of actions that lead from the initial state to the goal state.

---

## 📌 **1. Basic Assumptions in Search Problems**  
A search problem is characterized by several key properties:  

🔹 **Sequentiality** → The solution is a **sequence of steps**.  
🔹 **Observability** → All relevant information is **known**.  
🔹 **Determinism** → The effects of actions are **predictable**.  
🔹 **Staticity** → Time **does not affect** action selection.  
🔹 **Discreteness** → The set of actions is **enumerable**.  

📌 **Note**: Only one actor is active → No interaction with other agents.

---

## 🏷 **2. Search Problems: Key Concepts**  
🔹 **Problem vs. State Space vs. Solution Space**  
- **Problem** → Defines the initial and goal states, plus the rules to move between them.  
- **State Space** → Set of all possible reachable states.  
- **Solution Space** → Sequence of actions that leads to the goal.  

🔹 **Search as Problem Solving**  
- **The agent must decide at each step which action to perform**.  
- **Example:** Path from Arad to Bucharest, exploring possible intermediate cities.

---

## 🔄 **3. Search Strategies**  
### 📌 **Uninformed Search Strategies**  
These algorithms **do not use additional information** about the goal's location.  

1️⃣ **Breadth-First Search (BFS)**  
   - Expands nodes level by level.  
   - **Complete** (if the search space is finite).  
   - **Optimal** (if all costs are equal).  
   - **Time/Space: \(O(b^d)\)** (where \( b \) is the branching factor and \( d \) is the depth of the solution).

2️⃣ **Depth-First Search (DFS)**  
   - Explores deep before backtracking.  
   - **Not optimal**, can get stuck in cycles.  
   - **Space \( O(bd) \)** (very memory efficient).

3️⃣ **Uniform-Cost Search (Dijkstra’s Algorithm)**  
   - Always expands the node with the lowest cost.  
   - **Optimal** even with different costs.  
   - **Space: \(O(b^d)\)** (similar to BFS, but with a priority queue).

---

### 📌 **Informed Search Strategies**  
Use **heuristics** to guide the search.  

1️⃣ **Greedy Best-First Search**  
   - Expands the node with **lowest heuristic cost** \( h(n) \).  
   - **Fast but not optimal** (can get stuck in local minima).

2️⃣ **A\* Search**  
   - Uses the evaluation function:  
     \[
     f(n) = g(n) + h(n)
     \]  
   - **Optimal if \( h(n) \) is admissible** (does not overestimate the cost).  
   - **Expands the minimum number of nodes possible**, guaranteeing optimality.

3️⃣ **Beam Search**  
   - Optimized version of BFS with a limit on the number of nodes explored per level.  
   - **Not complete** if the limit is too restrictive.

---

## 🌍 **4. Advanced Strategies**  
### 📌 **Bidirectional Search**  
- Starts **two simultaneous searches**: one **from the initial node** and one **from the goal node**.  
- **Advantages:** Reduces the search space from \( O(b^d) \) to \( O(b^{d/2}) \).

### 📌 **Generate and Test Search**  
- Generates a random solution and **tests if it is valid**.  
- Can use **Backtracking** to explore alternatives.

---

## ⚖️ **5. Comparison of Strategies**  
| Strategy | Optimal? | Complete? | Time | Space |  
|----------|----------|-----------|------|-------|  
| **BFS** | ✅ Yes (if costs are equal) | ✅ Yes | \( O(b^d) \) | \( O(b^d) \) |  
| **DFS** | ❌ No | ❌ No (if infinite) | \( O(b^d) \) | \( O(bd) \) |  
| **UCS (Dijkstra)** | ✅ Yes | ✅ Yes | \( O(b^d) \) | \( O(b^d) \) |  
| **Greedy Best-First** | ❌ No | ❌ No | \( O(b^d) \) | \( O(b^d) \) |  
| **A\*** | ✅ Yes (if \( h(n) \) is admissible) | ✅ Yes | \( O(b^d) \) | \( O(b^d) \) |

📌 **Note**: A\* is the best **optimal and efficient search algorithm**, but requires a **good heuristic**.

---

## 🎯 **6. Applications**  
✅ **GPS Navigation** → Google Maps uses variants of **Dijkstra and A\***.  
✅ **Robotics** → Path planning to avoid obstacles.  
✅ **Video Games** → Pathfinding for NPCs (e.g., *A\* in strategy games).  
✅ **Logistics Optimization** → Optimal routing for couriers.

---

## 🔥 **Conclusion**  
📌 **Finding an optimal path** is a central problem in Computational Intelligence. **Uninformed algorithms** (BFS, DFS, UCS) are simple but inefficient. **Informed algorithms** (A\*, Greedy) use heuristics to improve search efficiency.

# Chapter 13
### 🔍 **Genetic Programming (GP): Searching for a Formula**  
**Genetic Programming (GP)** is an evolutionary technique for automatically generating **programs, functions, and mathematical formulas** through a process of natural selection.  

Developed in the **1990s** by **John Koza**, GP is based on **syntax trees**, where **internal nodes** represent **mathematical operators/functions**, and the **leaves** represent **variables or constants**.

---

## 📌 **1. What is Genetic Programming?**  
📌 **GP is an extension of Genetic Algorithms (GA), but instead of evolving numeric strings, it evolves code structures.**  

🔹 **Typical applications of GP**:
- **Symbolic regression** (Discovering mathematical formulas from data).  
- **Classification and prediction in Machine Learning**.  
- **Automatic program synthesis**.  
- **Algorithm optimization**.  

🔹 **Differences between GP and GA**:  
| Characteristic | Genetic Algorithms (GA) | Genetic Programming (GP) |  
|----------------|-------------------------|--------------------------|  
| **Representation** | Bit strings or numbers | Syntax trees |  
| **Evolution** | Crossover and mutation on strings | Crossover and mutation on trees |  
| **Output** | Numerical or vector solutions | Programs or mathematical formulas |

---

## 🏷 **2. Fundamental Elements of GP**  
📌 **Features of GP**  
- **Representation**: **Syntax trees** (executable programs in symbolic languages like LISP).  
- **Selection**: **Roulette wheel** (fitness-proportionate) or **tournament**.  
- **Crossover**: **Exchange of subtrees** between individuals.  
- **Mutation**: **Random substitution of nodes in trees**.  
- **Generational evolution**: The best solutions **survive**.  

🔹 **Example of a GP tree for the formula \( f(x) = x^2 + 3x + 1 \)**  
```
      +
     / \
    *   1
   / \
  x   +
     / \
    3   x
```
📌 **Each individual is an executable program!**

---

## 🔄 **3. Evolution Process in GP**  
1️⃣ **Initialization**  
   - Random creation of programs in the form of **syntax trees**.  
   - **Ramped Half-and-Half**: Alternates between random growth and full tree creation.

2️⃣ **Fitness Evaluation**  
   - Measures the accuracy of the solution (e.g., **mean squared error for symbolic regression**).

3️⃣ **Parent Selection**  
   - **Roulette Wheel Selection** or **Tournament Selection**.

4️⃣ **Crossover and Mutation**  
   - **Crossover**: Two trees exchange sub-expressions.  
   - **Mutation**: Random substitution of functions or terminals in trees.

5️⃣ **Survival and New Generation**  
   - The best individuals **survive** and generate new solutions.  
   - Process is iterated until the **stopping criterion** is reached (e.g., maximum generations).

---

## 🔥 **4. Advanced Techniques in GP**  
📌 **Managing Complexity: The "Bloat" Problem**  
One problem in GP is that trees **grow excessively** without improving fitness.  

📌 **Solutions:**
- **Parsimony Pressure** → Penalizes trees that are too large.  
- **Depth Limitation** → Imposes a maximum depth on trees.  
- **Hoist Mutation** → Removes useless subtrees.  

📌 **Advanced Modifications to GP**:  
1. **Automatically Defined Functions (ADF)**  
   - Introduces **reusable functions**, reducing redundancy and improving modularity.

2. **Cartesian Genetic Programming (CGP)**  
   - Uses **directed acyclic graphs** instead of trees.

3. **Neuroevolution with GP**  
   - Evolution of **neural network architectures** (e.g., NEAT, HyperNEAT).

---

## 🚀 **5. Applications of GP**  
✅ **Symbolic Regression** → Discovering mathematical formulas from data.  
✅ **Data Science & Machine Learning** → Evolving predictive models.  
✅ **Program Synthesis** → Automatically creating code.  
✅ **AI for Video Games** → Evolving intelligent strategies.

📌 **Famous Example**:  
- A **GP program** **autonomously discovered physical laws** from experimental datasets.

---

## 📊 **6. Comparison between GP and Other Evolutionary Algorithms**  
| Algorithm | Type of Structure | When to Use? |  
|-----------|-------------------|--------------|  
| **Genetic Algorithms (GA)** | Bit strings/numbers | Combinatorial optimization |  
| **Evolution Strategies (ES)** | Real vectors | Numerical optimization |  
| **Genetic Programming (GP)** | Syntax trees | Formula and program synthesis |

---

## 🔥 **Conclusion**  
📌 **Genetic Programming (GP)** is a powerful evolutionary technique for **generating mathematical formulas, predictive models, and executable code**.  

📌 **GP is used in Machine Learning, AI, and Data Science to automatically discover rules and functions hidden in data**.  


# Chapter 14
### 📌 **Searching for a Policy: Learning and Planning in Computational Intelligence**  

In the context of *Computational Intelligence*, finding a **policy** means defining a strategy that guides an agent's actions in an environment, aiming to maximize a reward function or meet specific constraints.

---

### 🏷 **Learning vs. Planning**  
Two main approaches to finding a policy are **learning (Learning)** and **planning (Planning)**:

1. **Learning (Apprendimento)**  
   - The environment is **initially unknown**.  
   - The agent **interacts** with the environment by gathering experiences.  
   - The agent **improves its policy** based on the collected data.  
   - Examples: *Reinforcement Learning (Q-Learning, Policy Gradient, DDPG)*.

2. **Planning (Pianificazione)**  
   - A **model of the environment** is already known.  
   - The agent performs **internal calculations** without direct interaction with the environment.  
   - The agent **optimizes its policy** using the model.  
   - Examples: *Value Iteration, Policy Iteration, Monte Carlo Tree Search (MCTS)*.

📌 **Key Difference:**  
- **Learning** → Interaction with the environment, improving over time.  
- **Planning** → Uses a known model to make decisions ahead of time.

---

### 🎯 **Definition of Policy**  
A **policy \( \pi(s) \)** defines the action an agent must take in a given state \( s \).

1. **Deterministic Policy**  
   - Maps each state \( s \) to a specific action \( a \).  
   - Formula:  
     \[
     \pi(s) = a
     \]  
   - The output is always predictable for the same state.

2. **Stochastic Policy**  
   - Maps each state \( s \) to a **probability distribution** over actions.  
   - Formula:  
     \[
     \pi(a|s) = P(A = a | S = s)
     \]  
   - Allows exploration of different actions based on the assigned probability.  
   - Used in **probabilistic approaches** like *Policy Gradient Methods* in Reinforcement Learning.

📌 **When to use a stochastic policy?**  
- When we want to **favor exploration**.  
- When the problem has a **non-deterministic environment**.

---

### 🚀 **Evolutionary Approaches to Policy Search**  

In addition to traditional learning and planning approaches, **evolutionary** methods can be applied:

1. **Cartesian Genetic Programming (CGP)**  
   - Evolution of arithmetic functions represented as **directed acyclic graphs (DAGs)**.  
   - Useful for **symbolic optimization** and *program synthesis*.  
   - Implementation: [CGP++](https://github.com/RomanKalkreuth/cgp-plusplus).

2. **Linear Genetic Programming (LGP)**  
   - A variant of *Genetic Programming* that evolves programs as sequences of instructions.  
   - More structured than classical GP, supporting **branching and logical conditions**.

3. **Grammatical Evolution (GE)**  
   - Uses **Backus-Naur Form (BNF)** to evolve expressions in arbitrary languages.  
   - Indirect mapping between genotype (a list of integers) and phenotype (solution interpreted by the programming language).

📌 **Advantages of using evolutionary approaches for policy learning**  
- Can find **non-obvious solutions**.  
- Suitable for problems where the objective function is not easily derivable.  
- Applied to contexts like **program synthesis**, **strategy optimization**, and **algorithm design**.

---

### 🏆 **Policy Optimization Goals**  

When searching for a policy, different goals may exist:

1. **Worst-Case Scenario**  
   - Minimize the worst possible outcome.  
   - Example: Natural disaster management.

2. **Expected Return**  
   - Maximize the cumulative expected reward.  
   - Example: Financial investments.

3. **Risk-Adjusted Return**  
   - Optimize expected return considering risk.

4. **Robust Optimization**  
   - Ensure good performance across a variety of scenarios.

5. **Maximize Long-Term Value**  
   - Favor actions that guarantee long-term success.

6. **Minimize Risk**  
   - Reduce the probability of catastrophic failures.

7. **Achieve Specific Targets**  
   - Focus on specific and constrained goals.

8. **Enhance Robustness**  
   - Ensure the solution works under adverse conditions.

9. **Optimize Resource Utilization**  
   - Maximize efficiency in the use of available resources.

---

### 🔍 **Conclusion**  
Searching for an **optimal policy** is at the core of many **Computational Intelligence** problems, especially in **Reinforcement Learning, Planning, and Evolutionary Optimization**.

- If **the environment is unknown**, we use **learning** methods.  
- If **we can model the environment**, we use **planning techniques**.  
- If **the problem is highly non-linear or unstructured**, **evolutionary algorithms** can be applied to optimize policies.

# Chapter 15

### 📌 **Reinforcement Learning (RL): Reward-Based Learning**  

**Reinforcement Learning (RL)** is a **machine learning** paradigm where an agent interacts with an environment to maximize a reward function over time.

---

### 🏷 **Fundamentals of Reinforcement Learning**  

1. **Reward Hypothesis**  
   - All goals can be described as the **maximization of cumulative expected reward**.  
   - Actions have **long-term consequences**.  
   - Rewards can be **delayed** (e.g., refueling a helicopter now can prevent an accident later).  

📌 **Examples of Rewards in RL:**  
- **Backgammon** → \( \pm r \) for win/loss.  
- **Investment portfolio management** → \( \pm r \) for each euro gained or lost.  
- **Power plant control** → \( +r_1 \) for energy produced, \( -r_2 \) for safety violations.  
- **Humanoid robot walking** → \( +r_1 \) for moving forward, \( -r_2 \) for falling.

---

### 🏆 **Mathematical Modeling: Markov Decision Processes (MDP)**  

Reinforcement Learning can be formalized as a **Markov Decision Process (MDP)**:  
\[
MDP = (\mathcal{S}, \mathcal{A}, \mathcal{P}, R, \gamma)
\]  

- **\(\mathcal{S}\) (State Space)** → Set of possible states of the system.  
- **\(\mathcal{A}\) (Action Space)** → Set of available actions.  
- **\(\mathcal{P}(s' | s, a)\) (Transition Probability)** → Probability of transitioning from state \( s \) to \( s' \) after action \( a \).  
- **\(R(s, a)\) (Reward Function)** → Function that assigns a reward for performing an action in a state.  
- **\( \gamma \) (Discount Factor)** → Discount factor for weighting future rewards.  

📌 **Key Properties:**  
- **Markovian States** → The future is independent of the past given the present.  
  \[
  P(S_{t+1} | S_t) = P(S_{t+1} | S_t, S_{t-1}, ..., S_0)
  \]  
- **Policy \( \pi(s) \)** → Defines the agent’s behavior.  
  - **Deterministic**: \( \pi(s) = a \)  
  - **Stochastic**: \( \pi(a|s) = P(A = a | S = s) \)

---

### 🚀 **Agent vs. Environment**  

1. **Agent**  
   - Receives **observations \( O_t \)**.  
   - Takes **actions \( A_t \)**.  
   - Receives **rewards \( R_t \)**.  

2. **Environment**  
   - Receives action \( A_t \).  
   - Changes state \( S_{t+1} \).  
   - Provides a new observation \( O_{t+1} \).  
   - Emits a new reward \( R_{t+1} \).  

---

### 🔍 **Model-Based vs. Model-Free RL**  

1. **Model-Based RL**  
   - The agent learns or possesses a **model of the environment** and can simulate the evolution of states.  
   - Main techniques:  
     - **Policy Iteration** → Directly improves the policy.  
     - **Value Iteration** → Approximates the value function \( V(s) \).  
     - **Model-Based Q-Learning** → Estimates the function \( Q(s, a) \).  

2. **Model-Free RL**  
   - The agent learns **without an explicit model** of the environment, relying only on experience.  
   - Main techniques:  
     - **Monte Carlo Methods** → Estimates the average value of a policy based on complete samples.  
     - **Temporal Difference Learning (TD)** → Updates estimates as new data becomes available.  
       - **Off-policy** → \( Q(s, a) \) learning (e.g., *Q-Learning*).  
       - **On-policy** → TD(0), TD(\(\lambda\)) (e.g., *SARSA*).  

---

### 📊 **Objective of Reinforcement Learning: Maximizing the Return**  

The goal of the agent is to maximize the **expected return of cumulative rewards**:  
\[
G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \dots
\]  
\(\gamma\) (discount factor) determines how much future rewards are valued compared to the present:  
- \( \gamma = 0 \) → The agent maximizes only immediate rewards.  
- \( \gamma \to 1 \) → The agent optimizes long-term value.

---

### 🔁 **Episodic vs. Continuing Tasks**  

1. **Episodic Tasks**  
   - Have a **final time step \( T \)**.  
   - Example: Playing chess, where the game ends in a win or loss.  

2. **Continuing Tasks**  
   - Do not have a defined end.  
   - Expected return is calculated through **discounted return**:  
     \[
     G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}
     \]  

---

### 🏗 **Main Methods of RL**  

#### **1️⃣ Value-Based RL**  
- The agent learns a **value function** to evaluate states or state-action pairs.  
- **Examples:**  
  - **Q-Learning** → Off-policy algorithm to learn the function \( Q(s,a) \).  
  - **SARSA** → On-policy algorithm to update \( Q(s,a) \) following the current policy.

#### **2️⃣ Policy-Based RL**  
- The agent directly learns a **policy \( \pi(s) \)** without using a value function.  
- **Examples:**  
  - **Policy Gradient Methods** → Uses the gradient to update the policy directly.  
  - **REINFORCE** → Monte Carlo algorithm to estimate policy gradients.

#### **3️⃣ Actor-Critic RL**  
- Combines **Value-Based** and **Policy-Based RL**.  
- **Examples:**  
  - **Advantage Actor-Critic (A2C, A3C)** → Learns separately a policy (actor) and a value function (critic).  
  - **Deep Deterministic Policy Gradient (DDPG)** → Extension for continuous action spaces.

---

### 📖 **Conclusion**  
**Reinforcement Learning** is a powerful *Machine Learning* technique used in games, robotics, finance, and autonomous control.

- If we **have a model** → **Model-Based RL** (e.g., Value Iteration).  
- If we **don’t have a model** → **Model-Free RL** (e.g., Q-Learning).  
- If we **work with discrete actions** → **Q-Learning, SARSA**.  
- If we **work with continuous actions** → **DDPG, PPO**.


# Chapter 16
### 📌 **Model-Based Reinforcement Learning (MBRL): Learning with a Model**  

**Model-Based Reinforcement Learning (MBRL)** is a variant of Reinforcement Learning where the agent **learns or uses a model of the environment** to predict state transitions and rewards, thereby improving its efficiency in learning and planning.

---

### 🏷 **What is a Model in RL?**  

In RL, a **model** is a representation of the system's dynamics that allows simulating the environment's behavior. It consists of two key functions:

1. **Transition Model \( \mathcal{P}(s' | s, a) \)**  
   - Predicts the next state \( s' \) given the current state \( s \) and action \( a \).  
   \[
   \mathcal{P}(s' | s, a) = P(S_{t+1} = s' | S_t = s, A_t = a)
   \]  

2. **Reward Model \( \mathcal{R}(s, a) \)**  
   - Predicts the expected immediate reward for a state-action pair \( (s, a) \).  
   \[
   \mathcal{R}(s, a) = \mathbb{E}[R_{t+1} | S_t = s, A_t = a]
   \]  

📌 **Model Benefits:**  
- Allows **internal simulations** without taking real actions.  
- Reduces the number of **real-world interactions** needed to learn a good policy.  
- Enables **planning techniques**, such as *Value Iteration* and *Policy Iteration*.

---

### 🎯 **Markov Reward Process (MRP) and Markov Decision Process (MDP)**  

A **Markov Reward Process (MRP)** is defined as:  
\[
MRP = (\mathcal{S}, \mathcal{P}, \mathcal{R}, \gamma)
\]  
Where:  
- \( \mathcal{S} \) is the set of states.  
- \( \mathcal{P} \) is the transition probability matrix between states.  
- \( \mathcal{R} \) is the reward function.  
- \( \gamma \) is the **discount factor**, which balances the value of future rewards.  

When we introduce **actions**, we get a **Markov Decision Process (MDP)**:  
\[
MDP = (\mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R}, \gamma)
\]  
Where \( \mathcal{A} \) is the set of available actions.

---

### 🔢 **State Evaluation: Value Functions**  

1. **State-Value Function \( v(s) \)**  
   - Represents the expected return starting from state \( s \) following a policy \( \pi \).  
   \[
   v^\pi(s) = \mathbb{E}^\pi[G_t | S_t = s]
   \]  

2. **Action-Value Function \( q(s, a) \)**  
   - Represents the expected return for taking action \( a \) in state \( s \) and then following \( \pi \).  
   \[
   q^\pi(s, a) = \mathbb{E}^\pi[G_t | S_t = s, A_t = a]
   \]  

📌 **Goal:** Find the **optimal policy \( \pi^* \)** that maximizes the value of the states.

---

### 🏆 **Bellman Equations and Iterative Policy Evaluation**  

The **Bellman Equation** defines the recursive relationship between the value of a state and the value of future states:  
\[
v(s) = \mathcal{R}(s) + \gamma \sum_{s'} \mathcal{P}(s' | s) v(s')
\]  

For an **MDP with policy \( \pi \)**:  
\[
v^\pi(s) = \sum_a \pi(a|s) \left[ \mathcal{R}(s,a) + \gamma \sum_{s'} \mathcal{P}(s' | s, a) v^\pi(s') \right]
\]  

📌 **Methods for Solving the Bellman Equation:**  
1. **Value Iteration**  
   - Iteratively updates \( v(s) \) until convergence.  

2. **Policy Iteration**  
   - Alternates between **policy evaluation** and **policy improvement**.  

3. **Dynamic Programming**  
   - Computational approaches to calculate \( v(s) \) and \( \pi(s) \).

---

### 🚀 **Explicit Models vs. Approximated Models**  

1. **Explicit (Hard-Coded) Models**  
   - Used when the environment's dynamics are fully known (e.g., board games like chess).  
   - Allows **exact simulations**.

2. **Approximated Models (Learned Models)**  
   - When the environment's dynamics are unknown, the agent must **learn the model**.  
   - Learning techniques:  
     - **Supervised Learning** (using historical data to estimate \( \mathcal{P} \) and \( \mathcal{R} \)).  
     - **Neural Networks** (approach used in AlphaGo and MuZero).

📌 **Example: AlphaGo**  
- Uses a **neural network** to learn \( \mathcal{P} \) and \( \mathcal{R} \).  
- Employs **Monte Carlo Tree Search (MCTS)** for planning.

---

### 🔍 **Model-Based vs. Model-Free RL**  

| **Characteristic**    | **Model-Based RL** | **Model-Free RL** |
|----------------------|------------------|----------------|
| Requires a model? | ✅ Yes | ❌ No |
| Data efficiency | ✅ High | ❌ Low |
| Suitable for complex environments? | ❌ Difficult | ✅ Yes |
| Typical applications | Planning, Control | Games, Robotics, Finance |

📌 **Conclusion:**  
- **If we can estimate \( \mathcal{P} \) and \( \mathcal{R} \)** → Model-Based RL.  
- **If we can't model the environment** → Model-Free RL.

---

### 🏗 **Approaches for Policy Learning**  

1. **Iterative Policy Evaluation**  
   - Iteratively applies the Bellman Equation until convergence.

2. **Generalized Policy Iteration (GPI)**  
   - Alternates between **Policy Evaluation** and **Policy Improvement** to converge toward the optimal policy.

3. **Value-Based Methods**  
   - **Value Iteration** and **Policy Iteration** to learn the optimal policy from the value function.

4. **Policy-Based Methods**  
   - **Policy Gradient** (REINFORCE, PPO) to directly learn the optimal policy.

---

### 📖 **Conclusion**  
**Model-Based Reinforcement Learning** combines elements of **planning and learning** to make training more efficient.

- If the **model of the environment is known**, we can use **Value Iteration** and **Policy Iteration**.  
- If the **model is unknown**, we can learn \( \mathcal{P} \) and \( \mathcal{R} \) using **Supervised Learning** or **Neural Networks**.  
- **Model-Based RL is often more efficient**, but **Model-Free RL** is more flexible.

🔍 **Would you like to dive deeper into any specific aspect, such as AlphaGo, MuZero, or planning in RL?** 🚀

# Chapter 16
Below is a set of university-style study notes in English summarizing key definitions, formulas, and tables based on the uploaded slides. The notes combine material from both “Searching for a Policy – Adversarial Search” and “Parallelizing Minimax” (Davide), and are organized by topic for clarity.

────────────────────────────
• **1. Adversarial Search & Game-Playing**

**a. Key Definitions & Concepts**

- **Adversarial Search:**  
  A framework for decision-making in games where two (or more) opponents choose moves in a competitive (often zero‐sum) environment. The goal is to find an *optimal policy* (i.e., a mapping from game states to best moves) rather than a fixed sequence of actions. citeturn0file0

- **Game Taxonomy:**  
  Games can be classified by:
  - **Deterministic vs. Probabilistic:** (No chance vs. incorporating randomness)  
  - **Perfect vs. Imperfect Information:** (Full state visibility vs. hidden information)  
  - **Turn-based vs. Real-time:**  
  - **Zero-sum vs. Non-zero sum:**  
  *Example:* Chess is deterministic, turn-based, zero-sum, and with perfect information, whereas poker is probabilistic and has imperfect information.

- **Minimax Algorithm:**  
  A decision rule used in two-player zero-sum games with perfect information.  
  **Principle:**  
  – MAX (the player) selects the move that maximizes the minimum gain that can be forced by MIN (the opponent).  
  – **Negamax Formulation:**  
    The value of a node can be computed as the negation of the opponent’s evaluation:  
    \[
    \text{Value}(node) = -\text{Value}(\text{child node})
    \]
  **Properties:**  
  – *Complete* (if the game tree is finite)  
  – *Optimal* against an optimal opponent  
  – **Complexity:**  
    Time: \( \mathcal{O}(b^m) \)  Space: \( \mathcal{O}(b \times m) \)  
    where \( b \) is the branching factor and \( m \) is the maximum depth. citeturn0file0

**b. Alpha-Beta Pruning**

- **Definition:**  
  An optimization of the minimax algorithm that skips evaluating branches that will not influence the final decision.  
- **Mechanism:**  
  Two parameters—α (the best value the maximizer currently can guarantee) and β (the best value the minimizer currently can guarantee)—are maintained during search. If at any node α becomes greater than or equal to β, further search in that branch is abandoned.  
- **Benefits:**  
  – Reduces the number of nodes evaluated  
  – Allows deeper search in the same time budget

**c. Cut-off Techniques & Evaluation**

- **Cut-off Problems:**  
  When the full game tree cannot be explored (due to huge search spaces), a *hard cut-off* depth is used. This introduces issues like the *Horizon Effect* (failure to see an important event just beyond the cut-off).  
- **Enhanced Methods:**  
  – *Quiescence Search:* Increases depth in volatile positions  
  – *Singular Extensions:* Selectively extend search when one move is significantly better
- **Evaluation Functions:**  
  – Heuristic evaluation (e.g., material balance, pawn structure in chess)  
  – Machine Learning can also be used to “learn” evaluation functions from data. citeturn0file0

**d. Stochastic & Imperfect-Information Games**

- **Stochastic Minimax:**  
  In games involving chance (e.g., dice throws), the minimax formulation is extended to compute an expected reward:
  \[
  \text{Value}(node) = \max_{\text{actions}} \min_{\text{opponent actions}} \mathbb{E}[\text{Reward}]
  \]
- **Imperfect Information:**  
  Strategies such as treating unknown states as random or using a policy that maximizes the minimum reward are applied.  
- **Iterated Prisoner’s Dilemma:**  
  A repeated game demonstrating concepts like Nash equilibrium and strategies such as “Tit for Tat.”

────────────────────────────
• **2. Parallelizing Minimax**

**a. Recap: Minimax & Negamax**

- **Minimax (and Negamax):**  
  Used to evaluate game positions by assuming optimal play from both sides. In Negamax, the symmetry allows a simplified formulation:
  \[
  \text{Value}(node) = \max_{\text{action}} \left(-\text{Value}(\text{Succ}(node,\, action))\right)
  \]
  This simplification benefits implementation and parallelization. citeturn0file1

**b. Alpha-Beta in a Parallel Setting**

- **Parallelization Motivation:**  
  With modern multi-core processors, parallelizing search can increase both the number of nodes processed per second (scalability) and reduce the total search time (speedup).  
- **Challenge:**  
  Alpha-Beta pruning is inherently sequential due to shared bounds (α and β). Distributing the work requires careful synchronization and data sharing.

**c. Key Parallelization Techniques**

1. **Shared Hash Table:**  
   A common data structure (often in shared memory) used to store evaluated positions (transposition table).  
   **Pros/Cons Table:**

   | Aspect          | Pros                                        | Cons                                               |
   |-----------------|---------------------------------------------|----------------------------------------------------|
   | Locks           | Simple and reliable using standard mutexes  | Can suffer from contention and deadlocks           |
   | Lock-Free       | Better scalability using atomic operations  | More complex to design and verify                  |

2. **Lazy SMP:**  
   Multiple instances of the search share a common transposition table.  
   – Each thread explores the same root position with different move orders or depth settings, adding nondeterminism.  
   – Scales well on 8–12 cores and is implemented in engines like Stockfish.

3. **ABDADA (Alpha-Bêta Distribué avec Droit d'Aînesse):**  
   A distributed version where processors start simultaneously from the root and use a “young brothers wait” strategy to coordinate search efforts.

4. **Parallel Alpha-Beta Strategies:**

   - **Principal Variation Splitting:**  
     The best (principal) move is searched with a full window, and all other moves are evaluated with a narrow (null) window in parallel. If a secondary move “fails high” (exceeds the current best), it is re-searched with a full window.
     
   - **Young Brothers Wait Concept:**  
     Prioritizes the search of the first (oldest) child node fully, while the “younger siblings” wait to avoid unnecessary work if a cutoff occurs.
     
   - **Dynamic Tree Splitting:**  
     Processors that complete their work publish the current subtree state to shared memory. Idle processors then pick up these subtrees, ensuring no core remains idle during heavy search periods.

**d. Summary Table of Parallel Techniques**

| Technique                   | Key Idea                                       | Scalability Issue                            |
|-----------------------------|------------------------------------------------|----------------------------------------------|
| Shared Hash Table           | Share evaluated nodes across threads           | Lock contention can limit performance        |
| Lazy SMP                    | Nondeterministic search sharing common data      | Effective mainly on 8–12 cores                |
| ABDADA                      | Distributed alpha-beta with eldest son right     | Requires extra management of transposition info|
| Principal Variation Splitting| Full window for best move; null window for others | Must re-search if null search indicates a better move |
| Young Brothers Wait Concept | Sequentially focus on the first child then parallelize | Balances between waiting and parallel efficiency |
| Dynamic Tree Splitting      | Distribute work from busy to idle processors     | Complexity in continuous workload distribution|

────────────────────────────
• **3. Conclusions**

- **Adversarial Search:**  
  Methods like Minimax and Alpha-Beta Pruning are foundational for game-playing AI. Their effectiveness is tied to the ability to efficiently explore huge game trees using evaluation functions and selective search extensions.

- **Parallelization:**  
  As modern hardware emphasizes multi-core performance, techniques for parallelizing search (such as Lazy SMP and Principal Variation Splitting) have become crucial. However, inherent sequential aspects of Alpha-Beta pruning continue to pose challenges for achieving ideal scalability.

These notes provide a compact overview of key definitions, formulas, and algorithmic strategies in adversarial search and the parallelization of minimax-based algorithms, based on the slide material from both documents.

# Chapter 17

Below is a set of university-style study notes in English on Learning Classifier Systems (LCS) based on the provided slides. The notes summarize key definitions, components, algorithms, and challenges.

────────────────────────────
• **1. Introduction to Learning Classifier Systems (LCS)**

- **Definition:**  
  An LCS is a machine learning framework that uses a population of condition–action rules (classifiers) to learn from and interact with an environment. It integrates ideas from reinforcement learning and genetic algorithms to evolve a set of rules that map environmental conditions to appropriate actions. citeturn1file0

- **Key Characteristics:**  
  – Rule-based system where each rule is represented as a string (often ternary, e.g., using symbols like 0, 1, and ‘#’ for “don’t care”)  
  – The system continuously evolves its rule population to improve performance and generality  
  – Two main styles exist: Michigan-style (one classifier system) and Pittsburgh-style (rule sets as individuals)

────────────────────────────
• **2. Anatomy of an LCS**

- **Core Components:**

  1. **Classifier Population:**  
     – A finite set of rules (classifiers) that represent the system’s current knowledge.  
     – Each classifier has a condition part (specifying when it applies) and an action part (what to do when it applies).  
     – Specificity is defined as the fraction of fixed bits (i.e., not ‘#’).

  2. **Discovery Component:**  
     – Uses genetic algorithms (GAs) to generate new classifiers and improve existing ones.  
     – Can operate online (during interaction with the environment) or offline.

  3. **Performance Component:**  
     – Manages the interaction between the environment and the classifier population, determining which rules are activated based on the current state.

  4. **Reinforcement (Credit Assignment) Component:**  
     – Distributes rewards received from the environment to the classifiers that contributed to the decision.  
     – Supports both supervised and reinforcement learning paradigms.

- **System Architecture (JH’s Basic Structure):**  
  Typically includes interfaces for input, output, and message passing, along with a database of classifiers (rules represented as bit or ternary strings). citeturn1file0

────────────────────────────
• **3. LCS Rule Representations & Styles**

- **Rule Format:**  
  – Basic rule:  
    \[
    \text{IF } \text{condition} \text{ THEN } \text{action}
    \]
  – In simplified systems like Wilson’s ZCS:  
    \[
    r = \langle c : a \rightarrow s \rangle
    \]
    where:  
    • \(c\) is the condition (pattern for matching input),  
    • \(a\) is the action (effect to be executed),  
    • \(s\) is the strength (a numerical value representing rule utility).

- **Michigan-Style vs. Pittsburgh-Style:**  
  – **Michigan-style:** The population consists of individual classifiers that collectively represent the solution (e.g., Cognitive System One).  
  – **Pittsburgh-style:** Each individual in the population is a complete rule set (often used in offline learning).

────────────────────────────
• **4. Key Algorithms in LCS**

- **Bucket Brigade Algorithm:**  
  – A bidding process in which each activated classifier bids an amount proportional to its strength (rule strength is often a function of its specificity and fitness).  
  – The highest bidder “wins” and passes credit (or bid value) back to classifiers whose messages contributed to the activation.  
  – This creates a reinforcement chain that adjusts the strengths of classifiers based on their contribution to successful actions.

- **Genetic Algorithm (GA) in LCS:**  
  – Used as the discovery mechanism to evolve new classifiers.  
  – Operates on the population by selecting, crossing over, and mutating classifiers to improve performance.  
  – In systems like Wilson’s XCS, the GA uses rule accuracy (not just payoff) to drive evolution.

- **Wilson’s Variants:**  
  1. **ZCS (Zero-knowledge Classifier System):**  
     – Simplified system with no internal message list.  
     – Uses a simpler rule representation and deterministic matching.
  
  2. **XCS (eXtended Classifier System):**  
     – Focuses on learning an accurate and general representation of the payoff map.  
     – Each classifier in XCS is augmented with:  
       • Reward Prediction (\(R\)): Expected average reward  
       • Prediction Error (\(\varepsilon\)): Deviation in prediction  
       • Fitness (\(F\)): Normalized accuracy  
       • Experience (\(exp\)) and average action-set size (\(a\)) may also be maintained.  
     – Rule fitness for the GA is based on the accuracy of predictions rather than the absolute payoff.

────────────────────────────
• **5. Selection Mechanisms & Challenges**

- **Selection Strategies:**  
  – **Strength-based Selection:**  
    • Maximizes reward prediction; focuses on high-payoff rules.  
    • May under-represent low-reward classes and lead to over-generalization.
  
  – **Accuracy-based Selection:**  
    • Focuses on the accuracy of reward prediction to learn a complete reward map.  
    • Can be misled by inaccurate predictions if not properly managed.

- **Open Problems:**  
  – **Parallelism & Coordination:**  
    • How to effectively parallelize the learning and rule discovery processes.  
  – **Credit Assignment:**  
    • How to properly distribute reward over long sequences of actions.  
  – **Rule Discovery:**  
    • Determining when to replace low-strength rules using random generation and heuristics.

────────────────────────────
• **6. Summary Table**

| Component/Algorithm         | Description                                                               | Key Challenge                                  |
|-----------------------------|---------------------------------------------------------------------------|------------------------------------------------|
| **Classifier Population**   | Finite set of rules represented as ternary strings                        | Balancing generality vs. specificity           |
| **Bucket Brigade**          | Auction-based reinforcement where bids are proportional to rule strength   | Avoiding dominance by over-general rules       |
| **Genetic Algorithm**       | Discovery mechanism for evolving rules                                    | Maintaining diversity and convergence          |
| **ZCS vs. XCS**             | ZCS: Simplified, deterministic; XCS: Accuracy-based fitness and generality  | Accurate credit assignment and rule fitness    |
| **Selection Strategies**    | Strength-based (focus on payoff) vs. Accuracy-based (focus on prediction accuracy) | Handling under-representation and misleading accuracy |

────────────────────────────
• **Conclusion**

Learning Classifier Systems (LCS) offer a powerful and flexible framework for rule-based learning. By integrating reinforcement learning with genetic algorithms, LCS can adapt and evolve to effectively map environmental states to actions. Despite their promise, challenges remain in areas such as credit assignment, rule discovery, and parallel processing.

These notes provide a compact overview of the core concepts, algorithms, and challenges within LCS as described in the provided slides.

# Chapter 18 (presentation - contribution)

Below is a comprehensive set of university-style study notes covering the multiple topics presented in the merged PDF. The notes are organized into sections with key definitions, formulas, and tables where appropriate.

────────────────────────────
**1. The 8-Queens Problem**

- **Overview & History:**  
  - **Problem Statement:**  
    Place 8 queens on a chessboard so that no two queens share the same row, column, or diagonal.  
  - **Origin:**  
    First proposed in 1848 by Max Bezzel; later popularized as a demonstration of structured programming (also used by Gauss and Dijkstra).

- **Key Statistics (n = 8):**  
  - Total configurations: 4,426,165,368  
  - Valid solutions: 92 (or 12 unique solutions after accounting for rotations/reflections)

- **Algorithms & Techniques:**  
  - **Hill Climbing:**  
    - *Initialization:* Random placement  
    - *Successor Generation:* Move one queen within its column (56 possible neighbors)  
    - *Selection:* Choose neighbor with the lowest “badness” (h-value)
  - **Simulated Annealing:**  
    - Occasionally accepts worse moves based on a temperature schedule  
    - High temperatures allow exploration; low temperatures refine the search.
  - **Genetic Algorithms:**  
    - **Representation:** Strings denoting queen positions per column  
    - **Fitness:** Based on the number of non-attacking queen pairs  
    - **Operators:** Selection, crossover, and mutation to create new candidate solutions.
  - **Depth-First Search (DFS):**  
    - Place a queen in one column, backtrack when no valid position is found.
  - **Innovative Approaches:**  
    - **Quantum Annealing:** Uses quantum superposition and tunneling to escape local optima.  
    - **Swarm Intelligence:**  
      - *Ant Colony Optimization:* Mimics pheromone trails to converge on valid configurations.  
      - *Particle Swarm Optimization:* Uses particles (candidate solutions) that update positions based on their own and neighbors’ best-known states.

- **Comparison Table of Methods:**

| Algorithm             | Key Idea                                         | Pros                                     | Cons                                  |
|-----------------------|--------------------------------------------------|------------------------------------------|---------------------------------------|
| Hill Climbing         | Local search by moving one queen at a time       | Simple, fast for small problems          | Prone to getting stuck in local minima |
| Simulated Annealing   | Probabilistic acceptance of worse moves           | Escapes local minima                     | Requires careful temperature tuning    |
| Genetic Algorithms    | Evolution of queen-position strings               | Good global search capabilities          | May need many iterations; parameter tuning |
| Depth-First Search    | Recursive placement and backtracking              | Guarantees a solution if one exists      | Exponential search space               |
| Quantum Annealing     | Quantum-inspired search dynamics                  | Potentially escapes deep local traps     | Experimental; requires special hardware |
| Swarm Intelligence    | Collective, decentralized search (ants/particles) | Effective in balancing exploration and exploitation | More complex to design and tune        |

────────────────────────────
**2. The Generalized N-Friends (Tandem Bicycle) Problem**

- **Problem Statement:**  
  A group of students (divided into two types, e.g., computer engineers \(N_C\) and data scientists \(N_D\)) must travel to a pizzeria using a tandem bicycle that carries 2 people. A constraint is that if there are more computer engineers than data scientists, the evening is “ruined.”

- **Representation:**  
  - States are represented by the number of students at each location and the position of the tandem.  
  - Moves change the counts at “home” and “pizzeria.”

- **Key Formulas (Simplified Cases):**  
  - **Equal Numbers (\(N_C = N_D\)):**  
    For \(N_C = N_D\) up to 3, solutions exist with a formula like:  
    \[
    \#\text{steps} = \begin{cases}
    1, & \text{if } N_C = N_D \le 2 \\
    2N_C - 3, & \text{if } N_C = N_D \ge 3 \quad (\text{for } k=2 \text{ seats})
    \end{cases}
    \]
  - **Unequal Cases (\(0 \le N_C < N_D\)):**  
    Generalized formula example:  
    \[
    \#\text{steps} = \begin{cases}
    1, & \text{if } N_C = 0 \text{ and } N_D \le 2 \\
    3, & \text{if } N_C + N_D = 3 \\
    2N_C + N_D - 3, & \text{if } N_C + N_D > 3 \text{ and } 0 \le N_C < N_D
    \end{cases}
    \]
  - **Upgrading the Tandem:**  
    If the vehicle capacity increases (e.g., \(k=3\) or \(k=4\)), the formulas change accordingly—for instance, for \(N_C = N_D\) with \(k=3\):  
    \[
    \#\text{steps} = \begin{cases}
    2N_C - 1, & 1 \le N_C \le 3 \\
    2N_C + 1, & 4 \le N_C \le 5
    \end{cases}
    \]

- **Changing Representation:**  
  An alternative model may treat a student “in transit” as not being counted at either location, which can simplify the problem (e.g., making the step count a linear function like \(4N_C - 3\) when \(N_C = N_D\)).

────────────────────────────
**3. Parallelizing Minimax**

- **Recap:**  
  - **Minimax:** Evaluates game states in zero-sum games, assuming optimal play.  
  - **Negamax:** A simplified formulation using symmetry:
    \[
    \text{Value}(node) = \max_{\text{action}} \bigl(-\text{Value}(\text{Succ}(node, \text{action}))\bigr)
    \]
- **Alpha-Beta Pruning:**  
  - Maintains \( \alpha \) (best maximizer value) and \( \beta \) (best minimizer value) to prune subtrees that cannot affect the final decision.
- **Challenges in Parallelization:**  
  - The sequential nature of propagating shared bounds (α and β) makes parallelizing search nontrivial.
- **Techniques for Parallel Search:**

| Technique                      | Key Idea                                              | Notes                                                   |
|--------------------------------|-------------------------------------------------------|---------------------------------------------------------|
| Shared Hash Table              | Use common transposition tables to share search info  | May involve locks or lock-free designs                  |
| Lazy SMP                      | Multiple search instances share a table with different move orders  | Scales well up to 8–12 cores                            |
| ABDADA                        | Distributed search with “eldest son right” strategy     | Uses extra transposition info for coordination          |
| Principal Variation Splitting  | Search best move fully; other moves with null windows  | Requires re-search if a secondary move exceeds the best  |
| Young Brothers Wait Concept   | Delay sibling searches until the first (oldest) child is evaluated | Prevents wasted computation if a cutoff occurs         |
| Dynamic Tree Splitting         | Idle processors take over parts of busy subtrees       | Ensures continuous workload distribution                |

────────────────────────────
**4. Function Approximation in Reinforcement Learning**

- **Motivation: The Curse of Dimensionality**  
  - Explicit tables for value functions become intractable for large or continuous state spaces.
- **Approach:**  
  Replace lookup tables with parameterized functions \(V_\theta(s)\) or \(Q_\theta(s,a)\).
- **Types of Approximators:**
  - **Linear:**  
    \[
    V(s) \approx w_1 f_1(s) + w_2 f_2(s) + \dots + w_n f_n(s)
    \]
    *Pros:* Simple and efficient  
    *Cons:* Limited to linear relationships.
  - **Polynomial:**  
    Incorporates higher-order terms to capture some nonlinearity.
  - **Neural Networks:**  
    Highly expressive; can model complex, non-linear mappings.
  - **Decision Trees / Ensembles:**  
    Partition the state space into regions.
  - **Radial Basis Function (RBF) Networks:**  
    Use localized activations based on distance from centers.
- **Training Approaches:**  
  - **Loss Function:** Mean Squared Error (MSE) between predicted and target values.  
  - **Gradient Descent Update:**  
    \[
    \theta_{t+1} = \theta_t + \alpha \nabla J(\theta_t)
    \]
  - **Target Computation:**  
    - *Monte Carlo:* \( G_t = R_{t+1} + \gamma R_{t+2} + \dots \)  
    - *Temporal Difference (TD):* \( G_t = R_{t+1} + \gamma V(S_{t+1}) \)
- **Challenges:**  
  - Stability and convergence (the “Deadly Triad” of function approximation, off-policy learning, and bootstrapping)  
  - Overfitting and the need for techniques like experience replay.

────────────────────────────
**5. Multi-Agent Reinforcement Learning (MARL)**

- **Definition:**  
  MARL extends RL to environments with multiple autonomous agents that may cooperate, compete, or do both.
- **Architectural Approaches:**  
  - **Centralized:** A single controller makes decisions using aggregated information.  
  - **Decentralized:** Each agent acts on local observations.  
  - **Hybrid:** Combines centralized planning with decentralized execution.
- **Key Challenges:**  
  - **Combinatorial Explosion:** State–action space grows exponentially with the number of agents.  
  - **Non-Stationarity:** Agents learning simultaneously make the environment dynamic.  
  - **Credit Assignment:** Difficulties in attributing rewards to individual agents.  
  - **Exploration vs. Exploitation:** Balancing individual and collective learning strategies.
- **Applications:**  
  Robotics, autonomous vehicles, games, financial markets, resource planning.

────────────────────────────
**6. Fuzz Testing**

- **Definition:**  
  An automated testing technique that feeds invalid, malformed, or random inputs into a program to uncover bugs and vulnerabilities.
- **Process Steps:**  
  1. **Identification of Target System**  
  2. **Determination of Inputs**  
  3. **Generation of Fuzzed Data**  
  4. **Execution of Tests with Fuzzed Data**  
  5. **Logging & Analysis of System Behavior**
- **Advantages:**  
  - Uncovers hidden defects, memory issues, and input validation bugs.  
  - Can be highly automated and scalable.
- **Disadvantages:**  
  - May require significant computational resources.  
  - Possibility of false positives/negatives.

────────────────────────────
**7. Deep Q-Learning**

- **Background:**  
  Traditional Q-Learning uses a table of Q-values, which becomes infeasible for high-dimensional problems.
- **Deep Q-Learning:**  
  - Uses a neural network to approximate the Q-function:  
    \[
    Q(s,a; \theta) \approx Q^*(s,a)
    \]
  - **Key Innovations:**  
    - **Experience Replay:** Stores past experiences and samples them randomly to break correlation.  
    - **Target Networks:** Stabilize training by decoupling the target Q-value computation from the current network.
  - **Applications:**  
    - Video games (e.g., Atari)  
    - Robotics and control  
    - Finance and trading strategies
- **Advantages:**  
  - Can handle high-dimensional inputs (e.g., raw pixels).  
  - Scales to complex, real-world tasks.

────────────────────────────
**8. Pareto-Optimal Symbolic Regression**

- **Objective:**  
  Discover simple yet accurate symbolic expressions that explain data.
- **Method Overview:**  
  - **Neural Network Fitting:**  
    Fit a network to the data to obtain a computational graph.
  - **Graph Modularity:**  
    Analyze gradients and modularity in the computational graph to suggest separable components (e.g., additive or multiplicative structures).
  - **Pareto-Optimality:**  
    Balance accuracy (e.g., low MSE) with complexity (formula size), using a Pareto frontier to select optimal formulas.
- **Techniques:**  
  - Recursive pruning of overly complex candidate expressions.  
  - Brute-force search and polynomial fitting on extracted modules.

────────────────────────────
**9. Policy Gradient Methods in Reinforcement Learning**

- **Core Idea:**  
  Directly learn a parameterized policy \( \pi(a|s,\theta) \) by adjusting parameters in the direction that increases expected reward.
- **Policy Gradient Theorem:**  
  Provides the gradient of the performance measure \( J(\theta) \) with respect to \( \theta \):
  \[
  \nabla J(\theta) \propto \mathbb{E}_{\pi}\Bigl[ Q^\pi(s,a) \nabla \log \pi(a|s,\theta) \Bigr]
  \]
- **REINFORCE Algorithm:**  
  A Monte Carlo policy gradient method where the update is:
  \[
  \theta_{t+1} = \theta_t + \alpha G_t \nabla \log \pi(a_t|s_t,\theta_t)
  \]
  where \( G_t \) is the return following time \( t \).
- **Example Application:**  
  Grid world problems where an agent learns an optimal policy by trial and error.

────────────────────────────
**Conclusion**

These notes cover a broad range of topics in computational intelligence—from classic combinatorial puzzles like the 8-Queens problem and generalized transport puzzles, through advanced search techniques and reinforcement learning methods, to modern topics in deep learning and multi-agent systems. Each section introduces core concepts, highlights challenges, and provides key formulas or comparative tables to facilitate study and review.

Feel free to refer back to these notes as a guide when delving into the detailed algorithms and methods presented in class.

