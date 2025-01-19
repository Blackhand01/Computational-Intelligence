from datetime import datetime
import numpy as np
from pathlib import Path
from tqdm import tqdm
from gp.evolution import GeneticProgramming
from tree import Node
from evaluator import Evaluator
from gp_config import BLOAT_PENALTY, N_GENERATIONS
from utils import update_formula_in_file
from logger import Logger
from gp.statistics import GPStatistics
from plotting import Plotter
import time

def main():
    data_dir = './data/'
    output_file = './src/s333971.py'
    base_output_dir = './output/'

    # Trova tutti i file .npz nella directory
    data_files = sorted(Path(data_dir).glob('*.npz'))

    if not data_files:
        print("No data files found in the directory.")
        return

    for data_file in data_files:
        # Configurazioni iniziali per l'esperimento
        experiment_successful = True
        start_time = datetime.now()
        reason = "Max generations reached"
        best_expression = None

        try:
            # Estrarre l'ID del problema e configurare i percorsi
            problem_id = data_file.stem.split('_')[-1]
            problem_dir = Path(base_output_dir) / f"problem_{problem_id}"
            log_dir = problem_dir / "logs"
            plot_dir = problem_dir / "plots"

            log_dir.mkdir(parents=True, exist_ok=True)
            plot_dir.mkdir(parents=True, exist_ok=True)

            # Configura il logger
            logger = Logger(
                log_dir=str(log_dir),
                log_file_prefix=f"problem_{problem_id}"
            )

            logger.info(f"Processing Problem {problem_id}")

            # Caricamento dati
            data = np.load(data_file)
            x, y = data['x'], data['y']

            if x.shape[0] > x.shape[1]:
                x = x.T

            # Inizializzare le statistiche
            stats = GPStatistics()

            # Esecuzione della programmazione genetica
            logger.info("Initializing Genetic Programming.")
            gp = GeneticProgramming(
                n_features=x.shape[0],
                generations=N_GENERATIONS,
                bloat_penalty=BLOAT_PENALTY,
                logger=logger,
                stats=stats
            )

            with tqdm(total=N_GENERATIONS, desc=f"Problem {problem_id}", unit="gen") as pbar:
                gp.progress_bar = pbar
                best_individual = gp.run(x, y)

            end_time = datetime.now()
            total_time = (end_time - start_time).total_seconds()

            # Calcolo fitness e formula finale
            evaluator = Evaluator()
            best_expression = best_individual.tree_to_expression()
            best_fitness = evaluator.fitness_function(best_individual, x, y, BLOAT_PENALTY)

            logger.info(f"Problem {problem_id} - Best Fitness: {best_fitness:.4f} - Formula: {best_expression}")
            print(f"Problem {problem_id} processed. Best Fitness: {best_fitness:.4f}")

            # Salvataggio della formula nel file di output
            update_formula_in_file(
                formula_str=best_expression,
                file_path=output_file,
                function_name=f'f{problem_id}'
            )

            # Generazione dei grafici
            plotter = Plotter(plot_dir=str(plot_dir), plot_dir_prefix=f"problem_{problem_id}", history=stats.history)
            plotter.save_all_plots(
                strategy_usage=stats.strategy_usage
            )

        except Exception as e:
            experiment_successful = False
            reason = f"Error: {str(e)}"
            logger.info(f"Error processing Problem {problem_id}: {reason}")
            print(f"Error processing Problem {problem_id}: {reason}")

        finally:
            # Generazione del riepilogo
            end_time = datetime.now()
            total_time = (end_time - start_time).total_seconds()
            logger.generate_summary(
                stats=stats,
                best_expression=best_expression if best_expression else "N/A",
                total_time=total_time,
                start_time=start_time,
                end_time=end_time,
                reason=reason,
                success=experiment_successful
            )

    # Messaggio finale
    print("All experiments completed.")


if __name__ == "__main__":
    main()
