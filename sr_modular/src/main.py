import numpy as np
import random
from pathlib import Path
from gp import GeneticProgramming
from tree import generate_random_tree, tree_to_expression
from evaluator import Evaluator
from gp_config import POP_SIZE, MAX_DEPTH, N_GENERATIONS, BLOAT_PENALTY

# ==============================================
#         FUNZIONE PRINCIPALE DEL PROGETTO
# ==============================================
def main():
    data_dir = './data/raw/'  # Directory dei file dati
    output_dir = './output/'  # Directory di output

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

        # Normalizzazione opzionale
        x = (x - np.mean(x, axis=1, keepdims=True)) / (np.std(x, axis=1, keepdims=True) + 1e-8)
        y = (y - np.mean(y)) / (np.std(y) + 1e-8)

        # Inizializzazione popolazione
        population = [
            generate_random_tree(MAX_DEPTH, x.shape[0], grow=random.random() > 0.5)
            for _ in range(POP_SIZE)
        ]

        best_individual = None
        best_fitness = float('inf')

        # Evoluzione
        for generation in range(N_GENERATIONS):
            print(f"Generazione {generation + 1}/{N_GENERATIONS}")
            population = GeneticProgramming.evolve_population(population, x, y, x.shape[0], generation)

            # Miglior individuo della generazione
            evaluator = Evaluator()
            current_best, current_fitness = evaluator.get_best_individual(population, x, y, BLOAT_PENALTY)

            if current_fitness < best_fitness:
                best_fitness = current_fitness
                best_individual = current_best

            print(f"Fitness migliore della generazione: {current_fitness:.4f}")

        # Formula finale
        best_expression = tree_to_expression(best_individual)
        print(f"\n=== Risultati per Problem {problem_id} ===")
        print(f"Miglior formula trovata: {best_expression}")
        print(f"Fitness finale: {best_fitness:.4f}")

if __name__ == "__main__":
    main()
