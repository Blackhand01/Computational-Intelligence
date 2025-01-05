import numpy as np
import matplotlib.pyplot as plt
import os

def load_npz_file(file_path: str):
    """
    Carica un file .npz e restituisce i dati in esso contenuti.

    Args:
        file_path (str): Percorso al file .npz.

    Returns:
        dict: Dizionario contenente i dati caricati.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    data = np.load(file_path)
    return {key: data[key] for key in data}

def dataset_statistics(data: dict):
    """
    Stampa statistiche base (media, deviazione standard, minimo, massimo) per ogni variabile nel dataset.

    Args:
        data (dict): Dizionario contenente le variabili del dataset.
    """
    print("\nDataset Statistics:")
    for key, array in data.items():
        print(f"Variable: {key}")
        print(f"  Shape: {array.shape}")
        print(f"  Mean: {np.mean(array):.4f}")
        print(f"  Std Dev: {np.std(array):.4f}")
        print(f"  Min: {np.min(array):.4f}")
        print(f"  Max: {np.max(array):.4f}")

def plot_distribution(data: dict, output_dir: str = "outputs/plots", file_name: str = "distribution.png"):
    """
    Genera un grafico della distribuzione delle variabili nel dataset.

    Args:
        data (dict): Dizionario contenente le variabili del dataset.
        output_dir (str): Directory dove salvare il grafico.
        file_name (str): Nome del file del grafico salvato.
    """
    os.makedirs(output_dir, exist_ok=True)
    plt.figure(figsize=(10, 6))

    for key, array in data.items():
        plt.hist(array.flatten(), bins=50, alpha=0.5, label=f"{key} (shape: {array.shape})")

    plt.title("Variable Distributions")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.legend()
    output_path = os.path.join(output_dir, file_name)
    plt.savefig(output_path)
    plt.close()
    print(f"Distribution plot saved to {output_path}")

def analyze_dataset(file_path: str, output_dir: str = "outputs/plots"):
    """
    Analizza un dataset .npz, stampa statistiche e genera un grafico della distribuzione.

    Args:
        file_path (str): Percorso al file .npz.
        output_dir (str): Directory dove salvare il grafico.
    """
    print(f"Analyzing dataset: {file_path}")
    data = load_npz_file(file_path)
    dataset_statistics(data)
    plot_distribution(data, output_dir=output_dir, file_name=f"{os.path.basename(file_path).replace('.npz', '_distribution.png')}")

analyze_dataset("data/raw/problem_0.npz", output_dir="outputs/plots")
