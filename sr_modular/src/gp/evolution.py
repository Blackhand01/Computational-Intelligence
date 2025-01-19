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

class GeneticProgramming:
    """
    Class to coordinate the Genetic Programming process with adaptive managers.
    """
    def __init__(self, n_features, generations, bloat_penalty, logger, stats, progress_bar=None):
        self.n_features = n_features
        self.generations = generations
        self.bloat_penalty = bloat_penalty
        self.logger = logger
        self.stats = stats
        self.progress_bar = progress_bar
        self.evaluator = Evaluator()

        # Adaptive managers for selection, crossover, and mutation
        self.selection_manager = AdaptiveSelectionManager(stats.get_stats_dict())
        self.crossover_manager = AdaptiveCrossoverManager(stats.get_stats_dict())
        self.mutation_manager = AdaptiveMutationManager(stats.get_stats_dict())

    def generate_population(self):
        """
        Create the initial population of trees.
        """
        return [
            Node.generate_random_tree(MAX_DEPTH, self.n_features, grow=random.random() > 0.5)
            for _ in range(POP_SIZE)
        ]

    def evolve_population(self, population, generation):
        """
        Evolve the population using adaptive strategies.
        """
        # Sort population by fitness
        ranked_pop = sorted(
            population,
            key=lambda ind: self.evaluator.fitness_function(ind, self.x, self.y, self.bloat_penalty),
        )
        new_population = ranked_pop[:ELITISM]  # Elitism

        while len(new_population) < POP_SIZE:
            # Select parents dynamically
            parent1 = self.selection_manager.select(ranked_pop, self.x, self.y, self.bloat_penalty)
            parent2 = self.selection_manager.select(ranked_pop, self.x, self.y, self.bloat_penalty)

            # Apply crossover dynamically
            if random.random() < CROSSOVER_RATE:
                off1, off2 = self.crossover_manager.crossover(parent1, parent2)
            else:
                off1, off2 = Node.copy_tree(parent1), Node.copy_tree(parent2)

            # Apply mutation dynamically
            if random.random() < MUTATION_RATE:
                off1 = self.mutation_manager.mutate(off1, self.n_features)
            if random.random() < MUTATION_RATE:
                off2 = self.mutation_manager.mutate(off2, self.n_features)

            new_population.append(off1)
            if len(new_population) < POP_SIZE:
                new_population.append(off2)

        # Partial Reinitialization
        if generation % PARTIAL_REINIT_EVERY == 0 and generation != 0:
            for i in range(int(PARTIAL_REINIT_RATIO * POP_SIZE)):
                new_population[-(i + 1)] = Node.generate_random_tree(MAX_DEPTH, self.n_features, grow=True)

        return new_population

    def run(self, x, y):
        """
        Execute the Genetic Programming process.

        Args:
            x (np.ndarray): Input features.
            y (np.ndarray): Target values.

        Returns:
            Node: The best individual found.
        """
        self.x = x
        self.y = y
        population = self.generate_population()

        for gen in range(self.generations):
            # Get the best individual and its fitness
            current_best, current_fitness = self.evaluator.get_best_individual(
                population, self.x, self.y, self.bloat_penalty
            )

            # Get active strategies
            active_strategies = {
                "selection": self.selection_manager.get_active_strategy(),
                "crossover": self.crossover_manager.get_active_strategy(),
                "mutation": self.mutation_manager.get_active_strategy(),
            }

            # Update statistics
            self.stats.update(population, self.x, self.y, self.bloat_penalty, current_fitness, active_strategies)

            # Update managers with new statistics
            self.selection_manager.statistics = self.stats.get_stats_dict()
            self.crossover_manager.statistics = self.stats.get_stats_dict()
            self.mutation_manager.statistics = self.stats.get_stats_dict()

            # Evolve population
            population = self.evolve_population(population, gen)

            # Log generation details
            self.logger.info(
                f"Generation {gen + 1}/{self.generations} - Best Fitness: {current_fitness:.4f}",
                generation=gen + 1,
                best_fitness=current_fitness,
                avg_fitness=np.mean([
                    self.evaluator.fitness_function(ind, self.x, self.y, self.bloat_penalty)
                    for ind in population
                ]),
                diversity=self.stats.diversity,
                complexity=self.stats.complexity,
                strategies=active_strategies,
            )

            if self.progress_bar:
                self.progress_bar.update(1)

        return current_best
