# File: src/core/fitness.py

import numpy as np
from typing import Callable, List
from src.core.tree import Tree

class FitnessEvaluator:
    """
    Classe per valutare il fitness degli alberi in una popolazione.
    """
    def __init__(self, y_true: np.ndarray, alpha: float = 0.01):
        """
        Inizializza il valutatore di fitness.

        Args:
            y_true (np.ndarray): Valori target reali.
            alpha (float): Fattore di penalizzazione per la complessità dell'albero.
        """
        self.y_true = y_true
        self.alpha = alpha

    def mse(self, y_pred: np.ndarray) -> float:
        """
        Calcola l'errore quadratico medio tra valori attesi e predetti.

        Args:
            y_pred (np.ndarray): Valori predetti dall'albero.

        Returns:
            float: Errore quadratico medio.
        """
        return np.mean((self.y_true - y_pred) ** 2)

    def parsimony_penalty(self, tree: Tree) -> float:
        """
        Calcola una penalizzazione per alberi di grandi dimensioni.

        Args:
            tree (Tree): Albero da valutare.

        Returns:
            float: Penalizzazione basata sulla dimensione dell'albero.
        """
        return self.alpha * tree.size()

    def fitness(self, tree: Tree) -> float:
        """
        Calcola il valore di fitness per un albero, considerando sia l'accuratezza
        che una penalizzazione per complessità eccessiva.

        Args:
            tree (Tree): Albero da valutare.

        Returns:
            float: Valore di fitness (più basso è meglio).
        """
        try:
            y_pred = tree.evaluate(self.y_true)
            mse_error = self.mse(y_pred)
            penalty = self.parsimony_penalty(tree)
            return mse_error + penalty
        except Exception as e:
            # Penalizza drasticamente gli alberi che non possono essere valutati
            print(f"Errore durante la valutazione dell'albero: {e}")
            return float("inf")

    def evaluate_population(self, population: List[Tree]) -> List[float]:
        """
        Valuta l'intera popolazione e restituisce una lista di punteggi di fitness.

        Args:
            population (List[Tree]): Lista di alberi da valutare.

        Returns:
            List[float]: Lista dei punteggi di fitness per ogni albero.
        """
        fitness_scores = []
        for tree in population:
            fitness_score = self.fitness(tree)
            fitness_scores.append(fitness_score)
        return fitness_scores

    
def validate_fitness_scores(fitness_scores: list) -> bool:
    """
    Validates fitness scores for structural correctness.

    Args:
        fitness_scores (list): List of fitness scores to validate.

    Returns:
        bool: True if the scores are valid, False otherwise.
    """
    try:
        # Convert to NumPy array
        fitness_scores = np.array(fitness_scores, dtype=np.float64)

        # Check for NaN or infinite values
        if not np.all(np.isfinite(fitness_scores)):
            return False

        # # Optional: enforce non-negative fitness scores
        # if np.any(fitness_scores < 0):
        #     return False

        return True
    except Exception as e:
        print(f"Error during fitness score validation: {e}")
        return False
