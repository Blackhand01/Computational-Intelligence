import numpy as np
import time
import os
from datetime import datetime
from src.operators.definitions import OperatorSet

def benchmark_operator_times(operator_set: OperatorSet, array_size: int = int(1e6), iterations: int = 5) -> None:
    """
    Benchmarks the computational time of all operators across multiple iterations
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

def save_benchmark_times(operator_set: OperatorSet, output_file: str):
    """
    Saves the benchmark times to a file in ascending order of time, including rank.

    Args:
        operator_set (OperatorSet): The set of operators to save.
        output_file (str): Path to the output file.
    """
    with open(output_file, "w") as file:
        file.write("Operator Benchmark Times (Averaged)\n")
        file.write("=====================================\n")
        for idx, (name, op) in enumerate(sorted(operator_set.operators.items(), key=lambda item: item[1].cost), start=1):
            file.write(f"{idx}) {name}: time = {op.cost:.6f}s\n")

def calculate_normalized_times(latest_times_file: str, output_dir: str):
    """
    Reads the latest benchmark times, normalizes them, and saves them to a new file.

    Args:
        latest_times_file (str): Path to the latest benchmark times file.
        output_dir (str): Directory to save the normalized times.
    """
    # Parse the benchmark times
    operator_times = {}
    with open(latest_times_file, "r") as file:
        for line in file:
            if "time =" in line:
                parts = line.split(":")
                name = parts[0].strip().split(")")[1].strip()
                time_value = float(parts[1].strip().split("=")[1].strip().rstrip("s"))
                operator_times[name] = time_value

    # Find the maximum time for normalization
    max_time = max(operator_times.values())

    # Calculate normalized times
    normalized_times = {name: time_value / max_time for name, time_value in operator_times.items()}

    # Save normalized times to a new file
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    times_file = os.path.join(output_dir, f"{timestamp}_normalized_times.txt")
    with open(times_file, "w") as file:
        file.write("Normalized Operator Times\n")
        file.write("==========================\n")
        for name, normalized_time in sorted(normalized_times.items(), key=lambda item: item[1]):
            file.write(f"{name}: normalized time = {normalized_time:.4f}\n")
    print(f"Normalized times saved to {times_file}")

def run_benchmark(output_dir: str = "outputs/reports/operators", iterations: int = 5):
    """
    Runs the benchmark multiple times, saves the averaged results, calculates normalized times.

    Args:
        output_dir (str): Directory to save the benchmark results and normalized times.
        iterations (int): Number of iterations for averaging.
    """
    from src.operators.definitions import operator_set

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Run benchmark
    benchmark_operator_times(operator_set, iterations=iterations)

    # Generate output file name with timestamp
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    times_file = os.path.join(output_dir, f"{timestamp}_times.txt")

    # Save results to a file
    save_benchmark_times(operator_set, times_file)

    # Calculate normalized times
    calculate_normalized_times(times_file, output_dir)

if __name__ == "__main__":
    # Esegui il benchmark con 5 iterazioni di default
    run_benchmark(iterations=100)
