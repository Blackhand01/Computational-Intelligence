from symbolic_regression.src.utils.benchmark import run_benchmark
from operators.definitions import operator_set
import sys
print("\n".join(sys.path))

def print_sorted_operators():
    """
    Stampa gli operatori ordinati per costo in ordine crescente, numerandoli.
    """
    sorted_operators = operator_set.get_sorted_operators(by="cost")
    print("Classifica degli operatori per costo crescente:\n")
    for rank, (name, op) in enumerate(sorted_operators.items(), start=1):
        print(f"{rank}. {name.capitalize()} - Cost: {op.cost:.6f} s")

# Esegui il benchmark per aggiornare i costi
run_benchmark()

# Stampa la classifica
print_sorted_operators()
