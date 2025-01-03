import numpy as np

def load_data(file_path):
    """Carica i dati dal file .npz"""
    data = np.load(file_path)
    x, y = data['x'], data['y']
    train_size = int(0.8 * x.shape[1])
    return x[:, :train_size], y[:train_size], x[:, train_size:], y[train_size:]
