import os
from data_loader import load_data
from gxgp_wrapper import train_model, evaluate_model, draw_model
from evaluate import calculate_mse
from generate_graphs import plot_results
from report_generator import update_report
import logging

# Configurazione logging
logging.basicConfig(filename='results/logs/execution.log', level=logging.INFO)

def main():
    # 1. Caricamento dei dati
    data_file = "data/problem_0.npz"
    x_train, y_train, x_test, y_test = load_data(data_file)

    # 2. Addestramento del modello
    model = train_model(x_train, y_train)

    # 3. Valutazione del modello
    mse_train = calculate_mse(model, x_train, y_train)
    mse_test = calculate_mse(model, x_test, y_test)
    logging.info(f"MSE Training: {mse_train}, MSE Test: {mse_test}")

    # 4. Generazione dei grafici
    plot_results(model, x_test, y_test, output_dir="results/graphs")

    # 5. Disegno dell'albero
    draw_model(model, output_file="results/graphs/model_structure.png")

    # 6. Aggiornamento del report
    update_report(mse_train, mse_test, "results/graphs/")

if __name__ == "__main__":
    main()
