import numpy as np
import matplotlib.pyplot as plt
import os
# import plotly.graph_objects as go

# def plot_3d_interactive(data: dict):
#     """
#     Plots an interactive 3D surface for a dataset with two features and one target.

#     Args:
#         dataset_path (str): Path to the .npz dataset file.
#     """
#     # Load the dataset
#     x = data["x"]
#     y = data["y"]

#     if x.shape[0] != 2:
#         raise ValueError("This visualization only supports datasets with exactly two features.")

#     # Extract features
#     x1 = x[0, :]
#     x2 = x[1, :]

#     # Create a mesh grid for x1 and x2
#     grid_size = 50
#     x1_grid, x2_grid = np.meshgrid(
#         np.linspace(x1.min(), x1.max(), grid_size),
#         np.linspace(x2.min(), x2.max(), grid_size)
#     )

#     # Interpolate y values over the mesh grid
#     # Using a simple nearest-neighbor interpolation for the purpose of visualization
#     from scipy.interpolate import griddata
#     y_grid = griddata(
#         points=(x1, x2), 
#         values=y, 
#         xi=(x1_grid, x2_grid), 
#         method="linear"
#     )

#     # Create a 3D surface plot
#     fig = go.Figure(
#         data=[go.Surface(
#             z=y_grid, 
#             x=x1_grid, 
#             y=x2_grid, 
#             colorscale="Viridis", 
#             showscale=True
#         )]
#     )

#     # Add axis labels
#     fig.update_layout(
#         title="3D Surface Plot of Features and Target",
#         scene=dict(
#             xaxis_title="Feature 1",
#             yaxis_title="Feature 2",
#             zaxis_title="Target (y)"
#         )
#     )

#     # Show the plot
#     fig.show()

def dataset_statistics(data: dict):
    """
    Stampa statistiche base per ogni variabile nel dataset.

    Args:
        data (dict): Dizionario contenente le variabili del dataset.
    """
    if "x" not in data or "y" not in data:
        raise ValueError("Dataset must contain 'x' and 'y' keys.")

    x, y = data["x"], data["y"]

    print("\nDetailed Statistics:")
    print("-" * 50)
    print(f"Input (x):")
    print(f"  Number of features: {x.shape[0]}")
    print(f"  Number of samples: {x.shape[1]}")
    for i in range(x.shape[0]):
        print(f"    Feature {i + 1}:")
        print(f"      Mean: {x[i].mean():.4f}")
        print(f"      Std Dev: {x[i].std():.4f}")
        print(f"      Min: {x[i].min():.4f}")
        print(f"      Max: {x[i].max():.4f}")

    print("\nTarget (y):")
    print(f"  Mean: {y.mean():.4f}")
    print(f"  Std Dev: {y.std():.4f}")
    print(f"  Min: {y.min():.4f}")
    print(f"  Max: {y.max():.4f}")
    print("-" * 50)


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
    x, y = data["x"], data["y"]
    for i in range(x.shape[0]):
        plt.hist(
            x[i, :],
            bins=50,
            alpha=0.5,
            label=f"Feature {i + 1} ({x.shape[1]} samples)"
        )
    plt.hist(
        y,
        bins=50,
        alpha=0.5,
        label=f"Target (y) ({len(y)} samples)",
        color="orange"
    )

    plt.title("Distributions of Features and Target")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.legend(loc="best")
    output_path = os.path.join(output_dir, file_name)
    plt.savefig(output_path)
    plt.close()
    print(f"Distribution plot saved to {output_path}")
