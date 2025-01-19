import random
import numpy as np
from tree import Node
from gp.mutation import AdaptiveMutationManager
from gp.crossover import AdaptiveCrossoverManager
from gp.selection import AdaptiveSelectionManager
from gp.local_search import LocalSearchManager
from gp_config import (
    MAX_DEPTH, ELITISM, POP_SIZE, PARTIAL_REINIT_EVERY, PARTIAL_REINIT_RATIO,
    CROSSOVER_RATE, MUTATION_RATE, ENABLE_LOCAL_SEARCH
)
from evaluator import Evaluator


class GeneticProgramming:
    """
    Class to coordinate the Genetic Programming process with adaptive managers
    and an optional local search (memetic approach).
    """
    def __init__(self, n_features, generations, bloat_penalty, stats, progress_bar=None):
        self.n_features = n_features
        self.generations = generations
        self.bloat_penalty = bloat_penalty
        self.stats = stats
        self.progress_bar = progress_bar
        self.evaluator = Evaluator()

        # Initialize adaptive managers
        self.selection_manager = AdaptiveSelectionManager(stats)
        self.crossover_manager = AdaptiveCrossoverManager(stats)
        self.mutation_manager = AdaptiveMutationManager(stats)
        self.local_search_manager = LocalSearchManager(stats)

    def generate_population(self):
        """Create the initial population of trees."""
        return [
            Node.generate_random_tree(MAX_DEPTH, self.n_features, grow=random.random() > 0.5)
            for _ in range(POP_SIZE)
        ]

    def evolve_population(self, population, generation):
        """
        Evolve the population using adaptive strategies, and optionally apply local search
        to improve individuals.
        """
        # Sort the population by fitness (lower is better)
        ranked_pop = sorted(
            population,
            key=lambda ind: self.evaluator.fitness_function(ind, self.x, self.y, self.bloat_penalty)
        )
        new_population = ranked_pop[:ELITISM]

        while len(new_population) < POP_SIZE:
            parent1 = self.selection_manager.select(ranked_pop, self.x, self.y, self.bloat_penalty)
            parent2 = self.selection_manager.select(ranked_pop, self.x, self.y, self.bloat_penalty)

            if random.random() < CROSSOVER_RATE:
                off1, off2 = self.crossover_manager.crossover(parent1, parent2)
            else:
                off1, off2 = Node.copy_tree(parent1), Node.copy_tree(parent2)

            if random.random() < MUTATION_RATE:
                off1 = self.mutation_manager.mutate(off1, self.n_features)
            if random.random() < MUTATION_RATE:
                off2 = self.mutation_manager.mutate(off2, self.n_features)

            new_population.append(off1)
            if len(new_population) < POP_SIZE:
                new_population.append(off2)

        if generation % PARTIAL_REINIT_EVERY == 0 and generation != 0:
            for i in range(int(PARTIAL_REINIT_RATIO * POP_SIZE)):
                new_population[-(i + 1)] = Node.generate_random_tree(MAX_DEPTH, self.n_features, grow=True)

        # Apply local search if enabled
        if ENABLE_LOCAL_SEARCH:
            ls_fraction = 0.2
            num_ls = max(1, int(len(new_population) * ls_fraction))
            new_population = sorted(
                new_population,
                key=lambda ind: self.evaluator.fitness_function(ind, self.x, self.y, self.bloat_penalty)
            )
            for i in range(num_ls):
                improved_ind = self.local_search_manager.local_search(
                    new_population[i], self.x, self.y, self.bloat_penalty
                )
                new_population[i] = improved_ind

        return new_population

    def run(self, x, y):
        """
        Execute the Genetic Programming process.
        """
        self.x = x
        self.y = y
        population = self.generate_population()

        for gen in range(self.generations):
            current_best, current_fitness = self.evaluator.get_best_individual(
                population, self.x, self.y, self.bloat_penalty
            )

            # Retrieve the strategies active before updating statistics.
            old_selection = self.selection_manager.get_active_strategy()
            old_crossover = self.crossover_manager.get_active_strategy()
            old_mutation = self.mutation_manager.get_active_strategy()
            old_local_search = self.local_search_manager.get_active_strategy()

            # Update statistics with current generation metrics and active strategies.
            self.stats.update(
                population,
                self.x,
                self.y,
                self.bloat_penalty,
                best_fitness_current=current_fitness,
                active_strategies={
                    "selection": old_selection,
                    "crossover": old_crossover,
                    "mutation": old_mutation,
                    "local_search": old_local_search,
                }
            )

            # Check for individual strategy changes and update them via GPStatistics.
            self.stats.update_single_strategy(
                "selection", old_selection, self.selection_manager.get_active_strategy()
            )
            self.stats.update_single_strategy(
                "crossover", old_crossover, self.crossover_manager.get_active_strategy()
            )
            self.stats.update_single_strategy(
                "mutation", old_mutation, self.mutation_manager.get_active_strategy()
            )
            self.stats.update_single_strategy(
                "local_search", old_local_search, self.local_search_manager.get_active_strategy()
            )

            # Evolve population for next generation.
            population = self.evolve_population(population, gen)

            # Logging della generazione (inclusi metriche e strategie attive).
            self.stats.logger.info(
                f"Generation {gen+1}/{self.generations} - Best Fitness: {current_fitness:.4f}",
                generation=gen + 1,
                best_fitness=current_fitness,
                avg_fitness=np.mean([
                    self.evaluator.fitness_function(ind, self.x, self.y, self.bloat_penalty)
                    for ind in population
                ]),
                diversity=self.stats.diversity,
                complexity=self.stats.complexity,
                strategies={
                    "selection": self.selection_manager.get_active_strategy(),
                    "crossover": self.crossover_manager.get_active_strategy(),
                    "mutation": self.mutation_manager.get_active_strategy(),
                    "local_search": self.local_search_manager.get_active_strategy(),
                }
            )

            # Log additional message with the strategies active in this generation.
            self.stats.log_current_strategies()

            if self.progress_bar:
                self.progress_bar.update(1)

        return current_best
