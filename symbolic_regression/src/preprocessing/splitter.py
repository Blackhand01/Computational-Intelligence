import numpy as np
from typing import Tuple


def split_dataset(data: dict, train_size: float = 0.8, shuffle: bool = True) -> Tuple[dict, dict]:
    """
    Divide un dataset in set di training e test.

    Args:
        data (dict): Dataset da dividere (con chiavi 'x' e 'y').
        train_size (float): Proporzione del set di training (default 0.8).
        shuffle (bool): Se mescolare i dati prima della divisione (default True).

    Returns:
        Tuple[dict, dict]: Dizionari contenenti il training set e il test set.
    """
    if 'x' not in data or 'y' not in data:
        raise ValueError("Il dataset deve contenere chiavi 'x' e 'y'.")

    x, y = data['x'], data['y']
    indices = np.arange(len(x))
    if shuffle:
        np.random.shuffle(indices)

    split_idx = int(len(x) * train_size)
    train_indices, test_indices = indices[:split_idx], indices[split_idx:]

    train_set = {'x': x[train_indices], 'y': y[train_indices]}
    test_set = {'x': x[test_indices], 'y': y[test_indices]}

    return train_set, test_set
