import numpy as np
from tqdm.auto import tqdm
import matplotlib.pyplot as plt
import os
from itertools import accumulate

# Global variables for the instance
UNIVERSE_SIZE = None
NUM_SETS = None
DENSITY = None
rng = None

SETS = None
COSTS = None

def initialize_universe(universe_size, num_sets, density):
    global UNIVERSE_SIZE, NUM_SETS, DENSITY, rng, SETS, COSTS
    UNIVERSE_SIZE = universe_size
    NUM_SETS = num_sets
    DENSITY = density
    seed = [UNIVERSE_SIZE, NUM_SETS, int(10_000 * DENSITY)]
    rng = np.random.default_rng(np.random.PCG64(seed))
    
    # Generate sets with specified density and assign costs
    SETS = rng.random((NUM_SETS, UNIVERSE_SIZE)) < DENSITY
    for s in range(UNIVERSE_SIZE):
        if not np.any(SETS[:, s]):
            SETS[rng.integers(NUM_SETS), s] = True
    COSTS = np.power(SETS.sum(axis=1), 1.1)

def basic_tweak(solution, elements):
    candidate = solution.copy()
    selected_index = rng.integers(0, NUM_SETS)
    candidate[selected_index] = not candidate[selected_index]
    change = 1 if candidate[selected_index] else -1

    if change == -1 and np.any(elements[SETS[selected_index]] <= 1):
        return solution, elements  # Prevent invalid solution by keeping the original

    updated_elements = elements + change * SETS[selected_index]
    return candidate, updated_elements

def multiple_tweak(solution, elements, num_flips=2):
    candidate = solution.copy()
    indices = rng.choice(NUM_SETS, size=num_flips, replace=False)

    for index in indices:
        candidate[index] = not candidate[index]
        change = 1 if candidate[index] else -1
        if change == -1 and np.any(elements[SETS[index]] <= 1):
            candidate[index] = not candidate[index]  # Revert change
        else:
            elements += change * SETS[index]

    return candidate, elements

def probability_tweak(solution, elements, flip_prob=0.1):
    candidate = solution.copy()
    for i in range(NUM_SETS):
        if rng.random() < flip_prob:
            candidate[i] = not candidate[i]
            change = 1 if candidate[i] else -1
            if change == -1 and np.any(elements[SETS[i]] <= 1):
                candidate[i] = not candidate[i]  # Revert change
            else:
                elements += change * SETS[i]

    return candidate, elements

def adaptive_tweak(solution, elements):
    candidate = solution.copy()
    set_cover_counts = SETS.dot(elements > 0)
    low_coverage_sets = np.where(set_cover_counts == np.min(set_cover_counts))[0]
    
    selected_index = rng.choice(low_coverage_sets)
    candidate[selected_index] = not candidate[selected_index]
    change = 1 if candidate[selected_index] else -1

    if change == -1 and np.any(elements[SETS[selected_index]] <= 1):
        return solution, elements  # Keep original solution
    else:
        updated_elements = elements + change * SETS[selected_index]
        return candidate, updated_elements

def weighted_tweak(solution, elements):
    candidate = solution.copy()
    weights = 1 / (COSTS + 1e-6)
    selected_index = rng.choice(NUM_SETS, p=weights / weights.sum())

    candidate[selected_index] = not candidate[selected_index]
    change = 1 if candidate[selected_index] else -1

    if change == -1 and np.any(elements[SETS[selected_index]] <= 1):
        return solution, elements  # Keep original solution
    else:
        updated_elements = elements + change * SETS[selected_index]
        return candidate, updated_elements

def calculate_cost(solution):
    return COSTS[solution].sum()

def fitness(solution, elements):
    return np.sum(elements > 0), -calculate_cost(solution)

def hill_climbing(max_steps, tweak_function):
    global tweak
    tweak = tweak_function
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

def test_tweaks():
    # Define instances with different sizes and densities
    instances = [
        {"Universe size": 100, "Num sets": 10, "Density": 0.2, "Max steps": 100},
        {"Universe size": 1000, "Num sets": 100, "Density": 0.2, "Max steps": 1000},
        {"Universe size": 10000, "Num sets": 1000, "Density": 0.3, "Max steps": 10000},
        {"Universe size": 100000, "Num sets": 10000, "Density": 0.1, "Max steps": 100000},
    ]
    
    # Define the tweak functions to test
    tweaks = [
        ("Basic Tweak", basic_tweak),
        ("Multiple Tweak", multiple_tweak),
        ("Adaptive Tweak", adaptive_tweak),
        ("Weighted Tweak", weighted_tweak),
    ]
    
    # Track results for each tweak
    results = {name: {"cost": [], "steps": [], "time": []} for name, _ in tweaks}
    
    # Run hill climbing for each instance and tweak function
    for idx, params in enumerate(instances, 1):
        initialize_universe(params["Universe size"], params["Num sets"], params["Density"])
        
        for name, tweak_func in tweaks:
            print(f"\nRunning instance {idx} with {name}...")
            
            best_solution, best_fitness, best_step, exec_time, history = hill_climbing(params["Max steps"], tweak_func)
            total_cost = -best_fitness[1]
            
            # Store results
            results[name]["cost"].append(total_cost)
            results[name]["steps"].append(best_step)
            results[name]["time"].append(exec_time[0] * 60 + exec_time[1] + exec_time[2] / 1000)
    
    # Calculate averages and print summary
    for name in results:
        avg_cost = np.mean(results[name]["cost"])
        avg_steps = np.mean(results[name]["steps"])
        avg_time = np.mean(results[name]["time"])
        
        print(f"{name} - Average Cost: {avg_cost:.2f}, Average Steps: {avg_steps:.0f}, Average Time: {avg_time:.2f} seconds")

def main():
    test_tweaks()

if __name__ == "__main__":
    main()
