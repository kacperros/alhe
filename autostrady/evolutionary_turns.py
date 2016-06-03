from evolutionary_highways import EvolutionaryHighways
import copy
import geometry_utils
import random

class EvolutionaryTurns:
    def __init__(self):
        self.evolutionary_highways = EvolutionaryHighways()
        self.min_turn_dist = 0
        self.analyzed_map = None
        self.population = []
        self.population_size = 0
        self.turn_mutation_chance = 0
        self.turn_min_dist = 0


    def select_best_map_with_best_turns(self, population_highways_size, population_turns_size, max_iterations,
                                        highway_km_cost, route_km_cost, turn_cost, turn_min_distance,
                                         num_analyzed, connect, parent_mutation_likelyhood, child_mutation_likelyhood,
                                         child_add_highway_chance, turn_mutation_chance):
        self.population_size = population_turns_size
        self.turn_mutation_chance = 1 - turn_mutation_chance
        self.turn_min_dist = turn_min_distance
        self.evolutionary_highways.select_best_map_with_improvement(population_highways_size, max_iterations,
                                                                    highway_km_cost, route_km_cost, turn_cost,
                                                                    num_analyzed, connect,
                                                                    parent_mutation_likelyhood, child_mutation_likelyhood,
                                                                    child_add_highway_chance)
        self.analyzed_map = self.evolutionary_highways.maps[0]
        self.__create_starting_population()
        for i in range(0, max_iterations):
            self._evolve_population()
        self.population.sort(key=lambda x: x.cost)
        return self.population[0]

    def __create_starting_population(self):
        for i in range(0, self.population_size):
            new_map = copy.deepcopy(self.analyzed_map)
            for highway in new_map.highways:
                highway.append_random_turn(self.turn_min_dist)
            new_map.calculate_highways_with_turns_costs()
            self.population.append(new_map)

    def _evolve_population(self):
        for specimen in self.population:
            if self.turn_mutation_chance < random.random():
                self.population.append(self.__mutate_specimen(specimen))
        self.population.sort(key=lambda x: x.cost)
        self.population = self.population[:self.population_size]

    def __mutate_specimen(self, specimen):
        created_specimen = copy.deepcopy(specimen)
        for highway in created_specimen.highways:
            if self.turn_mutation_chance < random.random():
                highway.append_random_turn(self.min_turn_dist)
        created_specimen.calculate_highways_with_turns_costs()
        return created_specimen
