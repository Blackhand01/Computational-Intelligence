import matplotlib.pyplot as plt
import numpy as np

def plot_results(model, x, y, output_dir):
    """Genera grafici di output"""
    y_pred = model(x=x.T)
    plt.figure()
    plt.scatter(y, y_pred, alpha=0.6, label="Predicted vs Actual")
    plt.xlabel("Actual")
    plt.ylabel("Predicted")
    plt.legend()
    plt.savefig(f"{output_dir}/predicted_vs_actual.png")
    plt.close()
