import random
import math
import copy

# Target state for the 8-puzzle
TARGET_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

# Define possible moves
MOVES = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up

def is_target_state(state):
    """Check if the given state matches the target state."""
    return state == TARGET_STATE

def find_blank_position(state):
    """Find the position of the blank tile in the given state."""
    for row_index, row in enumerate(state):
        if 0 in row:
            return row_index, row.index(0)
    return None

def move_blank(state, direction):
    """Move the blank tile in the given direction and return the new state."""
    row, col = find_blank_position(state)
    new_row, new_col = row + direction[0], col + direction[1]

    if 0 <= new_row < 3 and 0 <= new_col < 3:
        new_state = copy.deepcopy(state)
        new_state[row][col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[row][col]
        return new_state
    return None

def generate_neighbors(state):
    """Generate all possible neighboring states by moving the blank tile."""
    neighbors = []
    for direction in MOVES:
        new_state = move_blank(state, direction)
        if new_state:
            neighbors.append(new_state)
    return neighbors

def calculate_manhattan_distance(state):
    """Calculate the Manhattan distance heuristic for the given state."""
    distance = 0
    for row in range(3):
        for col in range(3):
            tile = state[row][col]
            if tile != 0:
                target_row, target_col = divmod(tile - 1, 3)
                distance += abs(target_row - row) + abs(target_col - col)
    return distance

def simulated_annealing(initial_state, initial_temp=1000, cooling_rate=0.995, max_iterations=50000):
    """Simulated annealing algorithm to solve the 8-puzzle problem."""
    current_state = initial_state
    current_cost = calculate_manhattan_distance(current_state)
    best_state = current_state
    best_cost = current_cost
    temperature = initial_temp

    for _ in range(max_iterations):
        neighbors = generate_neighbors(current_state)
        if not neighbors:
            break

        next_state = random.choice(neighbors)
        next_cost = calculate_manhattan_distance(next_state)

        delta_cost = next_cost - current_cost
        if delta_cost < 0 or random.random() < math.exp(-delta_cost / temperature):
            current_state = next_state
            current_cost = next_cost
            if current_cost < best_cost:
                best_state = current_state
                best_cost = current_cost

        temperature *= cooling_rate

        if best_cost == 0:
            break

    return best_state

def print_state(state):
    """Print the given state in a formatted way."""
    for row in state:
        print(' '.join(map(str, row)))
    print()

# Initial configuration
initial_configuration = [[1, 2, 3], [4, 5, 6], [0, 7, 8]]

print("Initial Configuration:")
print_state(initial_configuration)

final_state = simulated_annealing(initial_configuration)

print("Final Configuration:")
print_state(final_state)

if is_target_state(final_state) == True :
    print("Final target state successfully reached!")
else:
    print("Current state is not the target state.")