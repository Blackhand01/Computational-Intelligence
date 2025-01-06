# File: src/meta_rl/meta_rl_manager.py

"""
Questo modulo implementa un "meta-gestore" basato su Reinforcement Learning (RL)
che coordina diverse tecniche di ricerca:
- Programmazione Genetica (GP)
- Ricerca Locale (Simulated Annealing e Tabu Search)
- Random Restart

L'idea è trattare l'intero processo come un problema di apprendimento per rinforzo,
dove stati, azioni e ricompense sono definiti in base ai progressi (fitness) e
alla diversità della popolazione.

Per adattarlo ai tuoi scopi:
- Integra le funzioni GP, SA, TS e random_restart definite in altri moduli
- Scegli la definizione di stato, le azioni e la funzione di ricompensa (reward)
- Implementa un algoritmo di RL (es. Q-Learning, SARSA) che apprenda una policy
  per massimizzare la ricompensa e, di conseguenza, il miglioramento di fitness.
"""

import numpy as np
from typing import List, Dict, Tuple
from src.operators.local_search import simulated_annealing, tabu_search
from src.core.tree import Tree
from src.core.genetic_programming import GeneticProgram
from src.core.fitness import FitnessEvaluator
from src.operators.mutation import MutationOperator
from src.operators.crossover import CrossoverOperator

# Se hai funzioni più semplici (placeholder) per GP, SA, TS, importale al posto
# di GeneticProgram e local_search. Oppure richiama direttamente i metodi.

# ---------------------- ESEMPI DI FUNZIONI CHE DEFINISCONO RL ---------------------- #

def extract_state(population: List[Tree], fitness_scores: List[float], generations_no_improvement: int) -> Tuple[float, float, int, int]:
    """
    Costruisce lo 'stato' RL come una tupla di feature:
      (best_fitness, avg_fitness, generations_no_improvement, pop_size).

    Args:
        population (List[Tree]): Lista di individui (alberi).
        fitness_scores (List[float]): Lista dei punteggi di fitness corrispondenti.
        generations_no_improvement (int): Generazioni consecutive senza miglioramenti.

    Returns:
        Tuple[float, float, int, int]: Stato rappresentato da 4 valori.
    """
    if not fitness_scores:
        best_fitness = 1e9
        avg_fitness = 1e9
    else:
        best_fitness = min(fitness_scores)
        avg_fitness = float(np.mean(fitness_scores))

    pop_size = len(population)
    # Arrotonda best_fitness e avg_fitness per stabilità (se usi Q-table come dict)
    return (round(best_fitness, 4), round(avg_fitness, 4), generations_no_improvement, pop_size)


def compute_reward(old_state: Tuple[float, float, int, int],
                   new_state: Tuple[float, float, int, int]) -> float:
    """
    Calcola la ricompensa (reward) in base al miglioramento della fitness.

    Esempio: reward = differenza (old_best_fitness - new_best_fitness).
    Se < 0 => peggioramento.
    """
    old_best_fitness = old_state[0]
    new_best_fitness = new_state[0]
    reward = old_best_fitness - new_best_fitness
    return reward


# ---------------------- AZIONI METASTRATEGICHE ---------------------- #

def apply_gp(population: List[Tree],
             fitness_scores: List[float],
             x: np.ndarray,
             fitness_evaluator: FitnessEvaluator,
             num_generations: int = 1) -> List[Tree]:
    """
    Esegue un certo numero di generazioni di Programmazione Genetica su tutta la popolazione.

    Args:
        population (List[Tree]): Popolazione di alberi.
        fitness_scores (List[float]): Punteggi di fitness corrispondenti.
        x (np.ndarray): Dati di input per valutare la fitness.
        fitness_evaluator (FitnessEvaluator): Oggetto per calcolare la fitness.
        num_generations (int): Quante generazioni di GP eseguire (default: 1).

    Returns:
        List[Tree]: Nuova popolazione aggiornata dopo le generazioni GP.
    """
    # Invece di definire tutto da zero, potresti usare GeneticProgram:
    # 1) Crei un'istanza fittizia di GeneticProgram
    gp_temp = GeneticProgram(
        population_size=len(population),
        max_generations=num_generations,
        max_tree_depth=6,
        mutation_rate=0.3,
        crossover_rate=0.7,
        fitness_evaluator=fitness_evaluator,
    )

    # Sostituisci la popolazione iniziale con la tua
    gp_temp.population = population
    gp_temp.fitness_scores = fitness_scores  # Se vuoi mantenerli
    # Esegui .run() => evolverà la popolazione per `num_generations`
    gp_temp.run(x, max_no_improvement=num_generations * 2)  # giusto per fermarlo
    return gp_temp.population


def apply_sa(population: List[Tree],
             fitness_scores: List[float],
             x: np.ndarray,
             fitness_evaluator: FitnessEvaluator,
             max_iterations: int = 100) -> List[Tree]:
    """
    Esegue Simulated Annealing su un sottoinsieme di individui promettenti della popolazione.
    """
    new_population = list(population)  # copia
    sorted_indices = np.argsort(fitness_scores)
    top_k_indices = sorted_indices[:3]  # ad es. prendi i 3 migliori

    for idx in top_k_indices:
        best_solution = simulated_annealing(
            initial_solution=new_population[idx],
            fitness_function=lambda ind: fitness_evaluator.fitness(ind, x),
            max_iterations=max_iterations,
            initial_temperature=100.0,
            cooling_rate=0.95
        )
        new_population[idx] = best_solution

    return new_population


def apply_ts(population: List[Tree],
             fitness_scores: List[float],
             x: np.ndarray,
             fitness_evaluator: FitnessEvaluator,
             max_iterations: int = 100) -> List[Tree]:
    """
    Esegue Tabu Search su un sottoinsieme di individui "bloccati" (ad es. i peggiori).
    """
    new_population = list(population)
    sorted_indices = np.argsort(fitness_scores)
    worst_k_indices = sorted_indices[-3:]  # peggiori 3

    for idx in worst_k_indices:
        best_solution = tabu_search(
            initial_solution=new_population[idx],
            fitness_function=lambda ind: fitness_evaluator.fitness(ind, x),
            max_iterations=max_iterations,
            tabu_list_size=5,
            neighborhood_size=5
        )
        new_population[idx] = best_solution

    return new_population


def random_restart(population: List[Tree],
                   size: int = 50,
                   max_tree_depth: int = 6) -> List[Tree]:
    """
    Rimpiazza parzialmente o totalmente la popolazione con individui random.
    Qui lo facciamo totalmente per semplicità.

    Args:
        population (List[Tree]): Popolazione corrente.
        size (int): Nuova dimensione popolazione desiderata.
        max_tree_depth (int): Profondità massima dei nuovi alberi.

    Returns:
        List[Tree]: Nuova popolazione random.
    """
    from src.core.tree import Tree
    new_population = [
        Tree.generate_random_tree(max_depth=max_tree_depth, operator_set="basic")
        for _ in range(size)
    ]
    return new_population


# ---------------------- ALGORITMO RL PRINCIPALE ---------------------- #

def rl_meta_algorithm(
    initial_population: List[Tree],
    fitness_evaluator: FitnessEvaluator,
    x: np.ndarray,
    max_steps: int = 50,
    alpha: float = 0.1,
    gamma: float = 0.95,
    epsilon: float = 0.1
) -> List[Tree]:
    """
    Esegue un loop di Reinforcement Learning (Q-Learning) per selezionare azioni meta
    (GP, SA, TS, random restart) massimizzando il miglioramento di fitness.

    Args:
        initial_population (List[Tree]): Popolazione iniziale di alberi.
        fitness_evaluator (FitnessEvaluator): Valutatore di fitness.
        x (np.ndarray): Dati di input per calcolare la fitness.
        max_steps (int): Iterazioni totali del meta-algoritmo.
        alpha (float): Tasso di apprendimento (Q-learning).
        gamma (float): Fattore di sconto.
        epsilon (float): Parametro di esplorazione epsilon-greedy.

    Returns:
        List[Tree]: Popolazione finale (o quella risultante alla fine del loop).
    """
    # Azioni possibili
    actions = ["apply_gp", "apply_sa", "apply_ts", "random_restart"]

    # Inizializza la popolazione e calcola la fitness
    population = initial_population
    fitness_scores = [fitness_evaluator.fitness(ind, x) for ind in population]

    # Q-table = dict con chiave: stato, valore: dict { azione: Q-value }
    Q: Dict[Tuple[float, float, int, int], Dict[str, float]] = {}
    best_global_fitness = min(fitness_scores) if fitness_scores else 1e9
    generations_no_improvement = 0

    # Stato iniziale
    state = extract_state(population, fitness_scores, generations_no_improvement)

    for step in range(max_steps):
        # Se lo stato non è presente in Q, inizializziamo le Q-values
        if state not in Q:
            Q[state] = {a: 0.0 for a in actions}

        # Scegli un'azione con epsilon-greedy
        if np.random.rand() < epsilon:
            action = np.random.choice(actions)
        else:
            # prendi l'azione con Q-value maggiore
            action = max(Q[state], key=Q[state].get)

        # Salva popolazione e fitness per calcolo reward
        old_population = population
        old_fitness_scores = fitness_scores

        # ---------------------------- ESECUZIONE AZIONE ----------------------------
        if action == "apply_gp":
            population = apply_gp(population, fitness_scores, x, fitness_evaluator, num_generations=1)
        elif action == "apply_sa":
            population = apply_sa(population, fitness_scores, x, fitness_evaluator, max_iterations=50)
        elif action == "apply_ts":
            population = apply_ts(population, fitness_scores, x, fitness_evaluator, max_iterations=50)
        elif action == "random_restart":
            population = random_restart(population, size=len(population))

        # Ricalcola la fitness
        fitness_scores = [fitness_evaluator.fitness(ind, x) for ind in population]
        new_best_fitness = min(fitness_scores) if fitness_scores else 1e9

        # Verifica miglioramento best globale
        if new_best_fitness < best_global_fitness:
            best_global_fitness = new_best_fitness
            generations_no_improvement = 0
        else:
            generations_no_improvement += 1

        # Nuovo stato
        new_state = extract_state(population, fitness_scores, generations_no_improvement)

        # Calcoliamo la ricompensa (reward)
        reward = compute_reward(state, new_state)

        # Se il nuovo stato non è in Q, inizializzalo
        if new_state not in Q:
            Q[new_state] = {a: 0.0 for a in actions}

        # Aggiorna la Q-table (Q-learning off-policy)
        old_q = Q[state][action]
        best_future_q = max(Q[new_state].values())

        Q[state][action] = old_q + alpha * (reward + gamma * best_future_q - old_q)

        # Passa al nuovo stato
        state = new_state

    return population
