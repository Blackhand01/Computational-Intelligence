import numpy as np
from tqdm.auto import tqdm
import matplotlib.pyplot as plt
import os
from itertools import accumulate
import math

# Global variables for the instance
UNIVERSE_SIZE = None
NUM_SETS = None
DENSITY = None
rng = None

SETS = None
COSTS = None

INITIAL_TEMPERATURE = 1000
COOLING_RATE = 0.996

def initialize_universe(universe_size, num_sets, density):
    global UNIVERSE_SIZE, NUM_SETS, DENSITY, rng, SETS, COSTS
    UNIVERSE_SIZE = universe_size
    NUM_SETS = num_sets
    DENSITY = density
    seed = [UNIVERSE_SIZE, NUM_SETS, int(10_000 * DENSITY)]
    rng = np.random.default_rng(np.random.PCG64(seed))
    
    SETS = rng.random((NUM_SETS, UNIVERSE_SIZE)) < DENSITY
    for s in range(UNIVERSE_SIZE):
        if not np.any(SETS[:, s]):
            SETS[rng.integers(NUM_SETS), s] = True
    COSTS = np.power(SETS.sum(axis=1), 1.1)

def tweak(solution, elements):
    candidate = solution.copy()
    selected_index = rng.integers(0, NUM_SETS)
    candidate[selected_index] = not candidate[selected_index]
    change = 1 if candidate[selected_index] else -1

    if change == -1 and np.any(elements[SETS[selected_index]] <= 1):
        return solution, elements  # Prevent invalid solution

    updated_elements = elements + change * SETS[selected_index]
    return candidate, updated_elements

def calculate_cost(solution):
    return COSTS[solution].sum()

def fitness(solution, elements):
    return np.sum(elements > 0), -calculate_cost(solution)

def RMHC(max_steps):
    solution = rng.random(NUM_SETS) < 0.5
    elements = SETS[solution].sum(axis=0)
    best_solution, best_fitness = solution.copy(), fitness(solution, elements)
    best_step = 0
    history = [best_fitness]

    with tqdm(total=max_steps, desc="Hill Climbing Progress", leave=True) as pbar:
        for step in range(max_steps):
            candidate, candidate_elements = tweak(solution, elements)
            candidate_fitness = fitness(candidate, candidate_elements)
            history.append(candidate_fitness)

            if candidate_fitness > best_fitness:
                solution, elements = candidate, candidate_elements
                best_solution, best_fitness = solution.copy(), candidate_fitness
                best_step = step + 1
            
            pbar.update(1)
            
        exec_time = pbar.format_dict["elapsed"]
        minutes, seconds = divmod(exec_time, 60)
        milliseconds = int((exec_time - int(exec_time)) * 1000)

    return best_solution, best_fitness, best_step, (int(minutes), int(seconds), milliseconds), history

def simulated_annealing(max_steps):
    solution = rng.random(NUM_SETS) < 0.5
    elements = SETS[solution].sum(axis=0)
    best_solution = solution.copy()
    current_fitness = fitness(solution, elements)
    history = [current_fitness]
    temperature = INITIAL_TEMPERATURE
    best_step = 0

    with tqdm(total=max_steps, desc="Simulated Annealing Progress", leave=True) as pbar:
        for step in range(max_steps):
            candidate, candidate_elements = tweak(solution, elements)
            candidate_fitness = fitness(candidate, candidate_elements)
            fitness_diff = candidate_fitness[1] - current_fitness[1]

            if fitness_diff > 0 or rng.random() < math.exp(fitness_diff / temperature):
                solution, elements = candidate, candidate_elements
                current_fitness = candidate_fitness
                history.append(current_fitness)
                
                if current_fitness > fitness(best_solution, elements):
                    best_solution = solution.copy()
                    best_step = step + 1

            temperature *= COOLING_RATE
            pbar.update(1)

        exec_time = pbar.format_dict["elapsed"]
        minutes, seconds = divmod(exec_time, 60)
        milliseconds = int((exec_time - int(exec_time)) * 1000)

    return best_solution, current_fitness, best_step, (int(minutes), int(seconds), milliseconds), history

def display_statistics(idx, total_cost, best_step, exec_time, algorithm):
    minutes, seconds, milliseconds = exec_time
    print(f"Instance {idx} - Universe Size: {UNIVERSE_SIZE}, Sets: {NUM_SETS}, Density: {DENSITY}")
    print(f"  Algorithm: {algorithm}")
    print(f"  Best step: {best_step}")
    print(f"  Total cost: {total_cost:.2f}")
    print(f"  Execution time: {minutes}m {seconds}s {milliseconds}ms\n")

def plot_fitness_evolution(history, instance_index, algorithm):
    if not os.path.exists("img"):
        os.makedirs("img")

    coverage_scores = [f[0] for f in history]
    fitness_scores = [f[1] for f in history]
    first_full_coverage_step = next(i for i, coverage in enumerate(coverage_scores) if coverage == UNIVERSE_SIZE)

    plt.figure(figsize=(14, 8))
    plt.scatter(first_full_coverage_step, fitness_scores[first_full_coverage_step], color="green", marker="X", s=100, label="First full coverage")
    plt.plot(range(first_full_coverage_step, len(fitness_scores)), list(accumulate(fitness_scores[first_full_coverage_step:], max)), color="red", label="Max accumulated fitness")
    plt.scatter(range(len(fitness_scores)), fitness_scores, marker=".", color="blue", label="Fitness per step")

    plt.title(f"{algorithm} - Instance {instance_index}: Universe Size={UNIVERSE_SIZE}, Sets={NUM_SETS}, Density={DENSITY:.2f}")
    plt.xlabel("Steps")
    plt.ylabel("Fitness")
    plt.legend()
    plt.savefig(f"img/plot_{algorithm}_instance_{instance_index}.png")
    plt.close()

def main():
    instances = [
        {"Universe size": 100, "Num sets": 10, "Density": 0.2, "Max steps": 100},
        {"Universe size": 1000, "Num sets": 100, "Density": 0.2, "Max steps": 1000},
        {"Universe size": 10000, "Num sets": 1000, "Density": 0.2, "Max steps": 10000},
        {"Universe size": 100000, "Num sets": 10000, "Density": 0.1, "Max steps": 100000},
        {"Universe size": 100000, "Num sets": 10000, "Density": 0.2, "Max steps": 100000},
        {"Universe size": 100000, "Num sets": 10000, "Density": 0.3, "Max steps": 100000},
    ]

    for idx, params in enumerate(instances, 1):
        initialize_universe(params["Universe size"], params["Num sets"], params["Density"])

        # Run RMHC
        best_solution, best_fitness, best_step, exec_time, history = RMHC(params["Max steps"])
        total_cost = -best_fitness[1]
        display_statistics(idx, total_cost, best_step, exec_time, "RMHC")
        plot_fitness_evolution(history, idx, "RMHC")

        # Run Simulated Annealing
        best_solution, best_fitness, best_step, exec_time, history = simulated_annealing(params["Max steps"])
        total_cost = -best_fitness[1]
        display_statistics(idx, total_cost, best_step, exec_time, "Simulated Annealing")
        plot_fitness_evolution(history, idx, "Simulated Annealing")

if __name__ == "__main__":
    main()
