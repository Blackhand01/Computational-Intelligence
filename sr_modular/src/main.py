import numpy as np
from pathlib import Path
from gp.evolution import GeneticProgramming
from tree import tree_to_expression
from evaluator import Evaluator
from gp_config import BLOAT_PENALTY, N_GENERATIONS
from utils import update_formula_in_file

# ==============================================
#         FUNZIONE PRINCIPALE DEL PROGETTO
# ==============================================
def main():
    data_dir = './data/raw/'  # Directory dei file dati
    output_file = './src/s333971.py'  # File di output per la formula

    # Trova tutti i file .npz nella directory data_dir
    data_files = sorted(Path(data_dir).glob('*.npz'))

    if not data_files:
        print("No data files found in the directory.")
        return

    for data_file in data_files:
        # Estrai l'ID del problema dal nome del file
        problem_id = data_file.stem.split('_')[-1]
        print(f"\n=== Caricamento dati per Problem {problem_id} ===")

        # Caricamento dati
        data = np.load(data_file)
        x, y = data['x'], data['y']

        # Se necessario, trasponi x
        if x.shape[0] > x.shape[1]:
            x = x.T

        # Esegue la programmazione genetica
        gp = GeneticProgramming()
        best_individual = gp.run_gp(x, y, n_features=x.shape[0], generations=N_GENERATIONS, bloat_penalty=BLOAT_PENALTY)

        # Calcolo della fitness migliore
        evaluator = Evaluator()
        best_fitness = evaluator.fitness_function(best_individual, x, y, BLOAT_PENALTY)

        # Formula finale
        best_expression = tree_to_expression(best_individual)
        print(f"\n=== Risultati per Problem {problem_id} ===")
        print(f"Miglior formula trovata: {best_expression}")
        print(f"Fitness finale: {best_fitness:.4f}")

        # Salva la formula nel file
        update_formula_in_file(
            formula_str=best_expression,
            file_path=output_file,
            function_name=f'f{problem_id}'
        )

if __name__ == "__main__":
    main()
