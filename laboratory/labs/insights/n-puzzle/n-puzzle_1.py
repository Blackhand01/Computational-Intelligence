from collections import namedtuple, deque
from heapq import heappush, heappop
from random import choice
from tqdm.auto import tqdm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from functools import lru_cache
import time  # Import for measuring execution time
import os  # For handling directories

# ------------------------------
# 1. Import Libraries and Define Constants
# ------------------------------

# Puzzle dimensions to test (modifiable)
puzzle_sizes = [3]  # Added 4 for 4x4 puzzle

# Number of randomization steps to ensure a well-shuffled puzzle
RANDOMIZE_STEPS = 1000  # You may increase this for larger puzzles

# Named tuple to represent an action (swap positions)
Action = namedtuple('Action', ['pos1', 'pos2'])

# ------------------------------
# 2. Puzzle Utility Functions
# ------------------------------

def available_actions(state: tuple, puzzle_dim: int) -> list:
    """
    Returns all valid actions for moving the empty tile (0).
    """
    zero_index = state.index(0)
    x, y = divmod(zero_index, puzzle_dim)
    actions = []
    if x > 0:
        actions.append(Action(zero_index, zero_index - puzzle_dim))  # Move up
    if x < puzzle_dim - 1:
        actions.append(Action(zero_index, zero_index + puzzle_dim))  # Move down
    if y > 0:
        actions.append(Action(zero_index, zero_index - 1))  # Move left
    if y < puzzle_dim - 1:
        actions.append(Action(zero_index, zero_index + 1))  # Move right
    return actions


def do_action(state: tuple, action_move: 'Action') -> tuple:
    """
    Executes a given action on the state.
    """
    lst = list(state)
    lst[action_move.pos1], lst[action_move.pos2] = lst[action_move.pos2], lst[action_move.pos1]
    return tuple(lst)


@lru_cache(maxsize=None)
def manhattan_distance(state: tuple, puzzle_dim: int) -> int:
    """
    Calculates the Manhattan distance for the given state.
    """
    distance = 0
    for index, value in enumerate(state):
        if value != 0:
            target_index = value - 1
            current_x, current_y = divmod(index, puzzle_dim)
            target_x, target_y = divmod(target_index, puzzle_dim)
            distance += abs(current_x - target_x) + abs(current_y - target_y)
    return distance


@lru_cache(maxsize=None)
def linear_conflict(state: tuple, puzzle_dim: int) -> int:
    """
    Calculates the Linear Conflict heuristic for the given state.
    """
    conflict = 0
    # Row conflicts
    for row in range(puzzle_dim):
        max_seen = -1
        for col in range(puzzle_dim):
            index = row * puzzle_dim + col
            value = state[index]
            if value != 0 and (value - 1) // puzzle_dim == row:
                if value > max_seen:
                    max_seen = value
                else:
                    conflict += 2
    # Column conflicts
    for col in range(puzzle_dim):
        max_seen = -1
        for row in range(puzzle_dim):
            index = row * puzzle_dim + col
            value = state[index]
            if value != 0 and (value - 1) % puzzle_dim == col:
                if value > max_seen:
                    max_seen = value
                else:
                    conflict += 2
    return conflict


def total_heuristic(state: tuple, puzzle_dim: int) -> int:
    """
    Combines Manhattan Distance and Linear Conflict for the A* heuristic.
    """
    return manhattan_distance(state, puzzle_dim) + linear_conflict(state, puzzle_dim)


def reconstruct_path(came_from: dict, current: tuple) -> list:
    """
    Reconstructs the path from the initial state to the current state.
    """
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def is_solvable(state: tuple, puzzle_dim: int) -> bool:
    """
    Determines if a given puzzle state is solvable.
    """
    inversions = 0
    flat_state = [num for num in state if num != 0]
    for i in range(len(flat_state)):
        for j in range(i + 1, len(flat_state)):
            if flat_state[i] > flat_state[j]:
                inversions += 1
    if puzzle_dim % 2 != 0:
        return inversions % 2 == 0
    else:
        zero_row = state.index(0) // puzzle_dim
        return (inversions + zero_row) % 2 == 0


def randomize_puzzle(puzzle_dim: int, randomize_steps: int = RANDOMIZE_STEPS) -> tuple:
    """
    Generate a randomized puzzle state by performing random moves.
    """
    # Create the goal state
    state = tuple([i for i in range(1, puzzle_dim**2)] + [0])
    for _ in tqdm(range(randomize_steps), desc='Randomizing', unit='steps'):
        actions = available_actions(state, puzzle_dim)
        state = do_action(state, choice(actions))
    # Ensure the state is solvable
    if not is_solvable(state, puzzle_dim):
        # Swap two tiles (not including the empty tile) to make it solvable
        lst = list(state)
        # Find two tiles that are not zero to swap
        non_zero_indices = [i for i, val in enumerate(lst) if val != 0]
        if len(non_zero_indices) >= 2:
            i1, i2 = non_zero_indices[0], non_zero_indices[1]
            lst[i1], lst[i2] = lst[i2], lst[i1]
            state = tuple(lst)
    return state

# ------------------------------
# 3. Algorithm Implementations
# ------------------------------

def bfs(state: tuple, puzzle_dim: int, max_depth: int = 50):
    """
    Solve the puzzle using the Breadth-First Search (BFS) algorithm with a depth limit.
    """
    goal = tuple([i for i in range(1, puzzle_dim**2)] + [0])

    queue = deque([(state, 0)])  # (state, depth)
    visited = set([state])
    came_from = {}
    nodes_evaluated = 0

    pbar = tqdm(desc="BFS Progress", unit="nodes", dynamic_ncols=True)

    while queue:
        current, depth = queue.popleft()
        nodes_evaluated += 1
        pbar.update(1)

        if current == goal:
            pbar.set_description("BFS Completed")
            pbar.close()
            return reconstruct_path(came_from, current), nodes_evaluated

        if depth >= max_depth:
            pbar.set_description(f"BFS Max depth {max_depth} reached")
            pbar.close()
            return None, nodes_evaluated

        for action_move in available_actions(current, puzzle_dim):
            neighbor = do_action(current, action_move)
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, depth + 1))
                came_from[neighbor] = current

    pbar.set_description("BFS Terminated")
    pbar.close()
    return None, nodes_evaluated  # No solution found


def dls(state: tuple, puzzle_dim: int, limit=50):
    """
    Solve the puzzle using Depth-Limited Search (DLS).
    """
    goal = tuple([i for i in range(1, puzzle_dim**2)] + [0])
    nodes_evaluated = 0

    def recursive_dls(current, depth, path):
        nonlocal nodes_evaluated
        nodes_evaluated += 1

        if current == goal:
            return path

        if depth == 0:
            return None

        for action_move in available_actions(current, puzzle_dim):
            neighbor = do_action(current, action_move)
            if neighbor not in path:
                result = recursive_dls(neighbor, depth - 1, path + [neighbor])
                if result:
                    return result

        return None

    result = recursive_dls(state, limit, [state])
    return result, nodes_evaluated


def iterative_deepening_dfs(state: tuple, puzzle_dim: int, max_depth: int = 50):
    """
    Solve the puzzle using Iterative Deepening Depth-First Search (IDDFS).
    """
    nodes_evaluated = 0

    for depth in range(1, max_depth + 1):
        result, evaluated = dls(state, puzzle_dim, depth)
        nodes_evaluated += evaluated

        if result:
            return result, nodes_evaluated

    return None, nodes_evaluated


def a_star(state: tuple, puzzle_dim: int):
    """
    Solve the puzzle using the A* search algorithm with optimized heuristic and time estimation.
    """
    goal = tuple([i for i in range(1, puzzle_dim**2)] + [0])

    open_set = []
    heappush(open_set, (total_heuristic(state, puzzle_dim), 0, state))  # (f-score, g(n), state)
    came_from = {}
    g_score = {state: 0}
    f_score = {state: total_heuristic(state, puzzle_dim)}
    nodes_evaluated = 0
    closed_set = set()

    pbar = tqdm(desc="A* Progress", unit="nodes", dynamic_ncols=True)
    start_time = time.time()

    last_time = start_time
    last_nodes_evaluated = 0

    while open_set:
        _, current_g, current = heappop(open_set)
        nodes_evaluated += 1
        pbar.update(1)

        if current == goal:
            total_time = time.time() - start_time
            pbar.set_description("A* Completed")
            pbar.close()
            return reconstruct_path(came_from, current), nodes_evaluated

        if current in closed_set:
            continue
        closed_set.add(current)

        # Periodically estimate remaining time
        if nodes_evaluated % 1000 == 0:
            current_time = time.time()
            elapsed_time = current_time - start_time
            nodes_since_last = nodes_evaluated - last_nodes_evaluated
            time_since_last = current_time - last_time
            nodes_per_second = nodes_since_last / time_since_last if time_since_last > 0 else 0
            estimated_total_nodes = (len(open_set) + nodes_evaluated)
            estimated_remaining_nodes = estimated_total_nodes - nodes_evaluated
            estimated_time_remaining = estimated_remaining_nodes / nodes_per_second if nodes_per_second > 0 else float('inf')
            # Optional: Print or log the estimated time remaining
            # print(f"Nodes evaluated: {nodes_evaluated}, Estimated time remaining: {estimated_time_remaining/60:.2f} minutes")
            last_time = current_time
            last_nodes_evaluated = nodes_evaluated

        for action_move in available_actions(current, puzzle_dim):
            neighbor = do_action(current, action_move)
            tentative_g = current_g + 1

            if neighbor in closed_set:
                continue

            tentative_f = tentative_g + total_heuristic(neighbor, puzzle_dim)

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_f
                heappush(open_set, (tentative_f, tentative_g, neighbor))

    total_time = time.time() - start_time
    pbar.set_description("A* Terminated")
    pbar.close()
    return None, nodes_evaluated  # No solution found


def ida_star(state: tuple, puzzle_dim: int):
    """
    Solve the puzzle using Iterative Deepening A* (IDA*) with time estimation.
    """
    goal = tuple([i for i in range(1, puzzle_dim**2)] + [0])
    nodes_evaluated = 0

    start_time = time.time()
    pbar = tqdm(desc="IDA* Progress", unit="nodes", dynamic_ncols=True)

    threshold = total_heuristic(state, puzzle_dim)
    path = [state]

    max_threshold = 80  # You can adjust this limit

    while True:
        min_threshold = float('inf')
        stack = [(state, 0, total_heuristic(state, puzzle_dim), [state])]
        visited = set()
        iteration_start_time = time.time()
        nodes_in_iteration = 0

        while stack:
            current, g, f, current_path = stack.pop()
            nodes_evaluated += 1
            nodes_in_iteration += 1
            pbar.update(1)

            if current == goal:
                total_time = time.time() - start_time
                pbar.set_description("IDA* Completed")
                pbar.close()
                return current_path, nodes_evaluated

            if f > threshold:
                if f < min_threshold:
                    min_threshold = f
                continue

            visited.add(current)

            for action_move in available_actions(current, puzzle_dim):
                neighbor = do_action(current, action_move)
                if neighbor in visited:
                    continue
                g_neighbor = g + 1
                f_neighbor = g_neighbor + total_heuristic(neighbor, puzzle_dim)
                stack.append((neighbor, g_neighbor, f_neighbor, current_path + [neighbor]))

        # Estimate remaining time
        iteration_time = time.time() - iteration_start_time
        if nodes_in_iteration > 0:
            nodes_per_second = nodes_in_iteration / iteration_time
            estimated_nodes_remaining = (min_threshold - threshold) * nodes_per_second
            estimated_time_remaining = estimated_nodes_remaining / nodes_per_second if nodes_per_second > 0 else float('inf')
            total_elapsed_time = time.time() - start_time
            # Optional: Print or log the estimated time remaining
            # print(f"Threshold increased to {min_threshold}. Elapsed time: {total_elapsed_time/60:.2f} minutes. "
            #       f"Estimated remaining time: {estimated_time_remaining/60:.2f} minutes.")

        if min_threshold == float('inf') or threshold > max_threshold:
            total_time = time.time() - start_time
            pbar.set_description("IDA* Terminated")
            pbar.close()
            return None, nodes_evaluated

        threshold = min_threshold


def bidirectional_search(start_state: tuple, puzzle_dim: int):
    """
    Solve the puzzle using Bi-Directional Search (BDS) with time estimation.
    """
    goal_state = tuple([i for i in range(1, puzzle_dim**2)] + [0])
    start_bytes = start_state
    goal_bytes = goal_state

    # Initialize two queues and visited sets
    forward_queue = deque([start_bytes])
    backward_queue = deque([goal_bytes])
    forward_visited = {start_bytes}
    backward_visited = {goal_bytes}

    # Map each visited state to the state it came from
    forward_came_from = {}
    backward_came_from = {}

    nodes_evaluated = 0
    pbar = tqdm(desc="Bi-Directional Search Progress", unit="nodes", dynamic_ncols=True)
    start_time = time.time()

    last_time = start_time
    last_nodes_evaluated = 0

    while forward_queue and backward_queue:
        # Expand forward search
        if forward_queue:
            current_forward = forward_queue.popleft()
            nodes_evaluated += 1
            pbar.update(1)

            if current_forward in backward_visited:
                total_time = time.time() - start_time
                pbar.set_description("Bi-Directional Search Completed")
                pbar.close()
                return reconstruct_bidirectional_path(
                    current_forward,
                    forward_came_from,
                    backward_came_from
                ), nodes_evaluated

            for action_move in available_actions(current_forward, puzzle_dim):
                neighbor = do_action(current_forward, action_move)
                if neighbor not in forward_visited:
                    forward_visited.add(neighbor)
                    forward_queue.append(neighbor)
                    forward_came_from[neighbor] = current_forward

        # Expand backward search
        if backward_queue:
            current_backward = backward_queue.popleft()
            nodes_evaluated += 1
            pbar.update(1)

            if current_backward in forward_visited:
                total_time = time.time() - start_time
                pbar.set_description("Bi-Directional Search Completed")
                pbar.close()
                return reconstruct_bidirectional_path(
                    current_backward,
                    forward_came_from,
                    backward_came_from
                ), nodes_evaluated

            for action_move in available_actions(current_backward, puzzle_dim):
                neighbor = do_action(current_backward, action_move)
                if neighbor not in backward_visited:
                    backward_visited.add(neighbor)
                    backward_queue.append(neighbor)
                    backward_came_from[neighbor] = current_backward

        # Periodically estimate remaining time
        if nodes_evaluated % 1000 == 0:
            current_time = time.time()
            elapsed_time = current_time - start_time
            nodes_since_last = nodes_evaluated - last_nodes_evaluated
            time_since_last = current_time - last_time
            nodes_per_second = nodes_since_last / time_since_last if time_since_last > 0 else 0
            estimated_total_nodes = (len(forward_queue) + len(backward_queue) + nodes_evaluated)
            estimated_remaining_nodes = estimated_total_nodes - nodes_evaluated
            estimated_time_remaining = estimated_remaining_nodes / nodes_per_second if nodes_per_second > 0 else float('inf')
            # Optional: Print or log the estimated time remaining
            # print(f"Nodes evaluated: {nodes_evaluated}, Estimated time remaining: {estimated_time_remaining/60:.2f} minutes")
            last_time = current_time
            last_nodes_evaluated = nodes_evaluated

    total_time = time.time() - start_time
    pbar.set_description("Bi-Directional Search Terminated")
    pbar.close()
    return None, nodes_evaluated  # No solution found


def reconstruct_bidirectional_path(intersection: tuple, forward_came_from: dict, backward_came_from: dict) -> list:
    """
    Reconstruct the path from the start state to the goal state via the intersection point.
    """
    # Reconstruct path from start to intersection
    forward_path = []
    current = intersection
    while current in forward_came_from:
        forward_path.append(current)
        current = forward_came_from[current]
    forward_path.reverse()

    # Reconstruct path from intersection to goal
    backward_path = []
    current = intersection
    while current in backward_came_from:
        current = backward_came_from[current]
        backward_path.append(current)

    # Combine forward and backward paths
    return forward_path + [intersection] + backward_path

# ------------------------------
# 4. Enhanced A* Algorithm with New Heuristic
# ------------------------------

def corner_conflict(state: tuple, puzzle_dim: int) -> int:
    """
    Calculates the number of corner tiles that are not in their correct positions.
    """
    conflict = 0
    # Define corner positions
    corners = [0, puzzle_dim - 1, puzzle_dim * (puzzle_dim - 1), puzzle_dim**2 - 1]
    # Define the correct tile for each corner position
    correct_tiles = [1, puzzle_dim, puzzle_dim * (puzzle_dim - 1), 0]  # Assuming 0 is the blank
    for pos, correct_tile in zip(corners, correct_tiles):
        if state[pos] != correct_tile and state[pos] != 0:
            conflict += 1
    return conflict


@lru_cache(maxsize=None)
def enhanced_heuristic(state: tuple, puzzle_dim: int) -> int:
    """
    Combines Manhattan Distance, Linear Conflict, and Corner Conflict for the A* heuristic.
    """
    return manhattan_distance(state, puzzle_dim) + linear_conflict(state, puzzle_dim) + corner_conflict(state, puzzle_dim)


def a_star_enhanced(state: tuple, puzzle_dim: int):
    """
    Solve the puzzle using the A* search algorithm with the enhanced heuristic.
    """
    goal = tuple([i for i in range(1, puzzle_dim**2)] + [0])

    open_set = []
    heappush(open_set, (enhanced_heuristic(state, puzzle_dim), 0, state))  # (f-score, g(n), state)
    came_from = {}
    g_score = {state: 0}
    f_score = {state: enhanced_heuristic(state, puzzle_dim)}
    nodes_evaluated = 0
    closed_set = set()

    pbar = tqdm(desc="A*_Enhanced Progress", unit="nodes", dynamic_ncols=True)
    start_time = time.time()

    last_time = start_time
    last_nodes_evaluated = 0

    while open_set:
        _, current_g, current = heappop(open_set)
        nodes_evaluated += 1
        pbar.update(1)

        if current == goal:
            total_time = time.time() - start_time
            pbar.set_description("A*_Enhanced Completed")
            pbar.close()
            return reconstruct_path(came_from, current), nodes_evaluated

        if current in closed_set:
            continue
        closed_set.add(current)

        # Periodically estimate remaining time
        if nodes_evaluated % 1000 == 0:
            current_time = time.time()
            elapsed_time = current_time - start_time
            nodes_since_last = nodes_evaluated - last_nodes_evaluated
            time_since_last = current_time - last_time
            nodes_per_second = nodes_since_last / time_since_last if time_since_last > 0 else 0
            estimated_total_nodes = (len(open_set) + nodes_evaluated)
            estimated_remaining_nodes = estimated_total_nodes - nodes_evaluated
            estimated_time_remaining = estimated_remaining_nodes / nodes_per_second if nodes_per_second > 0 else float('inf')
            # Optional: Print or log the estimated time remaining
            # print(f"Nodes evaluated: {nodes_evaluated}, Estimated time remaining: {estimated_time_remaining/60:.2f} minutes")
            last_time = current_time
            last_nodes_evaluated = nodes_evaluated

        for action_move in available_actions(current, puzzle_dim):
            neighbor = do_action(current, action_move)
            tentative_g = current_g + 1

            if neighbor in closed_set:
                continue

            tentative_f = tentative_g + enhanced_heuristic(neighbor, puzzle_dim)

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_f
                heappush(open_set, (tentative_f, tentative_g, neighbor))

    total_time = time.time() - start_time
    pbar.set_description("A*_Enhanced Terminated")
    pbar.close()
    return None, nodes_evaluated  # No solution found

# ------------------------------
# 5. Evaluation and Result Logging
# ------------------------------

def evaluate_algorithm(algorithm, initial_state: tuple, puzzle_dim: int) -> dict:
    """
    Evaluate the performance of a path-search algorithm for the n^2 - 1 puzzle.
    """
    solution_path, nodes_evaluated = algorithm(initial_state, puzzle_dim)

    # Compute metrics
    if solution_path:
        quality = len(solution_path) - 1
        efficiency = 1000 * quality / nodes_evaluated if nodes_evaluated != 0 else 0
    else:
        quality = None
        efficiency = None

    cost = nodes_evaluated

    return {
        "algorithm": algorithm.__name__,
        "puzzle_dim": puzzle_dim,
        "quality": quality,
        "cost": cost,
        "efficiency": efficiency
    }


def rank_algorithms(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rank algorithms based on their average efficiency from the DataFrame.
    """
    # Remove entries where efficiency is None (no solution found)
    df = df.dropna(subset=['efficiency'])

    # Use efficiency for ranking
    df['composite_score'] = df['efficiency']

    # Assign rank, handling NaN values
    df['rank'] = df.groupby('puzzle_dim')['composite_score'].rank(method='dense', ascending=False)
    df['rank'] = df['rank'].fillna(0).astype(int)

    return df.sort_values(['puzzle_dim', 'rank'])


def print_and_save_results(results: list, output_file: str = "algorithm_comparison.csv"):
    """
    Print the results, compute average efficiency, and save them to a CSV file for visualization.
    """
    # Convert results to DataFrame
    df = pd.DataFrame(results)

    # Compute average metrics per algorithm
    avg_results = df.groupby(['algorithm', 'puzzle_dim']).agg({
        'quality': 'mean',
        'cost': 'mean',
        'efficiency': 'mean'
    }).reset_index()

    # Print average results
    print(f"{'Algorithm':<25} {'Puzzle Size':<12} {'Avg Quality':<15} {'Avg Cost':<15} {'Avg Efficiency':<15}")
    print("=" * 85)
    for _, result in avg_results.iterrows():
        puzzle_size_str = f"{int(result['puzzle_dim'])}x{int(result['puzzle_dim'])}"
        quality_str = f"{result['quality']:.2f}" if not pd.isna(result['quality']) else "N/A"
        cost_str = f"{result['cost']:.2f}" if not pd.isna(result['cost']) else "N/A"
        efficiency_str = f"{result['efficiency']:.6f}" if not pd.isna(result['efficiency']) else "N/A"
        print(f"{result['algorithm']:<25} {puzzle_size_str:<12} {quality_str:<15} {cost_str:<15} {efficiency_str:<15}")

    # Save average results to CSV
    avg_results.to_csv(output_file, index=False)
    print(f"\nAverage results saved to {output_file}")

    # Rank algorithms
    ranked_df = rank_algorithms(avg_results)
    print("\n=== Algorithm Ranking ===")
    for puzzle_dim in ranked_df['puzzle_dim'].unique():
        print(f"\nPuzzle Size: {int(puzzle_dim)}x{int(puzzle_dim)}")
        subset = ranked_df[ranked_df['puzzle_dim'] == puzzle_dim]
        top_3 = subset.head(3)
        for _, row in top_3.iterrows():
            print(f"Rank {int(row['rank'])}: {row['algorithm']} (Avg Efficiency: {row['efficiency']:.6f})")


# ------------------------------
# 6. Visualization
# ------------------------------

def plot_results_from_csv(file_path: str):
    """
    Read results from a CSV file and generate comparative plots for quality, cost, and efficiency.
    """
    # Read the CSV file into a DataFrame
    results = pd.read_csv(file_path)

    # Extract unique algorithms and puzzle dimensions
    algorithms = results['algorithm'].unique()
    puzzle_sizes = sorted(results['puzzle_dim'].unique())

    # Initialize plots for quality, cost, efficiency
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    axes = axes.flatten()
    axes[0].set_title("Quality vs Puzzle Size")
    axes[1].set_title("Cost vs Puzzle Size")
    axes[2].set_title("Efficiency vs Puzzle Size")

    for algorithm in algorithms:
        # Filter data for the current algorithm
        algo_results = results[results['algorithm'] == algorithm]

        # Plot Quality
        axes[0].plot(
            algo_results['puzzle_dim'],
            algo_results['quality'],
            marker='o',
            label=algorithm
        )

        # Plot Cost
        axes[1].plot(
            algo_results['puzzle_dim'],
            algo_results['cost'],
            marker='o',
            label=algorithm
        )

        # Plot Efficiency
        axes[2].plot(
            algo_results['puzzle_dim'],
            algo_results['efficiency'],
            marker='o',
            label=algorithm
        )

    # Set labels and legends
    for ax in axes:
        ax.set_xlabel("Puzzle Size (n x n)")
        ax.set_xticks(puzzle_sizes)
        ax.set_xticklabels([f"{int(size)}x{int(size)}" for size in puzzle_sizes])
        ax.legend()
        ax.grid()

    axes[0].set_ylabel("Quality (Number of Actions)")
    axes[1].set_ylabel("Cost (Nodes Evaluated)")
    axes[2].set_ylabel("Efficiency (Quality / Cost)")

    # Show the plots
    plt.tight_layout()
    plt.show()


def plot_average_efficiency(results: list, output_dir: str = "plot", filename: str = "average_efficiency.png"):
    """
    Generate a bar plot showing the average efficiency of each algorithm and save it to a file.

    Args:
        results (list): List of dictionaries containing evaluation metrics.
        output_dir (str): Directory where the plot will be saved. Default is "plot".
        filename (str): Name of the file where the plot will be saved. Default is "average_efficiency.png".
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Convert results to DataFrame
    df = pd.DataFrame(results)

    # Compute average efficiency per algorithm
    avg_efficiency = df.groupby('algorithm')['efficiency'].mean().reset_index()

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.bar(avg_efficiency['algorithm'], avg_efficiency['efficiency'], color='skyblue')
    plt.xlabel('Algorithm')
    plt.ylabel('Average Efficiency')
    plt.title('Average Efficiency of Algorithms over Multiple Runs')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath)
    plt.close()  # Close the plot to free memory

    print(f"Plot saved to {filepath}")

# ------------------------------
# 7. Main Execution
# ------------------------------
if __name__ == "__main__":
    # Initialize list to store results
    results = []

    # Define algorithms to evaluate
    algorithms = [
        ida_star,
        a_star,
        a_star_enhanced,  # Newly added enhanced A* algorithm
        bidirectional_search,
        bfs,
        # dls,
        # iterative_deepening_dfs,
    ]

    # Maximum depth for DLS and IDDFS
    max_depth = 50  # Adjust as needed for larger puzzles

    # Number of runs
    num_runs = 1  # You may decrease this for larger puzzles to manage computational load

    # Iterate over each puzzle size
    for size in puzzle_sizes:
        PUZZLE_DIM = size  # Update puzzle dimension
        print(f"\n=== Solving {PUZZLE_DIM}x{PUZZLE_DIM} Puzzle ===")

        # Execute the process multiple times
        for run in range(num_runs):
            print(f"\n--- Run {run + 1}/{num_runs} ---")
            # Randomize the puzzle state
            initial_state = randomize_puzzle(puzzle_dim=PUZZLE_DIM, randomize_steps=RANDOMIZE_STEPS)

            print("Randomized initial state:")
            print(np.array(initial_state).reshape((PUZZLE_DIM, PUZZLE_DIM)))

            # Evaluate each algorithm
            for algorithm in algorithms:
                print(f"\nRunning {algorithm.__name__}...")

                result = evaluate_algorithm(algorithm, initial_state, PUZZLE_DIM)

                # Add run number to the result
                result['run'] = run + 1

                results.append(result)
                if result['quality'] is not None:
                    efficiency_str = f"{result['efficiency']:.4f}" if result['efficiency'] is not None else "N/A"
                    print(f"{algorithm.__name__} completed. Moves: {result['quality']}, Nodes Evaluated: {result['cost']}, Efficiency: {efficiency_str}")
                else:
                    cost_str = f"{int(result['cost'])}" if not pd.isna(result['cost']) else "N/A"
                    print(f"{algorithm.__name__} did not find a solution. Nodes Evaluated: {cost_str}")
    
    print(np.array(results).reshape((PUZZLE_DIM, PUZZLE_DIM)))

    # Print and save the results with ranking based on CSV
    print("\n=== Evaluation Results ===")
    print_and_save_results(results)

    # Plot the results
    plot_average_efficiency(results)
    
