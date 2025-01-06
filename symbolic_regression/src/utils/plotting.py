import matplotlib.pyplot as plt
import os
from sympy import symbols, lambdify, latex
import numpy as np
from typing import Tuple

def visualize_formula(tree, n_variables: int = 1) -> Tuple[str, str]:
    """
    Visualizza la formula rappresentata da un oggetto Tree.

    Args:
        tree (Tree): L'albero sintattico rappresentante la formula.
        n_variables (int): Numero di variabili utilizzate.

    Returns:
        Tuple[str, str]: Espressione SymPy e rappresentazione LaTeX della formula.
    """
    var_symbols = symbols(f'x0:{n_variables}')  # Crea simboli x0, x1, ..., xn
    sympy_expr = tree.root.to_sympy(var_symbols)
    latex_formula = latex(sympy_expr)
    print(f"Formula (LaTeX): {latex_formula}")
    return str(sympy_expr), latex_formula

def plot_fitness_history(fitness_history, output_dir="outputs/plots", file_name="fitness_history.png"):
    """
    Plots the fitness history over generations.

    Args:
        fitness_history (list): Fitness values for each generation.
        output_dir (str): Directory to save the plot.
        file_name (str): Name of the output plot file.
    """
    os.makedirs(output_dir, exist_ok=True)
    plt.figure(figsize=(10, 6))
    plt.plot(fitness_history, marker='o')
    plt.title("Fitness History")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.grid(True)
    output_path = os.path.join(output_dir, file_name)
    plt.savefig(output_path)
    plt.close()
    print(f"Fitness history plot saved to {output_path}")

def plot_error(tree, x, y, file_name="error_distribution.png"):
    """
    Plots the error distribution between predicted and actual values.

    Args:
        tree (Tree): Syntax tree representing the formula.
        x (np.ndarray): Input data.
        y (np.ndarray): True output values.
        file_name (str): File name for saving the plot.
    """
    y_pred = tree.root.evaluate(x)
    error = np.abs(y - y_pred)

    plt.figure(figsize=(10, 6))
    plt.hist(error, bins=50, alpha=0.7, color="orange", label="Error distribution")
    plt.title("Error Distribution")
    plt.xlabel("Absolute Error")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"outputs/plots/{file_name}")
    plt.close()
    print(f"Error distribution plot saved to outputs/plots/{file_name}")

def plot_prediction_vs_actual(tree, x, y, file_name="prediction_vs_actual.png"):
    """
    Plots the predicted vs actual values.

    Args:
        tree (Tree): Syntax tree representing the formula.
        x (np.ndarray): Input data.
        y (np.ndarray): True output values.
        file_name (str): File name for saving the plot.
    """
    # Calculate predictions
    y_pred = tree.root.evaluate(x)

    # Plot actual vs predicted
    plt.figure(figsize=(10, 6))
    plt.scatter(y, y_pred, alpha=0.6, label='Predicted vs Actual')
    plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', label='Perfect fit')
    plt.title("Prediction vs Actual")
    plt.xlabel("Actual values")
    plt.ylabel("Predicted values")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"outputs/plots/{file_name}")
    plt.close()
    print(f"Prediction vs Actual plot saved to outputs/plots/{file_name}")

