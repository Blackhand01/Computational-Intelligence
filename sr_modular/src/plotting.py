import matplotlib.pyplot as plt
import os
import numpy as np

class Plotter:
    def __init__(self, plot_dir, plot_dir_prefix="", history=None):
        """
        Inizializza il plotter con la directory per salvare i grafici.

        Args:
            plot_dir (str): Directory di base per salvare i grafici.
            plot_dir_prefix (str): Prefisso per distinguere i grafici di un problema specifico.
            history (dict): Dizionario contenente i dati storici raccolti da GPStatistics.
        """
        self.plot_dir = os.path.join(plot_dir, plot_dir_prefix)
        os.makedirs(self.plot_dir, exist_ok=True)
        self.history = history

    def save_plot(self, fig, filename):
        """
        Salva il grafico nella directory specificata.

        Args:
            fig (Figure): Oggetto figura di Matplotlib.
            filename (str): Nome del file per il grafico.
        """
        filepath = os.path.join(self.plot_dir, filename)
        fig.savefig(filepath, bbox_inches='tight')
        plt.close(fig)

    def plot_best_fitness(self):
        """
        Traccia l'andamento della migliore fitness per generazione.
        """
        generations = self.history["generation"]
        best_fitness = self.history["best_fitness"]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(generations, best_fitness, label="Best Fitness", linewidth=2, color="blue")
        ax.set_title("Best Fitness Trend")
        ax.set_xlabel("Generations")
        ax.set_ylabel("Best Fitness")
        ax.legend()
        ax.grid()
        self.save_plot(fig, "best_fitness_trend.png")

    def plot_average_fitness(self):
        """
        Traccia l'evoluzione del fitness medio per generazione.
        """
        generations = self.history["generation"]
        avg_fitness = self.history["average_fitness"]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(generations, avg_fitness, label="Average Fitness", linewidth=2, linestyle="--", color="orange")
        ax.set_title("Average Fitness Trend")
        ax.set_xlabel("Generations")
        ax.set_ylabel("Average Fitness")
        ax.legend()
        ax.grid()
        self.save_plot(fig, "average_fitness_trend.png")

    def plot_fitness(self, title="Fitness Trend"):
        """
        Traccia il grafico del best fitness e dell'average fitness.
        """
        generations = self.history["generation"]
        best_fitness = self.history["best_fitness"]
        avg_fitness = self.history["average_fitness"]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(generations, best_fitness, label="Best Fitness", linewidth=2)
        ax.plot(generations, avg_fitness, label="Average Fitness", linestyle="--", linewidth=2)
        ax.set_title(title)
        ax.set_xlabel("Generations")
        ax.set_ylabel("Fitness")
        ax.legend()
        ax.grid()
        self.save_plot(fig, "fitness_trend.png")

    def plot_diversity(self, title="Diversity Trend"):
        """
        Traccia il grafico della diversità della popolazione.
        """
        generations = self.history["generation"]
        diversity = self.history["diversity"]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(generations, diversity, label="Diversity", color="orange", linewidth=2)
        ax.set_title(title)
        ax.set_xlabel("Generations")
        ax.set_ylabel("Diversity")
        ax.legend()
        ax.grid()
        self.save_plot(fig, "diversity_trend.png")

    def plot_complexity(self, title="Complexity Trend"):
        """
        Traccia il grafico della complessità media della popolazione.
        """
        generations = self.history["generation"]
        complexity = self.history["complexity"]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(generations, complexity, label="Complexity", color="green", linewidth=2)
        ax.set_title(title)
        ax.set_xlabel("Generations")
        ax.set_ylabel("Complexity")
        ax.legend()
        ax.grid()
        self.save_plot(fig, "complexity_trend.png")

    def plot_operation_frequencies(self, strategy_usage):
        """
        Diagrammi a barre che mostrano la frequenza relativa di operazioni applicate per generazione.

        Args:
            strategy_usage (dict): Uso delle strategie per operazione e generazione.
        """
        generations = sorted(list(strategy_usage["selection"].keys()))
        operations = ["selection", "crossover", "mutation"]

        operation_counts = {
            op: [strategy_usage[op].get(g, 0) for g in generations]
            for op in operations
        }

        x = np.arange(len(generations))
        bar_width = 0.25

        fig, ax = plt.subplots(figsize=(12, 6))
        for i, op in enumerate(operations):
            ax.bar(x + i * bar_width, operation_counts[op], width=bar_width, label=op.capitalize())

        ax.set_title("Operation Frequencies per Generation")
        ax.set_xlabel("Generations")
        ax.set_ylabel("Frequency")
        ax.set_xticks(x + bar_width)
        ax.set_xticklabels(generations, rotation=45)
        ax.legend()
        ax.grid(axis='y')
        self.save_plot(fig, "operation_frequencies.png")

    def plot_exploration_vs_exploitation(self, exploration_counts, exploitation_counts):
        """
        Grafico che confronta esplorazione vs sfruttamento nel tempo.

        Args:
            exploration_counts (list): Numero di nuove soluzioni generate per generazione.
            exploitation_counts (list): Numero di soluzioni migliorate localmente per generazione.
        """
        generations = self.history["generation"]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(generations, exploration_counts, label="Exploration (New Solutions)", linewidth=2, color="green")
        ax.plot(generations, exploitation_counts, label="Exploitation (Local Improvement)", linewidth=2, linestyle="--", color="red")
        ax.set_title("Exploration vs Exploitation")
        ax.set_xlabel("Generations")
        ax.set_ylabel("Count")
        ax.legend()
        ax.grid()
        self.save_plot(fig, "exploration_vs_exploitation.png")

    def save_all_plots(self, strategy_usage, exploration_counts=None, exploitation_counts=None):
        """
        Genera e salva tutti i grafici rilevanti.
        """
        self.plot_best_fitness()
        self.plot_average_fitness()
        self.plot_fitness()
        self.plot_diversity()
        self.plot_complexity()
        self.plot_operation_frequencies(strategy_usage)
        if exploration_counts and exploitation_counts:
            self.plot_exploration_vs_exploitation(exploration_counts, exploitation_counts)
