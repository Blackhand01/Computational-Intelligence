# ==============================================
# Funzione per salvare la formula migliore in un file
# ==============================================
from pathlib import Path
import random
import numpy as np
from tqdm import tqdm

from core.evaluator import Evaluator
from memetic.evolution import GeneticProgramming
from core.statistics import GPStatistics
from gp_config import BLOAT_PENALTY, N_GENERATIONS, SEED
from utility.logger import Logger
from utility.plotting import Plotter


def initialize_experiment(data_file, base_output_dir):
    """
    Inizializza i percorsi, il logger e le directory per un esperimento.

    Args:
        data_file (Path): Percorso al file dei dati.
        base_output_dir (str): Directory di output base.

    Returns:
        dict: Contiene le configurazioni iniziali dell'esperimento.
    """
    random.seed(SEED)
    np.random.seed(SEED)
    # Estrae l'ID del problema dall'ultimo elemento del nome del file
    problem_id = data_file.stem.split('_')[-1]
    problem_dir = Path(base_output_dir) / f"problem_{problem_id}"
    log_dir = problem_dir / "logs"
    plot_dir = problem_dir / "plots"

    log_dir.mkdir(parents=True, exist_ok=True)
    plot_dir.mkdir(parents=True, exist_ok=True)

    logger = Logger(
        log_dir=str(log_dir),
        log_file_prefix=f"p_{problem_id}"
    )

    return {
        "problem_id": problem_id,
        "problem_dir": problem_dir,
        "log_dir": log_dir,
        "plot_dir": plot_dir,
        "logger": logger
    }


def load_data(data_file):
    """
    Carica i dati dal file specificato.

    Args:
        data_file (Path): Percorso al file dei dati.

    Returns:
        tuple: Dati X e Y caricati.
    """
    data = np.load(data_file)
    x, y = data['x'], data['y']
    if x.shape[0] > x.shape[1]:
        x = x.T
    return x, y


def run_genetic_programming(x, y, logger):
    """
    Esegue l'algoritmo di programmazione genetica.

    Args:
        x (np.ndarray): Dati di input.
        y (np.ndarray): Dati di output.
        logger (Logger): Logger per tracciare il processo.

    Returns:
        tuple: L'individuo migliore e le statistiche del GP.
    """
    # Istanzia GPStatistics passando il logger per poter registrare i cambi di strategia
    stats = GPStatistics(logger)
    logger.info("Initializing Genetic Programming.")
    
    gp = GeneticProgramming(
        n_features=x.shape[0],
        generations=N_GENERATIONS,
        bloat_penalty=BLOAT_PENALTY,
        stats=stats
    )

    with tqdm(total=N_GENERATIONS, desc="Genetic Programming", unit="gen") as pbar:
        gp.progress_bar = pbar
        best_individual = gp.run(x, y)

    return best_individual, stats


def save_results(best_individual, stats, output_file, function_name, plot_dir):
    """
    Salva i risultati dell'esperimento.

    Args:
        best_individual (Node): L'individuo migliore.
        stats (GPStatistics): Statistiche del GP.
        output_file (str): File in cui salvare la formula.
        function_name (str): Nome della funzione da aggiornare.
        plot_dir (Path): Directory per i grafici.
    """
    evaluator = Evaluator()
    best_expression = best_individual.tree_to_expression()
    update_formula_in_file(
        formula_str=best_expression,
        file_path=output_file,
        function_name=function_name
    )

    # Crea e salva tutti i grafici tramite il Plotter
    plotter = Plotter(plot_dir=str(plot_dir), plot_dir_prefix=function_name, history=stats.history)
    plotter.save_all_plots(strategy_usage=stats.strategy_usage)

def update_formula_in_file(formula_str, file_path, function_name):
    """
    Sovrascrive completamente la funzione `function_name` in `file_path`
    con `return formula_str`, assicurandosi che sia nel formato NumPy corretto.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    new_lines = []
    inside_function = False
    for line in lines:
        if line.strip().startswith(f"def {function_name}"):
            inside_function = True
            new_lines.append(f"def {function_name}(x: np.ndarray) -> np.ndarray:\n")
            new_lines.append(f"    return {formula_str}\n")
            continue
        if inside_function:
            if line.strip() == "" or line.strip().startswith("def "):
                inside_function = False
        if not inside_function:
            new_lines.append(line)

    with open(file_path, 'w') as file:
        file.writelines(new_lines)

    print(f"Formula aggiornata in {file_path} nella funzione {function_name}.")

