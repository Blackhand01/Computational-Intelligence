import numpy as np
from evaluator import Evaluator

class GPStatistics:
    def __init__(self):
        """
        Inizializza le metriche.
        """
        self.best_fitness = float('inf')
        self.generations_no_improvement = 0
        self.complexity = 0.0
        self.diversity = 0.0
        self.current_generation = 0

        # Traccia l'uso delle strategie
        self.strategy_usage = {
            "selection": {},
            "crossover": {},
            "mutation": {}
        }

    def update(self, population, x, y, bloat_penalty, best_fitness_current, active_strategies):
        """
        Aggiorna le statistiche in base alla popolazione attuale.

        Args:
            population (list): Lista degli individui attuali.
            x (np.ndarray): Input.
            y (np.ndarray): Output atteso.
            bloat_penalty (float): Penalità per la complessità dell'albero.
            best_fitness_current (float): Miglior fitness attuale.
            active_strategies (dict): Strategie attive in questa generazione.
        """
        self.current_generation += 1

        # Stagnation
        if best_fitness_current < self.best_fitness:
            self.best_fitness = best_fitness_current
            self.generations_no_improvement = 0
        else:
            self.generations_no_improvement += 1

        # Complexity
        sizes = [ind.tree_size() for ind in population]
        self.complexity = float(np.mean(sizes))

        # Diversity
        self.diversity = self.calculate_diversity(population, x, y, bloat_penalty)

        # Aggiorna l'uso delle strategie
        for strategy_type, strategy_name in active_strategies.items():
            if strategy_name not in self.strategy_usage[strategy_type]:
                self.strategy_usage[strategy_type][strategy_name] = 0
            self.strategy_usage[strategy_type][strategy_name] += 1

    def calculate_diversity(self, population, x, y, bloat_penalty) -> float:
        """
        Calcola la diversità come deviazione standard dei valori di fitness normalizzati.

        Args:
            population (list): Lista degli individui della popolazione.
            x (np.ndarray): Input.
            y (np.ndarray): Output atteso.
            bloat_penalty (float): Penalità per la complessità dell'albero.

        Returns:
            float: Valore della diversità.
        """
        evaluator = Evaluator()
        fits = [
            evaluator.fitness_function(ind, x, y, bloat_penalty) 
            for ind in population
        ]

        # Rimuovi valori non validi (NaN, inf)
        fits = np.array(fits)
        fits = fits[np.isfinite(fits)]

        if len(fits) == 0:
            return 0.0  # Nessuna diversità se non ci sono valori validi

        # Normalizza i valori di fitness tra 0 e 1
        # Bassa diversità (vicina a 0)
        # Alta diversità (vicina a 1)
        # Valori intermedi (tra 0.3 e 0.7, ad esempio) indicano un equilibrio tra esplorazione e sfruttamento
        fits_normalized = (fits - np.min(fits)) / (np.ptp(fits) + 1e-10)

        # Calcola la deviazione standard
        return float(np.std(fits_normalized))

    def get_stats_dict(self):
        """
        Restituisce un dizionario con le metriche attuali.
        """
        return {
            "generation": self.current_generation,
            "best_fitness": self.best_fitness,
            "diversity": self.diversity,
            "complexity": self.complexity,
            "stagnation": self.generations_no_improvement > 5,
        }

    def get_strategy_usage(self):
        """
        Restituisce un dizionario con l'uso delle strategie.
        """
        return self.strategy_usage

    def generate_summary(self):
        """
        Genera un riepilogo leggibile delle statistiche.
        """
        summary = [
            f"Generazioni totali: {self.current_generation}",
            f"Miglior fitness ottenuto: {self.best_fitness:.4f}",
            f"Diversità finale: {self.diversity:.4f}",
            f"Complessità media finale: {self.complexity:.4f}",
            f"Generazioni senza miglioramenti: {self.generations_no_improvement}",
        ]

        summary.append("\nUso delle strategie:")
        for strategy_type, usage in self.strategy_usage.items():
            summary.append(f"  {strategy_type.capitalize()}:")
            for strategy, count in usage.items():
                summary.append(f"    {strategy}: {count} volte")

        return "\n".join(summary)
