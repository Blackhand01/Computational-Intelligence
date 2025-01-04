# utils/benchmark.py
import numpy as np
import time
import os
from src.operators.definitions import OperatorSet


def benchmark_operator_costs(operator_set: OperatorSet, array_size: int = int(1e6)) -> None:
    """
    Benchmarks the computational cost of all operators and updates their cost attribute.

    Args:
        operator_set (OperatorSet): The set of operators to benchmark.
        array_size (int): Size of the array for benchmarking.
    """
    x = np.random.rand(array_size) * 1000
    y = np.random.rand(array_size) * 1000

    for name, op in operator_set.operators.items():
        start_time = time.time()
        if op.arity == 1:
            op.function(x)
        elif op.arity == 2:
            op.function(x, y)
        elapsed_time = time.time() - start_time
        operator_set.operators[name] = op._replace(cost=elapsed_time)  # Update cost


def save_benchmark_results(operator_set: OperatorSet, output_file: str):
    """
    Saves the benchmark results to a file in descending order of cost.

    Args:
        operator_set (OperatorSet): The set of operators to save.
        output_file (str): Path to the output file.
    """
    with open(output_file, "w") as file:
        file.write("Operator Benchmark Results\n")
        file.write("===========================\n")
        for name, op in sorted(operator_set.operators.items(), key=lambda item: item[1].cost, reverse=True):
            file.write(f"{name}: cost = {op.cost:.6f}s\n")


def run_benchmark(output_dir: str = "reports/"):
    """
    Runs the benchmark and saves the results to a file in the output directory.

    Args:
        output_dir (str): Directory to save the benchmark results.
    """
    from src.operators.definitions import operator_set

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Run benchmark
    benchmark_operator_costs(operator_set)

    # Save results to a file
    output_file = os.path.join(output_dir, "operator_benchmark_results.txt")
    save_benchmark_results(operator_set, output_file)
    print(f"Benchmark results saved to {output_file}")


