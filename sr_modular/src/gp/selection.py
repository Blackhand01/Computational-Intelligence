import random
from abc import ABC, abstractmethod
from typing import List
import numpy as np
from tree import Node
from evaluator import Evaluator

class BaseSelectionStrategy(ABC):
    """
    Abstract base class for selection strategies (tournament, roulette, etc.).
    """

    @abstractmethod
    def select(self, population: List[Node], x, y, bloat_penalty: float) -> Node:
        pass

class TournamentSelection(BaseSelectionStrategy):
    """
    Tournament selection strategy.
    """

    def __init__(self, tournament_size=3):
        self.tournament_size = tournament_size
        self.evaluator = Evaluator()

    def select(self, population: List[Node], x, y, bloat_penalty: float) -> Node:
        competitors = random.sample(population, self.tournament_size)
        fitness_values = [
            self.evaluator.fitness_function(ind, x, y, bloat_penalty)
            for ind in competitors
        ]
        best_index = np.argmin(fitness_values)
        return competitors[best_index]

class RouletteSelection(BaseSelectionStrategy):
    """
    Roulette wheel (fitness-proportionate) selection strategy.
    """

    def __init__(self):
        self.evaluator = Evaluator()

    def select(self, population: List[Node], x, y, bloat_penalty: float) -> Node:
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

class RankSelection(BaseSelectionStrategy):
    """
    Rank-based selection strategy.
    """

    def __init__(self):
        self.evaluator = Evaluator()

    def select(self, population: List[Node], x, y, bloat_penalty: float) -> Node:
        fitness_values = [
            self.evaluator.fitness_function(ind, x, y, bloat_penalty)
            for ind in population
        ]
        sorted_indices = np.argsort(fitness_values)
        ranks = np.arange(1, len(population) + 1)
        probabilities = ranks / ranks.sum()
        return population[np.random.choice(sorted_indices, p=probabilities)]

class ElitistSelection(BaseSelectionStrategy):
    """
    Always selects the best individual.
    """

    def __init__(self):
        self.evaluator = Evaluator()

    def select(self, population: List[Node], x, y, bloat_penalty: float) -> Node:
        fitness_values = [
            self.evaluator.fitness_function(ind, x, y, bloat_penalty)
            for ind in population
        ]
        best_index = np.argmin(fitness_values)
        return population[best_index]

class AdaptiveSelectionManager:
    def __init__(self, statistics):
        self.strategies = {
            "tournament": TournamentSelection(),
            "roulette": RouletteSelection(),
            "rank": RankSelection(),
            "elitist": ElitistSelection()
        }
        self.statistics = statistics
        self.active_strategy = "elitist"  # Default strategy

    def choose_strategy(self) -> BaseSelectionStrategy:
        if self.statistics.get("complexity", 0) > 10:
            self.active_strategy = "rank"
        elif self.statistics.get("diversity", 0) < 5:
            self.active_strategy = "tournament"
        elif self.statistics.get("stagnation", False):
            self.active_strategy = "roulette"
        else:
            self.active_strategy = "elitist"

        return self.strategies[self.active_strategy]

    def select(self, population: list[Node], x, y, bloat_penalty: float) -> Node:
        chosen_strategy = self.choose_strategy()
        return chosen_strategy.select(population, x, y, bloat_penalty)

    def get_active_strategy(self) -> str:
        """Restituisce la strategia attiva."""
        return self.active_strategy
