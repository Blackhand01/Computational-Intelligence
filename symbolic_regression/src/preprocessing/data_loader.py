import numpy as np
import os
from src.preprocessing.data_statistics import dataset_statistics, plot_distribution


def load_npz_file(file_path: str, output_dir: str = "outputs/plots", debug: bool = False) -> dict:
    """
    Carica un file .npz, valida i dati e presenta statistiche utili e distribuzioni.

    Args:
        file_path (str): Percorso al file .npz.
        output_dir (str): Directory per salvare i grafici delle distribuzioni.
        debug (bool): Se True, stampa messaggi di debug.

    Returns:
        dict: Dizionario contenente i dati caricati.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    data = np.load(file_path)
    x, y = data["x"], data["y"]

    # Validazione: assicura che il numero di campioni corrisponda
    if x.shape[1] != len(y):
        raise ValueError(
            f"Inconsistent data: 'x' has {x.shape[1]} samples but 'y' has {len(y)} targets."
        )

    dataset = {"x": x, "y": y}

    # plot_3d_interactive(dataset)

    # Genera statistiche e distribuzioni
    if debug:
        print("\nDataset Information:")
        print(f"  Number of features: {x.shape[0]}")
        print(f"  Number of samples: {x.shape[1]}")
        print(f"  Target shape: {y.shape}")
        print(f"  Target mean: {y.mean():.4f}, Target std: {y.std():.4f}")
        dataset_statistics(dataset)
        plot_distribution(
            dataset,
            output_dir=output_dir,
            file_name=f"{os.path.basename(file_path).replace('.npz', '_distribution.png')}"
        )

    return dataset


def save_npz_file(data: dict, file_path: str) -> None:
    """
    Salva un dataset in formato .npz.

    Args:
        data (dict): Dizionario contenente i dati da salvare.
        file_path (str): Percorso in cui salvare il file .npz.
    """
    if "x" not in data or "y" not in data:
        raise ValueError("Dataset must contain 'x' and 'y' keys.")

    x, y = data["x"], data["y"]
    if not isinstance(x, np.ndarray) or not isinstance(y, np.ndarray):
        raise TypeError("Both 'x' and 'y' must be NumPy arrays.")

    if x.shape[1] != len(y):
        raise ValueError(
            f"Inconsistent data: 'x' has {x.shape[1]} samples, "
            f"but 'y' has {len(y)} samples."
        )

    np.savez(file_path, **data)
    print(f"Dataset saved in {file_path}")
