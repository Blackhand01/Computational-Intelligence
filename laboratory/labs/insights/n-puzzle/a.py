from heapq import heappop, heappush
import numpy as np
from collections import namedtuple

PUZZLE_DIM = 4
Action = namedtuple('Action', ['pos1', 'pos2'])

# ----------------------------
# Utility Functions
# ----------------------------
def available_actions(state: np.ndarray) -> list[Action]:
    x, y = np.where(state == 0)
    x, y = int(x[0]), int(y[0])
    actions = []
    if x > 0:
        actions.append(Action((x, y), (x - 1, y)))
    if x < PUZZLE_DIM - 1:
        actions.append(Action((x, y), (x + 1, y)))
    if y > 0:
        actions.append(Action((x, y), (x, y - 1)))
    if y < PUZZLE_DIM - 1:
        actions.append(Action((x, y), (x, y + 1)))
    return actions

def do_action(state: np.ndarray, action: Action) -> np.ndarray:
    new_state = state.copy()
    new_state[action.pos1], new_state[action.pos2] = new_state[action.pos2], new_state[action.pos1]
    return new_state

def get_goal_position(value: int) -> tuple[int, int]:
    if value == 0:
        return (PUZZLE_DIM - 1, PUZZLE_DIM - 1)
    value -= 1
    return value // PUZZLE_DIM, value % PUZZLE_DIM

def manhattan_distance(state: np.ndarray) -> int:
    dist = 0
    for x in range(PUZZLE_DIM):
        for y in range(PUZZLE_DIM):
            value = state[x, y]
            if value != 0:
                target_x, target_y = get_goal_position(value)
                dist += abs(x - target_x) + abs(y - target_y)
    return dist

def is_solvable(state: np.ndarray) -> bool:
    flat = state.flatten()
    inversions = sum(
        flat[i] > flat[j] > 0
        for i in range(len(flat))
        for j in range(i + 1, len(flat))
    )
    zero_row = np.where(state == 0)[0][0]
    if PUZZLE_DIM % 2 == 1:
        return inversions % 2 == 0
    else:
        return (inversions + zero_row) % 2 == 0

def reconstruct_path(came_from: dict, start: tuple, end: tuple) -> list:
    path = []
    current = end
    while current in came_from:
        path.append(current)
        current = came_from[current]
    return path[::-1]

# ----------------------------
# Bidirectional A* Algorithm
# ----------------------------
def bidirectional_a_star(initial_state: np.ndarray):
    if not is_solvable(initial_state):
        return None, 0, 0, 0, initial_state, None

    goal_state = np.array([i for i in range(1, PUZZLE_DIM**2)] + [0]).reshape((PUZZLE_DIM, PUZZLE_DIM))

    # Define the heaps and sets for the two search fronts
    forward_heap = []
    backward_heap = []

    forward_g = {initial_state.tobytes(): 0}
    backward_g = {goal_state.tobytes(): 0}

    forward_came_from = {}
    backward_came_from = {}

    heappush(forward_heap, (manhattan_distance(initial_state), initial_state.tobytes()))
    heappush(backward_heap, (manhattan_distance(goal_state), goal_state.tobytes()))

    forward_visited = {initial_state.tobytes()}
    backward_visited = {goal_state.tobytes()}

    state_mapping = {initial_state.tobytes(): initial_state, goal_state.tobytes(): goal_state}

    total_nodes_evaluated = 0

    while forward_heap and backward_heap:
        # Expand the forward front
        _, current_forward_hash = heappop(forward_heap)
        current_forward = state_mapping[current_forward_hash]

        if current_forward_hash in backward_visited:
            # Intersection found
            mid_state = current_forward_hash
            forward_path = reconstruct_path(forward_came_from, initial_state.tobytes(), mid_state)
            backward_path = reconstruct_path(backward_came_from, goal_state.tobytes(), mid_state)
            backward_path = backward_path[::-1][1:]  # Reverse and remove duplicate
            return forward_path + backward_path, len(forward_path) + len(backward_path), total_nodes_evaluated

        for act in available_actions(current_forward):
            neighbor = do_action(current_forward, act)
            neighbor_hash = neighbor.tobytes()
            state_mapping[neighbor_hash] = neighbor

            tentative_g = forward_g[current_forward_hash] + 1
            if neighbor_hash not in forward_g or tentative_g < forward_g[neighbor_hash]:
                forward_g[neighbor_hash] = tentative_g
                forward_came_from[neighbor_hash] = current_forward_hash
                heappush(forward_heap, (tentative_g + manhattan_distance(neighbor), neighbor_hash))
                forward_visited.add(neighbor_hash)

        total_nodes_evaluated += 1

        # Expand the backward front
        _, current_backward_hash = heappop(backward_heap)
        current_backward = state_mapping[current_backward_hash]

        if current_backward_hash in forward_visited:
            # Intersection found
            mid_state = current_backward_hash
            forward_path = reconstruct_path(forward_came_from, initial_state.tobytes(), mid_state)
            backward_path = reconstruct_path(backward_came_from, goal_state.tobytes(), mid_state)
            backward_path = backward_path[::-1][1:]  # Reverse and remove duplicate
            return forward_path + backward_path, len(forward_path) + len(backward_path), total_nodes_evaluated

        for act in available_actions(current_backward):
            neighbor = do_action(current_backward, act)
            neighbor_hash = neighbor.tobytes()
            state_mapping[neighbor_hash] = neighbor

            tentative_g = backward_g[current_backward_hash] + 1
            if neighbor_hash not in backward_g or tentative_g < backward_g[neighbor_hash]:
                backward_g[neighbor_hash] = tentative_g
                backward_came_from[neighbor_hash] = current_backward_hash
                heappush(backward_heap, (tentative_g + manhattan_distance(neighbor), neighbor_hash))
                backward_visited.add(neighbor_hash)

        total_nodes_evaluated += 1

    return None, 0, total_nodes_evaluated

# ----------------------------
# Test the Algorithm
# ----------------------------
if __name__ == "__main__":
    RANDOMIZE_STEPS = 1000
    state = np.array([i for i in range(1, PUZZLE_DIM**2)] + [0]).reshape((PUZZLE_DIM, PUZZLE_DIM))
    for _ in range(RANDOMIZE_STEPS):
        state = do_action(state, np.random.choice(available_actions(state)))

    print("Initial state:")
    print(state)

    solution, quality, nodes_evaluated = bidirectional_a_star(state)

    if solution:
        print(f"Solution found in {quality} steps!")
        print(f"Nodes evaluated: {nodes_evaluated}")
    else:
        print("No solution found!")
