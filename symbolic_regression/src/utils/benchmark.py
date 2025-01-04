# utils/benchmark.py
import numpy as np
import time
import os
from src.operators.definitions import OperatorSet

def benchmark_operator_costs(operator_set: OperatorSet, array_size: int = int(1e6), iterations: int = 5) -> None:
    """
    Benchmarks the computational cost of all operators across multiple iterations
    and updates their cost attribute with the average time.

    Args:
        operator_set (OperatorSet): The set of operators to benchmark.
        array_size (int): Size of the array for benchmarking.
        iterations (int): Number of times to repeat the benchmark for averaging.
    """
    x = np.random.rand(array_size) * 1000
    y = np.random.rand(array_size) * 1000

    for name, op in operator_set.operators.items():
        total_time = 0.0
        for _ in range(iterations):
            start_time = time.time()
            if op.arity == 1:
                op.function(x)
            elif op.arity == 2:
                op.function(x, y)
            total_time += time.time() - start_time
        average_time = total_time / iterations
        operator_set.operators[name] = op._replace(cost=average_time)  # Update cost


def save_benchmark_results(operator_set: OperatorSet, output_file: str):
    """
    Saves the benchmark results to a file in ascending order of cost, including rank.

    Args:
        operator_set (OperatorSet): The set of operators to save.
        output_file (str): Path to the output file.
    """
    with open(output_file, "w") as file:
        file.write("Operator Benchmark Results (Averaged)\n")
        file.write("=====================================\n")
        for idx, (name, op) in enumerate(sorted(operator_set.operators.items(), key=lambda item: item[1].cost), start=1):
            file.write(f"{idx}) {name}: cost = {op.cost:.6f}s\n")


def run_benchmark(output_dir: str = "reports/", iterations: int = 5):
    """
    Runs the benchmark multiple times and saves the averaged results to a file.

    Args:
        output_dir (str): Directory to save the benchmark results.
        iterations (int): Number of iterations for averaging.
    """
    from src.operators.definitions import operator_set

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Run benchmark
    benchmark_operator_costs(operator_set, iterations=iterations)

    # Save results to a file
    output_file = os.path.join(output_dir, "operator_benchmark_results.txt")
    save_benchmark_results(operator_set, output_file)
    print(f"Benchmark results saved to {output_file}")


if __name__ == "__main__":
    # Esegui il benchmark con 5 iterazioni di default
    run_benchmark(iterations=100)
