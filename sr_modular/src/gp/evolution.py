import random
import numpy as np
from tree import Node 
from gp.mutation import AdaptiveMutationManager
from gp.crossover import AdaptiveCrossoverManager
from gp.selection import AdaptiveSelectionManager
from gp_config import (
    MAX_DEPTH, ELITISM, POP_SIZE, PARTIAL_REINIT_EVERY, PARTIAL_REINIT_RATIO, CROSSOVER_RATE, MUTATION_RATE
)
from evaluator import Evaluator
from gp.statistics import GPStatistics

def generate_population(max_depth, n_features):
    """
    Crea la popolazione iniziale.
    """
    population = [
        Node.generate_random_tree(max_depth, n_features, grow=random.random() > 0.5)
        for _ in range(POP_SIZE)
    ]
    return population

def evolve_population(population, x, y, n_features, generation, bloat_penalty, 
                      selection_manager, crossover_manager, mutation_manager, stats):
    """
    Evoluzione della popolazione con manager adattivi.
    """
    evaluator = Evaluator()

    # Ordina la popolazione per fitness
    ranked_pop = sorted(population, key=lambda ind: evaluator.fitness_function(ind, x, y, bloat_penalty))
    new_population = ranked_pop[:ELITISM]  # Elitismo

    while len(new_population) < POP_SIZE:
        # Seleziona genitori dinamicamente
        parent1 = selection_manager.select(ranked_pop, x, y, bloat_penalty)
        parent2 = selection_manager.select(ranked_pop, x, y, bloat_penalty)

        # Crossover dinamico
        if random.random() < CROSSOVER_RATE:
            off1, off2 = crossover_manager.crossover(parent1, parent2)
        else:
            off1, off2 = Node.copy_tree(parent1), Node.copy_tree(parent2)

        # Mutazione dinamica
        if random.random() < MUTATION_RATE:
            off1 = mutation_manager.mutate(off1, n_features)
        if random.random() < MUTATION_RATE:
            off2 = mutation_manager.mutate(off2, n_features)

        new_population.append(off1)
        if len(new_population) < POP_SIZE:
            new_population.append(off2)

    # Partial Reinitialization
    if generation % PARTIAL_REINIT_EVERY == 0 and generation != 0:
        for i in range(int(PARTIAL_REINIT_RATIO * POP_SIZE)):
            new_population[-(i + 1)] = Node.generate_random_tree(MAX_DEPTH, n_features, grow=True)

    return new_population

class GeneticProgramming:
    """
    Coordina la programmazione genetica con manager adattivi.
    """
    @staticmethod
    def run_gp(x, y, n_features, generations, bloat_penalty, logger, stats, progress_bar=None):
        """
        Esegue la programmazione genetica.

        Args:
            x (np.ndarray): Input features.
            y (np.ndarray): Target values.
            n_features (int): Numero di feature disponibili.
            generations (int): Numero di generazioni.
            bloat_penalty (float): Penalità per la dimensione dell'albero.
            logger (Logger): Logger per registrare informazioni.
            stats (GPStatistics): Oggetto per raccogliere statistiche.
            progress_bar (tqdm.tqdm): Barra di progresso opzionale.

        Returns:
            Node: L'individuo migliore trovato.
        """
        population = generate_population(MAX_DEPTH, n_features)
        evaluator = Evaluator()

        # Manager adattivi per selezione, crossover e mutazione
        selection_manager = AdaptiveSelectionManager(stats.get_stats_dict())
        crossover_manager = AdaptiveCrossoverManager(stats.get_stats_dict())
        mutation_manager = AdaptiveMutationManager(stats.get_stats_dict())

        for gen in range(generations):
            # Trova il miglior individuo nella popolazione
            current_best, current_fitness = evaluator.get_best_individual(population, x, y, bloat_penalty)

            # Ottieni le strategie attive
            active_strategies = {
                "selection": selection_manager.get_active_strategy(),
                "crossover": crossover_manager.get_active_strategy(),
                "mutation": mutation_manager.get_active_strategy(),
            }

            # Aggiorna statistiche
            stats.update(population, x, y, bloat_penalty, current_fitness, active_strategies)

            # Passa le statistiche aggiornate ai manager
            selection_manager.statistics = stats.get_stats_dict()
            crossover_manager.statistics = stats.get_stats_dict()
            mutation_manager.statistics = stats.get_stats_dict()

            # Evoluzione della popolazione
            population = evolve_population(
                population, x, y, n_features, gen, bloat_penalty,
                selection_manager, crossover_manager, mutation_manager, stats
            )

            logger.info(
                f"Generation {gen + 1}/{generations} - Best Fitness: {current_fitness:.4f}",
                generation=gen + 1,
                best_fitness=current_fitness,
                avg_fitness=np.mean([evaluator.fitness_function(ind, x, y, bloat_penalty) for ind in population]),
                diversity=stats.diversity,
                complexity=stats.complexity,
                strategies=active_strategies,
            )

            if progress_bar:
                progress_bar.update(1)

        return current_best
