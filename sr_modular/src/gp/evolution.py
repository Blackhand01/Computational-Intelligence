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
from gp.statistics import GPStatistics


class GeneticProgramming:
    """
    Class to coordinate the Genetic Programming process with adaptive managers
    and an optional local search (memetic approach).
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
        self.selection_manager = AdaptiveSelectionManager(stats.get_stats_dict(), logger)
        self.crossover_manager = AdaptiveCrossoverManager(stats.get_stats_dict(), logger)
        self.mutation_manager = AdaptiveMutationManager(stats.get_stats_dict(), logger)

        # LocalSearchManager per la ricerca locale
        self.local_search_manager = LocalSearchManager(stats.get_stats_dict(), logger)

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
        ranked_pop = sorted(
            population,
            key=lambda ind: self.evaluator.fitness_function(ind, self.x, self.y, self.bloat_penalty),
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

        # Controllo dell'abilitazione della local search
        if ENABLE_LOCAL_SEARCH:
            ls_fraction = 0.1
            num_ls = max(1, int(len(new_population) * ls_fraction))
            new_population = sorted(
                new_population,
                key=lambda ind: self.evaluator.fitness_function(ind, self.x, self.y, self.bloat_penalty),
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
            active_strategies = {
                "selection": self.selection_manager.get_active_strategy(),
                "crossover": self.crossover_manager.get_active_strategy(),
                "mutation": self.mutation_manager.get_active_strategy(),
            }

            # Aggiorna statistiche
            self.stats.update(population, self.x, self.y, self.bloat_penalty, current_fitness, active_strategies)

            # Buffer per i log dei cambiamenti di strategia
            strategy_change_logs = []

            # Aggiorna manager e accumula i log delle strategie
            self.selection_manager.statistics = self.stats.get_stats_dict()
            self.crossover_manager.statistics = self.stats.get_stats_dict()
            self.mutation_manager.statistics = self.stats.get_stats_dict()
            self.local_search_manager.statistics = self.stats.get_stats_dict()

            # Salva i cambiamenti di strategia nel buffer
            strategy_change_logs.append(
                f"Selection strategy changed to {self.selection_manager.get_active_strategy()}."
            )
            strategy_change_logs.append(
                f"Crossover strategy changed to {self.crossover_manager.get_active_strategy()}."
            )
            strategy_change_logs.append(
                f"Mutation strategy changed to {self.mutation_manager.get_active_strategy()}."
            )
            strategy_change_logs.append(
                f"Local search strategy changed to {self.local_search_manager.get_active_strategy()}."
            )

            # Evoluzione + local search
            population = self.evolve_population(population, gen)

            # Logging della generazione (prima dei cambiamenti di strategia)
            self.logger.info(
                f"Generation {gen+1}/{self.generations} - Best Fitness: {current_fitness:.4f}",
                generation=gen + 1,
                best_fitness=current_fitness,
                avg_fitness=np.mean([
                    self.evaluator.fitness_function(ind, self.x, self.y, self.bloat_penalty)
                    for ind in population
                ]),
                diversity=self.stats.diversity,
                complexity=self.stats.complexity,
                strategies=active_strategies,
                local_search=self.local_search_manager.get_active_strategy(),
            )

            # Logging dei cambiamenti di strategia (dopo il log della generazione)
            for log in strategy_change_logs:
                self.logger.log_message(log)

            if self.progress_bar:
                self.progress_bar.update(1)

        return current_best
