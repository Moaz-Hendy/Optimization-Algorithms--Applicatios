import random
import numpy as np

# Define the size of the wagon in 3D (length, width, height)
WAGON_SIZE = (10, 10, 10)


class Wagon_Packing:
    def __init__(self, wagon_size):
        self.wagon_size = wagon_size

    def generate_initial_population(self, population_size, items):
        population = []
        for _ in range(population_size):
            wagon = np.zeros(WAGON_SIZE, dtype=int)
            population.append((wagon, items))
        return population

    def fitness(self, individual):
        wagon, items = individual
        total_space = np.prod(WAGON_SIZE)
        used_space = np.sum([np.sum(wagon[item[0][0]:item[0][0] + item[0][1], item[0][1]:item[0][1] + item[0][2],
                                    item[0][2]:item[0][2] + item[0][1]]) for item in items])
        return total_space - used_space

    def crossover(self, parent1, parent2):
        crossover_point = random.randint(1, len(parent1[1]) - 1)
        child1_wagon = np.copy(parent1[0])
        child2_wagon = np.copy(parent2[0])
        child1_items = parent1[1][:crossover_point] + parent2[1][crossover_point:]
        child2_items = parent2[1][:crossover_point] + parent1[1][crossover_point:]
        for item in child1_items:
            if np.sum(child1_wagon[item[0][0]:item[0][0] + item[0][1], item[0][1]:item[0][1] + item[0][2],
                      item[0][2]:item[0][2] + item[0][1]]) == 0:
                child1_wagon[item[0][0]:item[0][0] + item[0][1], item[0][1]:item[0][1] + item[0][2],
                item[0][2]:item[0][2] + item[0][1]] = 1
        for item in child2_items:
            if np.sum(child2_wagon[item[0][0]:item[0][0] + item[0][1], item[0][1]:item[0][1] + item[0][2],
                      item[0][2]:item[0][2] + item[0][1]]) == 0:
                child2_wagon[item[0][0]:item[0][0] + item[0][1], item[0][1]:item[0][1] + item[0][2],
                item[0][2]:item[0][2] + item[0][1]] = 1
        return (child1_wagon, child1_items), (child2_wagon, child2_items)

    def mutate(self, individual):
        wagon, items = individual
        mutated_item_index = random.randint(0, len(items) - 1)
        mutated_item = items[mutated_item_index]

        # Mutate position: randomly translate the item within the wagon
        translation = [random.randint(-mutated_item[0][i], self.wagon_size[i] - mutated_item[0][i] - 1) for i in
                       range(3)]
        new_position = [mutated_item[0][i] + translation[i] for i in range(3)]

        # Ensure the new position is within the boundaries of the wagon
        for i in range(3):
            new_position[i] = max(0, min(new_position[i], self.wagon_size[i] - 1))

        # Convert the tuple to a list to modify the values
        new_position_list = list(mutated_item[0])
        for i in range(3):
            new_position_list[i] = new_position[i]

        # Convert the list back to a tuple
        mutated_item = (tuple(new_position_list), mutated_item[1])

        items[mutated_item_index] = mutated_item
        return wagon, items

    def select_individual(self, population):
        # Select an individual using tournament selection
        tournament_size = 3
        tournament = random.sample(population, tournament_size)
        return max(tournament, key=lambda x: self.fitness(x))

    def genetic_algorithm(self, population_size, generations, items):
        population = self.generate_initial_population(population_size, items)
        for generation in range(generations):
            offspring = []
            for _ in range(population_size // 2):
                parent1 = self.select_individual(population)
                parent2 = self.select_individual(population)
                child1, child2 = self.crossover(parent1, parent2)
                if random.random() < 0.1:  # Mutation rate
                    child1 = self.mutate(child1)
                if random.random() < 0.1:
                    child2 = self.mutate(child2)
                offspring.extend([child1, child2])
            population = offspring
        best_individual = max(population, key=lambda x: self.fitness(x))
        return best_individual


# # Example usage
# items = [((0, 0, 0), (2, 2, 1)), ((0, 0, 0), (3, 1, 3)), ((0, 0, 0), (4, 4, 2))]
# wp = Wagon_Packing(WAGON_SIZE)
# best_solution = wp.genetic_algorithm(population_size=50, generations=100, items=items)
# print("Best solution:", best_solution[1])
# print("Fitness:", wp.fitness(best_solution))
