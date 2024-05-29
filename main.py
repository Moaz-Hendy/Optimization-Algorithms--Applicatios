import numpy as np
from ACO import AntColony
from WPP import Wagon_Packing


class Truck():
    def __init__(self, wagon_volume, truck_id, milage_per_gallon, map, items):
        self.wagon_volume = wagon_volume
        self.truck_id = truck_id
        self.milage_per_gallon = milage_per_gallon
        self.map = map
        self.optimal_path = AntColony(distances, 1, 1, 100, 0.95, alpha=1, beta=1).run()
        self.items = items
        self.wp = Wagon_Packing(wagon_size=wagon_volume)
        self.org = self.wp.genetic_algorithm(population_size=50, generations=100, items=items)


distances = np.array([[np.inf, 2, 2, 5, 7],
                      [2, np.inf, 4, 8, 2],
                      [2, 4, np.inf, 1, 3],
                      [5, 8, 1, np.inf, 2],
                      [7, 2, 3, 2, np.inf]])

items = [((0, 0, 0), (2, 2, 1)), ((0, 0, 0), (3, 1, 3)), ((0, 0, 0), (4, 4, 2))]

tr = Truck(wagon_volume=(10, 10, 10), truck_id=5426, milage_per_gallon=25, map=distances,
           items=items)
print(tr.org)
print('\n')
print(tr.optimal_path)