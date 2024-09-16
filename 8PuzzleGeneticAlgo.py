import random
import numpy as np

# Target state for the 8-puzzle
TARGET_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 0]

def create_random_state():
    """Create a random configuration of the 8-puzzle."""
    state = TARGET_STATE[:]
    random.shuffle(state)
    return state

def calculate_fitness(state):
    """Compute fitness score as the count of misplaced tiles."""
    return sum([1 for index in range(9) if state[index] != TARGET_STATE[index]])

def perform_crossover(parent_a, parent_b):
    """Combine two parent states to produce a child state."""
    crossover_point = random.randint(1, 7)
    child_state = parent_a[:crossover_point] + parent_b[crossover_point:]
    return child_state

def apply_mutation(state):
    """Randomly modify the state by swapping two tiles."""
    index1, index2 = random.sample(range(9), 2)
    state[index1], state[index2] = state[index2], state[index1]
    return state

def tournament_selection(population):
    """Select a parent using tournament selection method."""
    tournament_group = random.sample(population, 3)
    tournament_group.sort(key=lambda x: x[1])
    return tournament_group[0][0]

def genetic_solver(start_state, pop_size=100, mutation_chance=0.2, max_gen=50000):
    """Genetic algorithm to solve the 8-puzzle challenge."""
    population = [(start_state, calculate_fitness(start_state))]

    # Create initial population
    for _ in range(pop_size - 1):
        individual = create_random_state()
        population.append((individual, calculate_fitness(individual)))

    solution_path = []
    generation_count = 0

    while generation_count < max_gen:
        population.sort(key=lambda x: x[1])
        solution_path.append(population[0][0])

        if population[0][1] == 0:  # Stop if the goal state is achieved
            print(f"Goal state achieved in generation {generation_count}!")
            break

        new_population = population[:20]  # Retain the top 20 individuals

        while len(new_population) < pop_size:
            parent_a = tournament_selection(population)
            parent_b = tournament_selection(population)
            offspring = perform_crossover(parent_a, parent_b)
            if random.uniform(0, 1) < mutation_chance:
                offspring = apply_mutation(offspring)
            new_population.append((offspring, calculate_fitness(offspring)))

        population = new_population
        generation_count += 1

    return solution_path

def verify_goal_state(solution_path):
    """Check if the last state in the solution path is the target state."""
    if solution_path[-1] == TARGET_STATE:
        print("Final target state successfully reached!")
    else:
        print("Current state is not the target state.")

# Initial configuration
initial_configuration = [1, 2, 3, 0, 5, 6, 4, 7, 8]

# Execute the genetic algorithm
solution_path = genetic_solver(initial_configuration)

# Display all configurations from the initial to the final state
print("Configurations from initial to final state:")
for step_index, configuration in enumerate(solution_path):
    print(f"\nStep {step_index}:")
    for i in range(0, 9, 3):
        print(configuration[i:i+3])

# Verify the final state
verify_goal_state(solution_path)