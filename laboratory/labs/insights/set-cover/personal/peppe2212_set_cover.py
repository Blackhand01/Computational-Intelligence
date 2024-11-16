from itertools import accumulate
import numpy as np
import random
from tqdm.auto import tqdm
from matplotlib import pyplot as plt
import math

# Inizializzazione dei parametri globali
var_UNIVERSE_SIZE = [100, 1000, 10000, 100000, 100000, 100000]
var_NUM_SETS = [10, 100, 1000, 10000, 10000, 10000]
var_DENSITY = [0.2, 0.2, 0.2, 0.1, 0.2, 0.3]
MAX_STEPS = 150
SETS, COSTS, rng = None, None, None

def generate_sets_and_costs(universe_size, num_sets, density):
    global SETS, COSTS, rng
    rng = np.random.default_rng(seed=[universe_size, num_sets, int(10_000 * density)])
    SETS = rng.random((num_sets, universe_size)) < density
    for s in range(universe_size):
        if not np.any(SETS[:, s]):
            SETS[rng.integers(num_sets), s] = True
    COSTS = np.power(SETS.sum(axis=1), 1.1)

# Funzioni di utilità
def valid(solution):
    """Verifica se la soluzione copre tutto l'universo"""
    return np.all(np.logical_or.reduce(SETS[solution]))

def cost(solution):
    """Calcola il costo della soluzione"""
    return COSTS[solution].sum()

def fitness(solution):
    """Restituisce il fitness della soluzione (copertura e costo negativo)"""
    return valid(solution), -cost(solution)

def fitness_improved(solution):
    """Restituisce il numero di elementi coperti e il costo negativo"""
    covered_items = np.sum(np.any(SETS[solution], axis=0)), -cost(solution)
    return covered_items

# Funzione per generare un punto di partenza
def starting_point(prob=0.5):
    """Genera un punto di partenza casuale"""
    return rng.random(len(SETS)) < prob

# Funzioni per il grafico
def plot_cost(history):
    """Grafico dell'evoluzione dei costi nel tempo"""
    costs = [c for _, c in history]
    plt.figure(figsize=(14, 8))
    plt.plot(range(len(costs)), list(accumulate(costs, max)), color="red", label="Costo massimo cumulativo")
    plt.scatter(range(len(costs)), costs, marker=".", label="Costo ad ogni step")
    plt.xlabel("Iterazioni")
    plt.ylabel("Valore Fitness")
    plt.legend()
    plt.grid(True)
    plt.show()

# Algoritmo Random Mutation Hill Climbing
def tweak_RMHC(solution):
    """Effettua una piccola modifica alla soluzione"""
    new_solution = solution.copy()
    if rng.random() < 0.5:
        candidates = np.where(~new_solution)[0]
        if candidates.size:
            new_solution[rng.choice(candidates)] = True
    else:
        candidates = np.where(new_solution)[0]
        if candidates.size:
            new_solution[rng.choice(candidates)] = False
    return new_solution

def hill_climb_RMHC(tweak, start_point, fitness_fn, plot_fn, max_steps=MAX_STEPS):
    """Esegue il Random Mutation Hill Climbing"""
    solution = start_point()
    best_solution = solution
    best_fitness = fitness_fn(solution)
    history = [best_fitness]
    for _ in range(max_steps):
        new_solution = tweak(solution)
        new_fitness = fitness_fn(new_solution)
        history.append(new_fitness)
        if new_fitness > best_fitness:
            solution, best_solution, best_fitness = new_solution, new_solution, new_fitness
    plot_fn(history)
    return best_solution

# Algoritmo Simulated Annealing
INITIAL_TEMPERATURE = 1000
COOLING_RATE = 0.996

def simulated_annealing(tweak, start_point, fitness_fn, plot_fn, max_steps=MAX_STEPS):
    """Esegue il Simulated Annealing"""
    solution = start_point()
    best_solution = solution.copy()
    best_fitness = fitness_fn(solution)
    current_fitness = best_fitness
    temperature = INITIAL_TEMPERATURE
    history = [current_fitness]
    
    for _ in range(max_steps):
        new_solution = tweak(solution)
        new_fitness = fitness_fn(new_solution)
        delta_fitness = new_fitness[1] - current_fitness[1]
        
        if delta_fitness > 0 or rng.random() < math.exp(delta_fitness / temperature):
            solution = new_solution
            current_fitness = new_fitness
            history.append(current_fitness)
            if new_fitness > best_fitness and valid(new_solution):
                best_solution, best_fitness = new_solution.copy(), new_fitness
        temperature *= COOLING_RATE
    
    plot_fn(history)
    return best_solution

# Esecuzione per tutte le istanze
for universe_size, num_sets, density in zip(var_UNIVERSE_SIZE, var_NUM_SETS, var_DENSITY):
    generate_sets_and_costs(universe_size, num_sets, density)
    print(f"\nEsecuzione per Universe Size: {universe_size}, Num Sets: {num_sets}, Density: {density}")

    # Hill Climbing
    best_hc_solution = hill_climb_RMHC(tweak_RMHC, starting_point, fitness, plot_cost)
    print(f"Hill Climbing - Soluzione Valida: {valid(best_hc_solution)}, Costo: {cost(best_hc_solution)}")
    
    # Simulated Annealing
    best_sa_solution = simulated_annealing(tweak_RMHC, starting_point, fitness_improved, plot_cost)
    print(f"Simulated Annealing - Soluzione Valida: {valid(best_sa_solution)}, Costo: {cost(best_sa_solution)}")
