import numpy as np
import csv
from evaluator import Evaluator
from plotting import Plotter


class GPStatistics:
    def __init__(self, logger=None):
        """
        Inizializza le metriche.
        """
        self.logger = logger  # Riferimento opzionale al logger

        self.history = {
            "generation": [],
            "best_fitness": [],
            "average_fitness": [],
            "diversity": [],
            "complexity": [],
        }
        self.best_fitness = float('inf')
        self.generations_no_improvement = 0
        self.complexity = 0.0
        self.diversity = 0.0
        self.current_generation = 0

        # Traccia l'uso delle strategie
        self.strategy_usage = {
            "selection": {},
            "crossover": {},
            "mutation": {},
            "local_search": {},
        }
        # Salva le strategie attive nella generazione corrente
        self.last_active_strategies = {}

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

        # Calcola la fitness media
        fitness_values = [
            Evaluator.fitness_function(ind, x, y, bloat_penalty) for ind in population
        ]
        avg_fitness = np.mean(fitness_values)

        # Aggiorna l'uso delle strategie
        for strategy_type, strategy_name in active_strategies.items():
            self._update_strategy_usage(strategy_type, strategy_name)

        # Salva i dati storici
        self.history["generation"].append(self.current_generation)
        self.history["best_fitness"].append(best_fitness_current)
        self.history["average_fitness"].append(avg_fitness)
        self.history["diversity"].append(self.diversity)
        self.history["complexity"].append(self.complexity)
        # Salva le strategie attive per la generazione corrente
        self.last_active_strategies = active_strategies

    def _update_strategy_usage(self, strategy_type, strategy_name):
        """
        Metodo interno per incrementare l'uso di una strategia.
        """
        if strategy_name not in self.strategy_usage[strategy_type]:
            self.strategy_usage[strategy_type][strategy_name] = 0
        self.strategy_usage[strategy_type][strategy_name] += 1

    def update_single_strategy(self, strategy_type: str, old_strategy: str, new_strategy: str, reason: str = ""):
        """
        Aggiorna e registra il cambio di strategia. Notifica anche il logger.

        Args:
            strategy_type (str): Tipo di strategia (es. "mutation", "selection", ecc.).
            old_strategy (str): Strategia precedente.
            new_strategy (str): Nuova strategia attiva.
            reason (str, optional): Motivo del cambiamento.
        """
        if old_strategy != new_strategy:
            self._update_strategy_usage(strategy_type, new_strategy)
            if self.logger:
                message = [f"{strategy_type.capitalize()} strategy changed from {old_strategy} to {new_strategy}"]
                if reason:
                    message.append(f"Reason: {reason}")
                self.logger.log_message(message)

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
        fits = [evaluator.fitness_function(ind, x, y, bloat_penalty) for ind in population]
        fits = np.array(fits)
        fits = fits[np.isfinite(fits)]
        if len(fits) == 0:
            return 0.0
        fits_normalized = (fits - np.min(fits)) / (np.ptp(fits) + 1e-10)
        return float(np.std(fits_normalized))

    def export_history_to_csv(self, file_path):
        """
        Esporta i dati storici in un file CSV.

        Args:
            file_path (str): Percorso del file CSV di output.
        """
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.history.keys())
            writer.writeheader()
            rows = zip(*self.history.values())
            writer.writerows([dict(zip(self.history.keys(), row)) for row in rows])

    def generate_plots(self, output_dir="./output/plots"):
        """
        Genera e salva i grafici a partire dai dati storici.

        Args:
            output_dir (str): Directory in cui salvare i grafici.
        """
        plotter = Plotter(self.history)
        plotter.save_plots(directory=output_dir)

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

    def log_current_strategies(self):
        """
        Invia al logger un messaggio che riassume le strategie attive nella generazione corrente.
        """
        if self.logger and self.last_active_strategies:
            strategies_msg = "Active strategies in Generation {}: ".format(self.current_generation)
            strategies_parts = []
            for strategy_type, strategy in self.last_active_strategies.items():
                strategies_parts.append(f"{strategy_type}={strategy}")
            strategies_msg += ", ".join(strategies_parts)
            self.logger.log_message(strategies_msg)

    def generate_summary(self, output_dir="./output/plots"):
        """
        Genera un riepilogo leggibile delle statistiche e salva i grafici.

        Args:
            output_dir (str): Directory in cui salvare i grafici.
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

        # Genera e salva i grafici
        self.generate_plots(output_dir=output_dir)
        summary.append(f"\nGrafici salvati in: {output_dir}")

        return "\n".join(summary)
