import numpy as np
from core.tree import Node

class Evaluator:
    """
    Modulo di valutazione per calcolare l'errore quadratico medio (MSE) e il fitness
    degli alberi generati dalla programmazione genetica (GP).
    """

    @staticmethod
    def check_validity(array: np.ndarray) -> bool:
        """
        Check if an array contains NaN, infinity, or values outside the allowed range.

        Args:
            array (np.ndarray): Array di valori da verificare.

        Returns:
            bool: True se l'array è valido, False altrimenti.
        """
        return not np.any(np.isnan(array) | np.isinf(array) | (array < -1e6) | (array > 1e6))

    @staticmethod
    def calculate_mse(tree, x, y):
        """
        Calcola l'errore quadratico medio (MSE) tra l'output dell'albero e i valori attesi.

        Args:
            tree (Node): L'albero da valutare.
            x (np.ndarray): Array di input, con feature lungo la prima dimensione.
            y (np.ndarray): Array di output atteso.

        Returns:
            float: Il valore dell'MSE.
        """
        try:
            y_pred = Node.evaluate_tree(tree, x)
            if not Evaluator.check_validity(y_pred):
                return float('inf')  # Penalizza formule che generano output non validi
            return np.mean((y - y_pred) ** 2)
        except Exception as e:
            return float('inf')  # Penalizza formule che generano errori

    @staticmethod
    def fitness_function(tree, x, y, bloat_penalty):
        """
        Calcola la funzione di fitness, combinando MSE e penalità per la dimensione dell'albero (bloat).

        Args:
            tree (Node): L'albero da valutare.
            x (np.ndarray): Array di input, con feature lungo la prima dimensione.
            y (np.ndarray): Array di output atteso.
            bloat_penalty (float): Penalità applicata in base alla dimensione dell'albero.

        Returns:
            float: Il valore della fitness.
        """
        mse = Evaluator.calculate_mse(tree, x, y)
        size = Node.tree_size(tree)
        # Penalità per alberi molto grandi
        penalty = bloat_penalty * size 

        return mse

    @staticmethod
    def evaluate_population(population, x, y, bloat_penalty):
        """
        Valuta una popolazione di alberi e restituisce la lista dei valori di fitness.

        Args:
            population (list[Node]): Lista di alberi da valutare.
            x (np.ndarray): Array di input, con feature lungo la prima dimensione.
            y (np.ndarray): Array di output atteso.
            bloat_penalty (float): Penalità applicata in base alla dimensione degli alberi.

        Returns:
            list[float]: Lista dei valori di fitness per ogni albero.
        """
        fitness_values = []
        for tree in population:
            fitness = Evaluator.fitness_function(tree, x, y, bloat_penalty)
            fitness_values.append(fitness)
        return fitness_values

    @staticmethod
    def get_best_individual(population, x, y, bloat_penalty):
        """
        Restituisce il miglior individuo (albero) della popolazione in base alla fitness.

        Args:
            population (list[Node]): Lista di alberi da valutare.
            x (np.ndarray): Array di input, con feature lungo la prima dimensione.
            y (np.ndarray): Array di output atteso.
            bloat_penalty (float): Penalità applicata in base alla dimensione degli alberi.

        Returns:
            tuple: Il miglior albero e il valore della sua fitness.
        """
        fitness_values = Evaluator.evaluate_population(population, x, y, bloat_penalty)
        best_index = np.argmin(fitness_values)
        return population[best_index], fitness_values[best_index]
