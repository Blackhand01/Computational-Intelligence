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
import time

def main():
    data_dir = './data/'
    output_file = './src/s333971.py'

    # Trova tutti i file .npz nella directory
    data_files = sorted(Path(data_dir).glob('*.npz'))

    if not data_files:
        print("No data files found in the directory.")
        return

    experiment_successful = True  # Per monitorare il completamento globale

    for data_file in data_files:
        try:
            # Estrarre l'ID del problema e configurare il logger specifico
            problem_id = data_file.stem.split('_')[-1]
            timestamp = datetime.now().strftime("%Y%m%d")
            logger = Logger(
                log_dir=f"./output/problem_{problem_id}/logs/",
                log_file_prefix=f"{timestamp}_problem_{problem_id}"
            )

            logger.info(f"Processing Problem {problem_id}")

            # Caricamento dati
            data = np.load(data_file)
            x, y = data['x'], data['y']

            if x.shape[0] > x.shape[1]:
                x = x.T

            # Inizializzare le statistiche
            stats = GPStatistics()

            # Esecuzione della programmazione genetica con barra di progresso
            logger.info("Initializing Genetic Programming.")
            gp = GeneticProgramming(
                n_features=x.shape[0],
                generations=N_GENERATIONS,
                bloat_penalty=BLOAT_PENALTY,
                logger=logger,
                stats=stats,
                progress_bar=None  # Sarà passato dopo
            )

            start_time = time.time()

            with tqdm(total=N_GENERATIONS, desc=f"Problem {problem_id}", unit="gen") as pbar:
                gp.progress_bar = pbar  # Passa la barra di progresso
                best_individual = gp.run(x, y)

            end_time = time.time()
            total_time = end_time - start_time

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

            # Generazione del riepilogo
            logger.generate_summary(stats, best_expression, total_time)

        except Exception as e:
            experiment_successful = False  # Segna l'esperimento come non completato
            error_message = f"Error processing Problem {problem_id}: {str(e)}"
            logger.info(error_message)
            print(error_message)

    if experiment_successful:
        print("Experiment completed successfully.")
    else:
        print("Experiment completed with errors. Check logs for details.")

if __name__ == "__main__":
    main()
