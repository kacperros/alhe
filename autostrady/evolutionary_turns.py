import copy

class EvolutionaryTurns:
    def __init__(self, evolved_map, population_size, iterations, turn_cost, turn_min_distance):
        self.evolved_map = evolved_map
        self.turn_cost = turn_cost
        self.turn_dist = turn_min_distance
        self.maps = []
        self.population_size = population_size
        self.iterations = iterations
        for i in range(0, population_size):
            copied_map = copy.deepcopy(evolved_map)
            self.maps.append(copy.deepcopy(evolved_map))

    def evolve_turns(self):
        highways = self.evolved_map.highways
        turns = [highway.start for highway in highways]
        turns.extend([highway.end for highway in highways])
        cities = self.evolved_map.cities
