import logging
import os
import csv
from datetime import datetime
from gp_config import POP_SIZE, MAX_DEPTH, N_GENERATIONS, TOURNAMENT_SIZE, MUTATION_RATE, CROSSOVER_RATE, ELITISM, BLOAT_PENALTY


class Logger:
    def __init__(self, log_dir="./logs", log_file_prefix="gp_run"):
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(log_dir, f"{log_file_prefix}_{timestamp}_log.csv")

        # CSV Header
        self.fields = [
            "timestamp",
            "message",
            "generation",
            "best_fitness",
            "average_fitness",
            "diversity",
            "complexity",
            "selection_strategy",
            "crossover_strategy",
            "mutation_strategy",
        ]

        # Write configuration and header to the CSV file
        with open(self.log_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Experiment Configuration"])
            writer.writerow(["POP_SIZE", POP_SIZE])
            writer.writerow(["MAX_DEPTH", MAX_DEPTH])
            writer.writerow(["N_GENERATIONS", N_GENERATIONS])
            writer.writerow(["TOURNAMENT_SIZE", TOURNAMENT_SIZE])
            writer.writerow(["MUTATION_RATE", MUTATION_RATE])
            writer.writerow(["CROSSOVER_RATE", CROSSOVER_RATE])
            writer.writerow(["ELITISM", ELITISM])
            writer.writerow(["BLOAT_PENALTY", BLOAT_PENALTY])
            writer.writerow([])  # Blank line for readability
            writer.writerow(self.fields)

        # Configure console logging
        logging.basicConfig(
            format="%(asctime)s - %(message)s",
            level=logging.INFO,
            handlers=[logging.StreamHandler()]
        )
        self.logger = logging.getLogger("GPLogger")

    def log_to_csv(self, generation=None, best_fitness=None, avg_fitness=None, diversity=None, complexity=None, strategies=None, message=None):
        """Log data into the CSV file."""
        row = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message": message,
            "generation": generation if generation is not None else "",
            "best_fitness": f"{best_fitness:.4f}" if best_fitness is not None else "",
            "average_fitness": f"{avg_fitness:.4f}" if avg_fitness is not None else "",
            "diversity": f"{diversity:.4f}" if diversity is not None else "",
            "complexity": f"{complexity:.4f}" if complexity is not None else "",
            "selection_strategy": strategies.get("selection") if strategies else "",
            "crossover_strategy": strategies.get("crossover") if strategies else "",
            "mutation_strategy": strategies.get("mutation") if strategies else "",
        }
        with open(self.log_file, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fields)
            writer.writerow(row)

    def info(self, message, generation=None, best_fitness=None, avg_fitness=None, diversity=None, complexity=None, strategies=None):
        """Log informational messages to console and CSV."""
        self.logger.info(message)
        self.log_to_csv(
            generation=generation,
            best_fitness=best_fitness,
            avg_fitness=avg_fitness,
            diversity=diversity,
            complexity=complexity,
            strategies=strategies,
            message=message,
        )

    def generate_summary(self, stats, best_expression, total_time):
        """Genera un riepilogo dettagliato dell'esperimento."""
        strategy_usage = stats.get_strategy_usage()
        summary = (
            "\n==================== Experiment Summary ====================\n"
            f"Total Generations: {stats.current_generation}\n"
            f"Best Fitness Achieved: {stats.best_fitness:.4f}\n"
            f"Best Expression: {best_expression}\n"
            f"Duration: {total_time:.2f} seconds\n"
            "\n--- Strategy Usage ---\n"
            f"Selection Strategies: {strategy_usage['selection']}\n"
            f"Crossover Strategies: {strategy_usage['crossover']}\n"
            f"Mutation Strategies: {strategy_usage['mutation']}\n"
            "\n--- Diversity and Complexity ---\n"
            f"Final Diversity: {stats.diversity:.4f}\n"
            f"Final Complexity: {stats.complexity:.4f}\n"
            "============================================================\n"
        )
        # Log summary to console and append to the CSV file
        self.logger.info(summary)
        with open(self.log_file, "a") as csvfile:
            csvfile.write("\n" + summary)
