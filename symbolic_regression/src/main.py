# File: src/main.py

import numpy as np
from tqdm import tqdm
from src.utils.logging_config import setup_logging
from src.core.genetic_programming import GeneticProgram
from src.core.fitness import FitnessEvaluator
from src.utils.plotting import plot_fitness_history, visualize_formula, plot_prediction_vs_actual, plot_error
from src.preprocessing.data_loader import load_npz_file
from src.preprocessing.splitter import split_dataset

def main():
    # Setup logging
    logger = setup_logging(log_dir="logs", log_level="DEBUG")
    logger.info("Starting symbolic regression process...")

    # Load dataset
    logger.info("Loading dataset...")
    dataset_path = "data/raw/problem_8.npz"  # Update the path if needed
    dataset = load_npz_file(dataset_path, debug=True)

    # # Split dataset into training and test sets
    # logger.info("Splitting dataset into training and test sets...")
    # train_set, test_set = split_dataset(dataset, train_size=0.8, shuffle=True)

    # # Ottieni il numero di variabili dal set di training
    # n_variables = train_set["x"].shape[0]  # In questo caso, 2

    # # Initialize fitness evaluator with training set's y
    # logger.info("Initializing fitness evaluator...")
    # fitness_evaluator = FitnessEvaluator(
    #     y_true=train_set["y"],  # Utilizza i valori target di training
    #     alpha=0.01  # Regularization for parsimony
    # )

    # # Setup Genetic Programming
    # logger.info("Initializing genetic programming...")
    # gp = GeneticProgram(
    #     population_size=50,
    #     max_generations=50,
    #     max_tree_depth=6,
    #     mutation_rate=0.3,   # Initial mutation rate
    #     crossover_rate=0.7,  # Initial crossover rate
    #     fitness_evaluator=fitness_evaluator,
    #     n_variables=n_variables  # Specifica il numero di variabili
    # )

    # # Run the Genetic Programming algorithm
    # logger.info("Starting genetic programming evolution...")
    # best_individual = gp.run(train_set["x"])

    # # Initialize fitness evaluator for test set
    # logger.info("Evaluating the best individual on the test set...")
    # test_fitness_evaluator = FitnessEvaluator(
    #     y_true=test_set["y"],
    #     alpha=0.0  # No penalizzazione durante la valutazione sul test set
    # )
    # test_fitness = test_fitness_evaluator.fitness(best_individual)
    # logger.info(f"Best individual's fitness on the test set: {test_fitness:.6f}")

    # # Save fitness history plot
    # logger.info("Saving fitness history plot...")
    # fitness_history = gp.fitness_scores  # Retrieve fitness scores from the GeneticProgram class
    # plot_fitness_history(fitness_history, file_name="fitness_history.png")

    # # Visualize the formula
    # logger.info("Visualizing the formula...")
    # formula, latex_formula = visualize_formula(best_individual, n_variables=n_variables)
    # logger.info(f"Best individual formula (LaTeX): {latex_formula}")

    # # Plot predictions vs actual values
    # logger.info("Plotting predictions vs actual values...")
    # plot_prediction_vs_actual(best_individual, test_set["x"], test_set["y"], file_name="prediction_vs_actual.png")

    # # Plot error distribution
    # logger.info("Plotting error distribution...")
    # plot_error(best_individual, test_set["x"], test_set["y"], file_name="error_distribution.png")

    # logger.info("Symbolic regression process completed successfully.")

if __name__ == "__main__":
    main()
