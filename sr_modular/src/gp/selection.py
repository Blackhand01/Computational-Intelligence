import random
import numpy as np
from tree import Node
from evaluator import Evaluator

class AdaptiveSelectionManager:
    def __init__(self, statistics):
        self.statistics = statistics
        self.active_strategy = "elitist"  # Default strategy
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
        Choose the active selection strategy based on statistics.
        """
        if self.statistics.get("complexity", 0) > 10:
            self.active_strategy = "rank"
        elif self.statistics.get("diversity", 0) < 5:
            self.active_strategy = "tournament"
        elif self.statistics.get("stagnation", False):
            self.active_strategy = "roulette"
        else:
            self.active_strategy = "elitist"

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
