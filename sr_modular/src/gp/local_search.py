import random
import numpy as np

class LocalSearchManager:
    """
    Manager per la ricerca locale che gestisce dinamicamente la scelta tra diversi algoritmi.
    Ottimizzato per modularità e velocità di computazione.
    """

    def __init__(self, stats):
        self.stats = stats
        self.current_solution = None
        self.evaluate = None
        self.algorithms = {
            "simulated_annealing": self.simulated_annealing,
            "tabu_search": self.tabu_search,
            "hill_climbing": self.hill_climbing,
        }
        self.active_algorithm = "hill_climbing"

    def choose_algorithm(self):
        """
        Seleziona dinamicamente l'algoritmo in base alle statistiche.
        """
        if self.stats.get("stagnation", False):
            self.active_algorithm = "simulated_annealing"
        elif self.stats.get("diversity", 0) < 0.1:
            self.active_algorithm = "tabu_search"
        else:
            self.active_algorithm = "hill_climbing"

    def search(self, current_solution, evaluate, **kwargs):
        """
        Esegue la ricerca locale utilizzando l'algoritmo selezionato dinamicamente.

        Args:
            current_solution (np.ndarray): Soluzione iniziale.
            evaluate (callable): Funzione di valutazione.
            **kwargs: Parametri aggiuntivi per gli algoritmi di ricerca.

        Returns:
            np.ndarray: La migliore soluzione trovata.
        """
        self.current_solution = current_solution
        self.evaluate = evaluate

        self.choose_algorithm()
        algorithm = self.algorithms[self.active_algorithm]
        return algorithm(**kwargs)

    def simulated_annealing(self, max_iterations=1000, initial_temp=100, cooling_rate=0.99):
        """
        Implementazione di Simulated Annealing.
        """
        temp = initial_temp
        best_solution = self.current_solution
        best_score = self.evaluate(self.current_solution)

        for _ in range(max_iterations):
            neighbor = self.get_neighbor(self.current_solution)
            neighbor_score = self.evaluate(neighbor)

            if neighbor_score < best_score or random.random() < np.exp((best_score - neighbor_score) / temp):
                self.current_solution = neighbor
                best_score = neighbor_score
                best_solution = neighbor

            temp *= cooling_rate

            if temp < 1e-3:
                break

        return best_solution

    def tabu_search(self, max_iterations=100, tabu_size=10):
        """
        Implementazione di Tabu Search.
        """
        best_solution = self.current_solution
        best_score = self.evaluate(self.current_solution)

        tabu_list = []

        for _ in range(max_iterations):
            neighbors = self.get_neighbors(self.current_solution)
            best_neighbor = None
            best_neighbor_score = float('inf')

            for neighbor in neighbors:
                if neighbor not in tabu_list:
                    score = self.evaluate(neighbor)
                    if score < best_neighbor_score:
                        best_neighbor = neighbor
                        best_neighbor_score = score

            if best_neighbor is not None:
                self.current_solution = best_neighbor
                tabu_list.append(best_neighbor)
                if len(tabu_list) > tabu_size:
                    tabu_list.pop(0)

                if best_neighbor_score < best_score:
                    best_solution = best_neighbor
                    best_score = best_neighbor_score

        return best_solution

    def hill_climbing(self, max_iterations=100):
        """
        Implementazione di Hill Climbing.
        """
        best_solution = self.current_solution
        best_score = self.evaluate(self.current_solution)

        for _ in range(max_iterations):
            neighbor = self.get_neighbor(self.current_solution)
            neighbor_score = self.evaluate(neighbor)

            if neighbor_score < best_score:
                best_solution = neighbor
                best_score = neighbor_score

        return best_solution

    @staticmethod
    def get_neighbor(solution):
        """
        Genera una soluzione vicina.

        Args:
            solution (np.ndarray): Soluzione corrente.

        Returns:
            np.ndarray: Soluzione vicina.
        """
        return solution.copy() + np.random.uniform(-0.1, 0.1, size=solution.shape)

    @staticmethod
    def get_neighbors(solution, n_neighbors=5):
        """
        Genera un insieme di soluzioni vicine.

        Args:
            solution (np.ndarray): Soluzione corrente.
            n_neighbors (int): Numero di soluzioni vicine da generare.

        Returns:
            list: Lista di soluzioni vicine.
        """
        return [solution + np.random.uniform(-0.1, 0.1, size=solution.shape) for _ in range(n_neighbors)]
