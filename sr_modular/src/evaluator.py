import numpy as np
from tree import evaluate_tree, tree_size

class Evaluator:
    """
    Modulo di valutazione per calcolare l'errore quadratico medio (MSE) e il fitness
    degli alberi generati dalla programmazione genetica (GP).
    """

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
        y_pred = evaluate_tree(tree, x)
        return np.mean((y - y_pred) ** 2)

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
        size = tree_size(tree)
        return mse + bloat_penalty * size

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
        return [Evaluator.fitness_function(tree, x, y, bloat_penalty) for tree in population]

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
            Node: L'albero con la miglior fitness.
        """
        fitness_values = Evaluator.evaluate_population(population, x, y, bloat_penalty)
        best_index = np.argmin(fitness_values)
        return population[best_index], fitness_values[best_index]
