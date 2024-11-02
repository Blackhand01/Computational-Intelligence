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

def calculate_cost(solution):
    return COSTS[solution].sum()

def fitness(solution, elements):
    return np.sum(elements > 0), -calculate_cost(solution)

def parent_selection(population):
    # Tournament selection of two parents, returns the one with better fitness
    candidates = rng.choice(population, 2)
    return max(candidates, key=lambda ind: ind["fitness"])

def crossover(parent1, parent2):
    # Single-point crossover with random mask
    mask = rng.random(NUM_SETS) < 0.5
    child = parent1["genome"].copy()
    child[mask] = parent2["genome"][mask]
    return {"genome": child, "fitness": None}

def mutation(individual):
    # Mutation that flips random genes in the genome
    genome = individual["genome"].copy()
    mutation_prob = 0.1  # Mutation rate
    for _ in range(int(mutation_prob * NUM_SETS)):
        index = rng.integers(NUM_SETS)
        genome[index] = not genome[index]
    return {"genome": genome, "fitness": None}

def EA(population_size, offspring_size, max_generations):
    # Initialize population
    population = [{"genome": rng.random(NUM_SETS) < 0.5, "fitness": None} for _ in range(population_size)]
    for ind in population:
        elements = SETS[ind["genome"]].sum(axis=0)
        ind["fitness"] = fitness(ind["genome"], elements)

    history = [max(ind["fitness"] for ind in population)]

    # Evolutionary loop
    with tqdm(total=max_generations, desc="Evolutionary Progress", leave=True) as pbar:
        for gen in range(max_generations):
            offspring = []
            for _ in range(offspring_size):
                if rng.random() < 0.5:
                    parent = parent_selection(population)
                    child = mutation(parent)
                else:
                    parent1 = parent_selection(population)
                    parent2 = parent_selection(population)
                    child = crossover(parent1, parent2)
                
                # Fitness evaluation
                elements = SETS[child["genome"]].sum(axis=0)
                child["fitness"] = fitness(child["genome"], elements)
                offspring.append(child)
            
            # Combine population and offspring, then keep only the best individuals
            population.extend(offspring)
            population = sorted(population, key=lambda ind: ind["fitness"], reverse=True)[:population_size]
            
            # Update history with best fitness of the generation
            history.append(population[0]["fitness"])
            pbar.update(1)

    return population[0], history  # Return the best solution and history of fitness

def display_statistics(idx, total_cost, exec_time):
    minutes, seconds, milliseconds = exec_time
    print(f"Instance {idx} - Universe Size: {UNIVERSE_SIZE}, Sets: {NUM_SETS}, Density: {DENSITY}")
    print(f"  Total cost: {total_cost:.2f}")
    print(f"  Execution time: {minutes}m {seconds}s {milliseconds}ms\n")

def plot_fitness_evolution(history, instance_index, algorithm_name):
    if not os.path.exists("img"):
        os.makedirs("img")

    fitness_scores = [f[1] for f in history]
    plt.figure(figsize=(14, 8))
    plt.plot(range(len(fitness_scores)), fitness_scores, marker=".", color="blue", label="Fitness per generation")

    plt.title(f"{algorithm_name} - Instance {instance_index}: Universe Size={UNIVERSE_SIZE}, Sets={NUM_SETS}, Density={DENSITY:.2f}")
    plt.xlabel("Generations")
    plt.ylabel("Fitness")
    plt.legend()
    plt.savefig(f"img/set_cover/{algorithm_name}_plot_instance_{instance_index}.png")
    plt.close()

def main():
    instances = [
        {"Universe size": 100, "Num sets": 10, "Density": 0.2, "Max generations": 100},
        {"Universe size": 1000, "Num sets": 100, "Density": 0.2, "Max generations": 1000},
        {"Universe size": 10000, "Num sets": 1000, "Density": 0.2, "Max generations": 10000},
        {"Universe size": 100000, "Num sets": 10000, "Density": 0.1, "Max generations": 100000},
        {"Universe size": 100000, "Num sets": 10000, "Density": 0.2, "Max generations": 100000},
        {"Universe size": 100000, "Num sets": 10000, "Density": 0.3, "Max generations": 100000},
    ]

    for idx, params in enumerate(instances, 1):
        initialize_universe(params["Universe size"], params["Num sets"], params["Density"])
        best_solution, history = EA(population_size=10, offspring_size=4, max_generations=params["Max generations"])
        total_cost = -best_solution["fitness"][1]
        
        exec_time = (0, 0, 0)  # Placeholder, insert timing code if needed
        display_statistics(idx, total_cost, exec_time)
        plot_fitness_evolution(history, idx, "Evolutionary Algorithm")

if __name__ == "__main__":
    main()
