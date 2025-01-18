import numpy as np
from evaluator import Evaluator
from tree import Node

class GPStatistics:
    def __init__(self):
        # Esempio di metriche
        self.best_fitness = float('inf')
        self.generations_no_improvement = 0
        self.complexity = 0.0
        self.diversity = 0.0
        self.current_generation = 0

    def update(self, population, x, y, bloat_penalty, best_fitness_current):
        """
        Aggiorna le statistiche in base alla popolazione attuale.
        """
        self.current_generation += 1

        # 1) Stagnation
        if best_fitness_current < self.best_fitness:
            self.best_fitness = best_fitness_current
            self.generations_no_improvement = 0
        else:
            self.generations_no_improvement += 1

        # 2) Complexity: es. media della dimensione degli alberi
        sizes = [ind.tree_size() for ind in population]
        self.complexity = float(np.mean(sizes))

        # 3) Diversity: es. differenza media di fitness
        #   (oppure Hamming distance fra alberi, ecc., qui mettiamo un esempio banale)
        evaluator = Evaluator()
        fits = [evaluator.fitness_function(ind, x, y, bloat_penalty) for ind in population]
        self.diversity = float(np.std(fits))

    def get_stats_dict(self):
        """
        Restituisce un dizionario usato dai manager per selezionare strategie.
        """
        return {
            "complexity": self.complexity,
            "diversity": self.diversity,
            "stagnation": (self.generations_no_improvement > 5)  # es. True se >5 generazioni senza miglioramento
        }
