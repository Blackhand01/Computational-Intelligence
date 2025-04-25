Miei lab:
Lab0 (witty joke or remark about the lecture):
Maybe I need to study *Computational Intelligence* to program an algorithm that respects deadlines... or maybe I just need more coffee, but I wasn't at home...😅 <br/>
<sub>This joke refers to slide 16, which discusses *Wozniak’s Cup of Coffee*.</sub>

Lab1:
Results

Instance 1

Universe Size: 100
Num Sets: 10
Density: 0.2
Best Coverage: 100/100
Best Cost: 277.9681373777353
Instance 2

Universe Size: 1000
Num Sets: 100
Density: 0.2
Best Coverage: 1000/1000
Best Cost: 7147.2677358291785
Instance 3

Universe Size: 10000
Num Sets: 1000
Density: 0.2
Best Coverage: 10000/10000
Best Cost: 744527.8242379159
Instance 4

Universe Size: 100000
Num Sets: 10000
Density: 0.1
Best Coverage: 100000/100000
Best Cost: 111710457.06755874
Instance 5

Universe Size: 100000
Num Sets: 10000
Density: 0.2
Best Coverage: 100000/100000
Best Cost: 247542733.07211494
Instance 6

Universe Size: 100000
Num Sets: 10000
Density: 0.3
Best Coverage: 100000/100000
Best Cost: 374153917.78369844
Summary

The Hill Climbing algorithm successfully found solutions that fully cover the universe for all instances.

Recensioni sul lab1:
Skip to content
Navigation Menu
Blackhand01
CI2024_lab1
 
Type / to search
Code
Issues
2
Pull requests
Actions
Projects
Wiki
Security
Insights
Settings
Lab1R #2
Open
@simotmm
Description
simotmm
opened on Oct 19, 2024
Overview

The proposed solution uses an Hill Climbing algorithm with a single mutation for each call of the tweak function. It reaches succesfully the maximum coverage for each instance of the problem proposed.

Code and documentation

The code is well organized and the comments are simple and helpful in order to understand the steps of the algorithm.

I appreciated the declaration of the instances array in the Main Execution part and I also appreciated the results summary in the readme markdown file.

The code ran successfully, there's no bug in it.

Possible improvements

As said, the program reaches the maximum coverage for each instance, but the valid function is never called to check if a solution is actually valid. I suggest to add a fitness function that combines the cost function and the valid function.
Final comment

Good job! 👍
Activity
Blackhand01
Add a comment
new Comment
Markdown input: edit mode selected.
Write
Preview

Assignees
No one - Assign yourself
Labels
No labels
Projects
No projects
Milestone
No milestone
Relationships
None yet
Development
Create a branch for this issue or link a pull request.
NotificationsCustomize
You're receiving notifications because you're subscribed to this thread.
Participants
@simotmm
Issue actions
Transfer issue
Lock conversation
Pin issue
Delete issue
Footer
© 2025 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Docs
Contact
Manage cookies
Do not share my personal information
Lab1R · Issue #2 · Blackhand01/CI2024_lab1

Skip to content
Navigation Menu
Blackhand01
CI2024_lab1
 
Type / to search
Code
Issues
2
Pull requests
Actions
Projects
Wiki
Security
Insights
Settings
Lab1 Peer Review #1
Open
@carlopantax
Description
carlopantax
opened on Oct 18, 2024
Generally Speaking the Hill Climbing algorithm is an optimum and fast solution for the Set Cover Problem, even if sometimes the search for a solution might get stuck in a local minimum.
In this case the algorithm starts with a random solution (50% of sets selected), it calculates the coverage and cost of the current solution, then the tweak() function flips one random set from the previous solution and the new solution is accepted if it increases the coverage of the universe, or it maintains the same coverage but it reduces the cost.
I think everything is ok, except for one detail. As indicated in https://en.wikipedia.org/wiki/Set_cover_problem: "Given a set of elements {1, 2, …, n} (called Universe, specifying all possible elements under consideration) and a collection, referred to as S, of a given m subsets whose union equals the universe, the set cover problem is to identify a smallest sub-collection of S whose union equals the universe", however the code accepts a new solution both it improves coverage (covers more items than the current solution), or it maintains the same coverage but reduces the cost, but there is no explicit check whether the coverage reaches 100% of the universe elements. Infact the helper function valid() is never called and np.sum(np.logical_or.reduce(sets[new_solution])) only calculates the current solution coverage, without checking if it covers all the items.
Activity
Blackhand01
Add a comment
new Comment
Markdown input: edit mode selected.
Write
Preview

Assignees
No one - Assign yourself
Labels
No labels
Projects
No projects
Milestone
No milestone
Relationships
None yet
Development
Create a branch for this issue or link a pull request.
NotificationsCustomize
You're receiving notifications because you're subscribed to this thread.
Participants
@carlopantax
Issue actions
Transfer issue
Lock conversation
Pin issue
Delete issue
Footer
© 2025 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Docs
Contact
Manage cookies
Do not share my personal information
Lab1 Peer Review · Issue #1 · Blackhand01/CI2024_lab1

---
Lab2:
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
Rewiew on lab2:
Skip to content
Navigation Menu
Blackhand01
CI2024_lab2
 
Type / to search
Code
Issues
2
Pull requests
Actions
Projects
Wiki
Security
Insights
Settings
Review #2
Open
@mericuluca
Description
mericuluca
opened on Nov 14, 2024
Hi, it is such a good solution and it was easy to understand what you did because you explained it very well. There are somethings that came to my mind when I read your code. To enhance performance, you can consider using parallel processing and caching distance matrices to speed up calculations. Additionally, instead of sorting each tournament sample to find the best candidate, using a simple minimum function could enhance efficiency. Lastly, implementing an early stopping mechanism when the solution stabilizes over several generations can save computational time.
Activity
Blackhand01
Add a comment
new Comment
Markdown input: edit mode selected.
Write
Preview

Assignees
No one - Assign yourself
Labels
No labels
Projects
No projects
Milestone
No milestone
Relationships
None yet
Development
Create a branch for this issue or link a pull request.
NotificationsCustomize
You're receiving notifications because you're subscribed to this thread.
Participants
@mericuluca
Issue actions
Transfer issue
Lock conversation
Pin issue
Delete issue
Footer
© 2025 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Docs
Contact
Manage cookies
Do not share my personal information
Review · Issue #2 · Blackhand01/CI2024_lab2
Skip to content
Navigation Menu
Blackhand01
CI2024_lab2
 
Type / to search
Code
Issues
2
Pull requests
Actions
Projects
Wiki
Security
Insights
Settings
Lab2 report #1
Open
@FruttoCheap
Description
FruttoCheap
opened on Nov 11, 2024
Strengths
Well-organized Structure: Each section of the notebook (from utility functions to the main algorithms) is logically ordered, making it easy to follow.
Detailed Explanations: The notebook is comprehensive, with explanations on each function’s purpose and parameters. This is particularly helpful for others who might review or adapt the code.
Clear Logging and Error Handling: Logging is used to track progress, errors, and key metrics. This is valuable for debugging and analyzing intermediate results.
Data Management: The code provides mechanisms to handle multiple datasets, adapt population sizes based on city count, and save results efficiently. This makes it easily extendable to different datasets.
Plotting: Progression plotting for both algorithms offers visual insights into the convergence rates and performance.
Recommendations for Improvement
Here are some suggestions to refine and potentially optimize the notebook further:

Performance Enhancements
Parallelization: Consider using parallel processing to speed up the computation of distance matrices or genetic algorithm operations, especially if handling larger datasets.
Distance Matrix Caching: If datasets are reused, save computed distance matrices to disk to avoid recalculating them repeatedly. For instance, use np.save and np.load to store and reload these matrices.
Algorithm Optimization
Tournament Selection Optimization: The tournament_selection function currently sorts each tournament sample every time it runs, which could be slow with larger populations. You could consider using min to find the best individual instead of sorting the entire sample.
Dynamic Mutation Rate: The mutation rate decreases linearly across generations, which is good for stability but could benefit from an adaptive approach. For instance, decreasing the mutation rate only if the solution stagnates for several generations.
Enhanced Plotting
Cost Improvement Plots: While the progression plots show convergence, plotting the rate of improvement or percentage improvement per generation/step can provide additional insight.
Comparison Plot: After the algorithms have completed, consider a side-by-side plot to compare the final costs of the GA and Greedy algorithms across datasets.
Additional Genetic Algorithm Enhancements
Diverse Initialization: The initial population can be seeded with a few known heuristics (like the greedy solution), which might improve GA’s convergence speed.
Alternate Crossover and Mutation Methods: Other crossover mechanisms like partially matched crossover (PMX) or mutation methods like swap mutation might be worth experimenting with, as they can sometimes yield better results for TSP.
Code Modularity and Reusability
Parameterization of Crossover and Mutation Rates: These could be set as parameters in the ea_tsp function to allow for easier experimentation with different values.
Separating Utility Functions into a Module: You might move utility functions into a separate Python module. This can make the notebook cleaner and also enable code reuse in other projects.
Documentation and Comments
Detailed Docstrings: Consider adding docstrings with example inputs/outputs for complex functions like order_crossover or inversion_mutation, especially for readers who may not be familiar with GA operations.
Explain Genetic Parameters: Adding brief explanations for why certain values (e.g., mutation rate, population size) were chosen would help readers understand the reasoning behind those choices.
Handling Large Datasets Gracefully
Memory Management: Loading large datasets into memory could cause issues. Consider limiting datasets by chunks or breaking the dataset into batches if resources are constrained.
Early Termination: Implement early stopping in ea_tsp when the best solution doesn’t improve for a certain number of generations, which would save time when results are close to optimal.
Extended Result Analysis
Result Aggregation: Including summary statistics (e.g., average tour cost across datasets, standard deviation) in the final output file would add insight into the overall performance of each algorithm.
Hyperparameter Tuning: Consider adding a section to test different population sizes, mutation rates, or number of generations for the GA. Plotting the outcomes based on these variations could guide tuning.
Activity
Blackhand01
Add a comment
new Comment
Markdown input: edit mode selected.
Write
Preview

Assignees
No one - Assign yourself
Labels
No labels
Projects
No projects
Milestone
No milestone
Relationships
None yet
Development
Create a branch for this issue or link a pull request.
NotificationsCustomize
You're receiving notifications because you're subscribed to this thread.
Participants
@FruttoCheap
Issue actions
Transfer issue
Lock conversation
Pin issue
Delete issue
Footer
© 2025 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Docs
Contact
Manage cookies
Do not share my personal information
Lab2 report · Issue #1 · Blackhand01/CI2024_lab2
---

Lab3:
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

Review on Lab3:
Skip to content
Navigation Menu
Blackhand01
CI2024_lab3
 
Type / to search
Code
Issues
2
Pull requests
Actions
Projects
Wiki
Security
Insights
Settings
Review #2
Open
@Gabry323387
Description
Gabry323387
opened on Dec 1, 2024
Your code is good and well-structured. The bidirectional A* approach is a very good idea to create an approach which improves the efficiency of your search process.
However, in order to show the actual improvement of your code, a mechanism which visualizes the comparison between your model and the classical A* algorithm could be helpful.
Great work!
Activity
Blackhand01
Add a comment
new Comment
Markdown input: edit mode selected.
Write
Preview

Assignees
No one - Assign yourself
Labels
No labels
Projects
No projects
Milestone
No milestone
Relationships
None yet
Development
Create a branch for this issue or link a pull request.
NotificationsCustomize
You're receiving notifications because you're subscribed to this thread.
Participants
@Gabry323387
Issue actions
Transfer issue
Lock conversation
Pin issue
Delete issue
Footer
© 2025 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Docs
Contact
Manage cookies
Do not share my personal information
Review · Issue #2 · Blackhand01/CI2024_lab3

Skip to content
Navigation Menu
Blackhand01
CI2024_lab3
 
Type / to search
Code
Issues
2
Pull requests
Actions
Projects
Wiki
Security
Insights
Settings
Review #1
Open
@imEmaa
Description
imEmaa
opened on Nov 30, 2024
The idea of a bidirectional a* search is very interesting, but i would be great if you also put a comparison in terms of efficiency between this approach and a standard A*.
To improve efficiency you can read online, or in my lab3 readme, about "Linear Conflict Distance", because this tipe of heuristic reduce the number of nodes evaluated with respect to Manhattan

You did a really nice job with the solver and the report file, which is very clear!
Activity
Blackhand01
Blackhand01 commented on Dec 1, 2024
Blackhand01
on Dec 1, 2024
Owner
Thank you for the feedback!
If you're interested, I've attached a chart comparing the average performance of three algorithms, based on multiple experiments that eventually led me to test the Bidirectional A* strategy. The comparison is based on 50 runs. Here's a summary:

X-Axis: Analyzed algorithms.
Y-Axis: Average efficiency, calculated as the ratio between solution quality and cost (number of explored nodes).
Results:
Bidirectional A*: The most efficient algorithm, with an average efficiency of 65.09.
A*: Second place, with an average efficiency of 57.42.
IDA*: The least efficient of the three, with an average efficiency of 49.87.
Regarding the IDA* algorithm (Iterative Deepening A*), it combines iterative deepening with heuristic-based evaluation, as in A*. It incrementally increases a cost limit, exploring only nodes with costs below or equal to the current limit, until the solution is found.

If you need more details, feel free to ask!

average_efficiency
Blackhand01
Add a comment
new Comment
Markdown input: edit mode selected.
Write
Preview

Assignees
No one - Assign yourself
Labels
No labels
Projects
No projects
Milestone
No milestone
Relationships
None yet
Development
Create a branch for this issue or link a pull request.
NotificationsCustomize
You're receiving notifications because you're subscribed to this thread.
Participants
@Blackhand01
@imEmaa
Issue actions
Transfer issue
Lock conversation
Pin issue
Delete issue
Footer
© 2025 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Docs
Contact
Manage cookies
Do not share my personal information
Review · Issue #1 · Blackhand01/CI2024_lab3
