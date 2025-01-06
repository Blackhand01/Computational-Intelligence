# File: src/operators/local_search.py

import numpy as np
import random
from typing import Callable, Any, Optional
from src.core.tree import Tree
from src.core.fitness import FitnessEvaluator

def simulated_annealing(
    initial_solution: Tree,
    fitness_function: Callable[[Tree], float],
    max_iterations: int = 100,
    initial_temperature: float = 100.0,
    cooling_rate: float = 0.95
) -> Tree:
    """
    Esegue Simulated Annealing (SA) su un singolo individuo (Tree).

    Args:
        initial_solution (Tree): Albero di partenza.
        fitness_function (Callable[[Tree], float]): Funzione di fitness da minimizzare.
        max_iterations (int): Numero massimo di iterazioni per la SA.
        initial_temperature (float): Temperatura iniziale.
        cooling_rate (float): Fattore di raffreddamento (es. 0.95).

    Returns:
        Tree: Soluzione (albero) ottimizzata localmente.
    """
    current_solution = initial_solution.copy()
    current_fitness = fitness_function(current_solution)
    best_solution = current_solution
    best_fitness = current_fitness

    temperature = initial_temperature

    for i in range(max_iterations):
        # Genera una soluzione vicina (neighbor)
        neighbor = _small_perturbation(current_solution)
        neighbor_fitness = fitness_function(neighbor)

        # Calcola la variazione di costo
        delta = neighbor_fitness - current_fitness

        if delta < 0:
            # Migliora => accetta sempre
            current_solution = neighbor
            current_fitness = neighbor_fitness
            if neighbor_fitness < best_fitness:
                best_solution = neighbor
                best_fitness = neighbor_fitness
        else:
            # Peggiora => accetta con una certa probabilità dipendente dalla temperatura
            acceptance_probability = np.exp(-delta / (temperature + 1e-9))
            if random.random() < acceptance_probability:
                current_solution = neighbor
                current_fitness = neighbor_fitness

        # Raffredda la temperatura
        temperature *= cooling_rate

    return best_solution


def tabu_search(
    initial_solution: Tree,
    fitness_function: Callable[[Tree], float],
    max_iterations: int = 100,
    tabu_list_size: int = 10,
    neighborhood_size: int = 5
) -> Tree:
    """
    Esegue Tabu Search (TS) su un singolo individuo (Tree).

    Args:
        initial_solution (Tree): Albero iniziale.
        fitness_function (Callable[[Tree], float]): Funzione di fitness da minimizzare.
        max_iterations (int): Iterazioni massime della ricerca tabu.
        tabu_list_size (int): Dimensione massima della lista Tabu.
        neighborhood_size (int): Numero di vicini da generare ogni iterazione.

    Returns:
        Tree: Miglior albero trovato durante la TS.
    """
    current_solution = initial_solution.copy()
    current_fitness = fitness_function(current_solution)
    best_solution = current_solution
    best_fitness = current_fitness

    # In Tabu Search, la Tabu List contiene soluzioni (o mosse) da NON esplorare
    # per evitare di tornare ripetutamente sugli stessi minimi.
    tabu_list = []

    for _ in range(max_iterations):
        neighborhood = _generate_neighbors(current_solution, neighborhood_size)
        
        # Valutiamo ciascun vicino ignorando quelli in tabu_list
        best_neighbor = None
        best_neighbor_fitness = float("inf")

        for neighbor in neighborhood:
            # Identifica la "mosse" (o l'hash) per la tabu list
            # (es. un ID semplificato della struttura)
            neighbor_id = _solution_hash(neighbor)

            if neighbor_id in tabu_list:
                continue  # Skip se è tabù

            neighbor_fitness = fitness_function(neighbor)
            if neighbor_fitness < best_neighbor_fitness:
                best_neighbor = neighbor
                best_neighbor_fitness = neighbor_fitness

        if best_neighbor is None:
            # Se tutti i vicini sono tabu, "liberiamo" la taboo list o forziamo un break
            tabu_list.clear()
            continue

        # Aggiornamento
        current_solution = best_neighbor
        current_fitness = best_neighbor_fitness

        # Aggiorna il best globale
        if current_fitness < best_fitness:
            best_solution = current_solution
            best_fitness = current_fitness

        # Aggiorna la tabu list
        tabu_list.append(_solution_hash(current_solution))
        if len(tabu_list) > tabu_list_size:
            tabu_list.pop(0)

    return best_solution


# ----------------------------- UTILITY FUNCTIONS ----------------------------- #

def _small_perturbation(solution: Tree) -> Tree:
    """
    Genera una perturbazione locale dell'albero (Tree).
    Esempio: mutazione puntuale o sostituzione di un singolo nodo.
    """
    new_tree = solution.copy()
    # Esempio: mutazione "point" su un nodo a caso
    random_node = new_tree.random_node(allow_root=False)
    random_node.mutate_value()
    return new_tree


def _generate_neighbors(solution: Tree, k: int) -> list:
    """
    Genera k soluzioni vicine (neighbors) ad un albero principale.
    Usando piccole perturbazioni multiple.
    """
    neighbors = []
    for _ in range(k):
        neighbor = _small_perturbation(solution)
        neighbors.append(neighbor)
    return neighbors


def _solution_hash(solution: Tree) -> str:
    """
    Calcola un hash (stringa) rappresentativo della struttura dell'albero
    per memorizzarlo in una tabu list. Qui, semplifichiamo a una stringa
    testuale dell'albero (non sempre robusta, ma sufficiente come demo).
    """
    return str(solution)
