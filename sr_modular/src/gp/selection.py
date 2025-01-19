import random
import numpy as np
from tree import Node
from evaluator import Evaluator
class AdaptiveSelectionManager:
    def __init__(self, statistics, logger=None):
        """
        Adaptive selection manager for genetic programming.

        Args:
            statistics (dict): Dictionary containing statistics for decision-making.
            logger (Logger, optional): Logger for recording strategy changes.
        """
        self.statistics = statistics
        self.logger = logger
        self.active_strategy = "elitist"  # Default strategy
        self.previous_strategy = None  # To track changes in strategy
        self.evaluator = Evaluator()

    def tournament_selection(self, population: list[Node], x, y, bloat_penalty: float, tournament_size=3) -> Node:
        """
        Tournament selection strategy.
        """
        competitors = random.sample(population, tournament_size)
        fitness_values = [
            self.evaluator.fitness_function(ind, x, y, bloat_penalty)
            for ind in competitors
        ]
        best_index = np.argmin(fitness_values)
        return competitors[best_index]

    def roulette_selection(self, population: list[Node], x, y, bloat_penalty: float) -> Node:
        """
        Roulette wheel (fitness-proportionate) selection strategy.
        """
        fitness_values = [
            self.evaluator.fitness_function(ind, x, y, bloat_penalty)
            for ind in population
        ]
        scores = [1 / (1 + f) for f in fitness_values]  # Convert fitness to scores
        total = sum(scores)
        pick = random.random() * total
        current = 0
        for ind, s in zip(population, scores):
            current += s
            if current > pick:
                return ind
        return population[-1]  # Fallback

    def rank_selection(self, population: list[Node], x, y, bloat_penalty: float) -> Node:
        """
        Rank-based selection strategy.
        """
        fitness_values = [
            self.evaluator.fitness_function(ind, x, y, bloat_penalty)
            for ind in population
        ]
        sorted_indices = np.argsort(fitness_values)
        ranks = np.arange(1, len(population) + 1)
        probabilities = ranks / ranks.sum()
        return population[np.random.choice(sorted_indices, p=probabilities)]

    def elitist_selection(self, population: list[Node], x, y, bloat_penalty: float) -> Node:
        """
        Always selects the best individual.
        """
        fitness_values = [
            self.evaluator.fitness_function(ind, x, y, bloat_penalty)
            for ind in population
        ]
        best_index = np.argmin(fitness_values)
        return population[best_index]

    def choose_strategy(self):
        """
        Choose the active selection strategy based on statistics and log the reason for changes.
        """
        new_strategy = self.active_strategy  # Default to current strategy
        reason = "Default strategy (elitist)"

        if self.statistics.get("complexity", 0) > 10:
            new_strategy = "rank"
            reason = "High complexity (>10)"
        elif self.statistics.get("diversity", 0) < 5:
            new_strategy = "tournament"
            reason = "Low diversity (<5)"
        elif self.statistics.get("stagnation", False):
            new_strategy = "roulette"
            reason = "Stagnation detected"

        # Log if the strategy changes
        if new_strategy != self.active_strategy:
            self.previous_strategy = self.active_strategy
            self.active_strategy = new_strategy
            if self.logger:
                self.logger.info(
                    [
                        f"Selection strategy changed from {self.previous_strategy} to {self.active_strategy}.",
                        f"Reason: {reason}"
                    ]
                )

    def select(self, population: list[Node], x, y, bloat_penalty: float) -> Node:
        """
        Apply the selected selection strategy to the population.
        """
        self.choose_strategy()
        strategies = {
            "tournament": self.tournament_selection,
            "roulette": self.roulette_selection,
            "rank": self.rank_selection,
            "elitist": self.elitist_selection
        }
        return strategies[self.active_strategy](population, x, y, bloat_penalty)

    def get_active_strategy(self) -> str:
        """
        Return the currently active strategy.
        """
        return self.active_strategy
