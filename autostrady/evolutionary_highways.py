import geometry_utils
import ast
import random
from model import Point, Highway, Map
import numpy
import math


class EvolutionaryHighways:
    def __init__(self):
        self.cities = []
        self.maps = []
        self.x_max = 0
        self.y_max = 0
        self.x_min = 0
        self.y_min = 0
        self.population_size = 0
        self.max_iterations = 0
        self.parent_mutation_chance = 0
        self.child_mutation_chance = 0
        self.child_add_highway_chance = 0

    def select_best_map_with_improvement(self, population_size, max_iterations, highway_km_cost, route_km_cost, turn_cost,
                                         num_analyzed, connect, parent_mutation_likelyhood, child_mutation_likelyhood,
                                         child_add_highway_chance):
        self.population_size = population_size
        self.max_iterations = max_iterations
        self.parent_mutation_chance = 1 - parent_mutation_likelyhood
        self.child_mutation_chance = 1 - child_mutation_likelyhood
        self.child_add_highway_chance = 1 - child_add_highway_chance
        self.__select_best_map(highway_km_cost, route_km_cost, turn_cost)
        improved_maps = self.maps[:num_analyzed]
        for improved_map in self.maps[:num_analyzed]:
            improved_map.improve_map()
        if connect:
            for improved_map in improved_maps:
                improved_map.connect_map()
        improved_maps.sort(key=lambda x: x.cost)
        return improved_maps[0]

    def __select_best_map(self, highway_km_cost, route_km_cost, turn_cost):
        self.read_cities()
        self._get_bounds()
        self._generate_start_population(highway_km_cost, route_km_cost, turn_cost)
        lowest_cost = self._get_lowest_cost()
        iterations_counter = 0
        no_better_cost_counter = 0
        while iterations_counter < self.max_iterations and no_better_cost_counter < 100:
            self._evolve_population()
            if self._cost_improved(lowest_cost):
                no_better_cost_counter = 0
            iterations_counter += 1
        return self._get_best_map_from_current_population()

    def read_cities(self):
        with open('cities.txt') as cities_file:
            content = cities_file.read()
        cities = ast.literal_eval(content)
        for city in cities:
            self.cities.append(Point(city[0], city[1]))

    def _get_bounds(self):
        max_x = float('-Inf')
        min_x = float('Inf')
        max_y = float('-Inf')
        min_y = float('Inf')
        for city in self.cities:
            min_x = min(min_x, city.x)
            max_x = max(max_x, city.x)
            min_y = min(min_y, city.y)
            max_y = max(max_y, city.y)
        self.x_min = min_x
        self.x_max = max_x
        self.y_min = min_y
        self.y_max = max_y

    def _generate_start_population(self, highway_km_cost, route_km_cost, turn_cost):
        for i in range(0, self.population_size):
            starting_highway = self._get_random_highway_in_bounds()
            created_map = Map([starting_highway], self.cities, highway_km_cost, route_km_cost, turn_cost)
            self.maps.append(created_map)

    def _get_random_highway_in_bounds(self):
        start = self.__get_random_point_in_bounds()
        end = self.__get_random_point_in_bounds()
        return Highway(start, end)

    def __get_random_point_in_bounds(self):
        x_range = self.x_max - self.x_min
        y_range = self.y_max - self.y_min
        x = self.x_min + random.random() * x_range
        y = self.y_min + random.random() * y_range
        return Point(x, y)

    def _get_lowest_cost(self):
        lowest_cost = float('Inf')
        for checked_map in self.maps:
            lowest_cost = min(checked_map.cost, lowest_cost)
        return lowest_cost

    def _cost_improved(self, current_best_cost):
        current_cost = self._get_lowest_cost()
        if current_cost < current_best_cost:
            return True
        else:
            return False

    def _get_best_map_from_current_population(self):
        self.maps.sort(key=lambda x: x.cost)
        best_map = self.maps[0]
        return best_map

    def _evolve_population(self):
        parents = self.__pair_parents(int(self.population_size / 3))
        children = self.__breed_children(parents)
        children = self.__mutate_children(children)
        mutated_parents = self.__mutate_parents()
        self.maps.extend(children)
        self.maps.extend(mutated_parents)
        self.maps.sort(key=lambda x: x.cost)
        self.maps = self.maps[:self.population_size]

    def __pair_parents(self, number_of_families):
        parents_origin = []
        max_cost = 0
        parents = []
        for single_map in self.maps:
            max_cost = max(single_map.cost, max_cost)
        for single_map in self.maps:
            added_maps = [single_map] * int(single_map.cost * 10 / max_cost)
            parents_origin.extend(added_maps)
        for i in range(0, number_of_families):
            parents_chosen = numpy.random.choice(parents_origin, 2)
            parents.append(parents_chosen)
        return parents

    def __breed_children(self, parents):
        children = []
        for parents_pair in parents:
            child = self.__mate_parents(parents_pair)
            children.append(child)
        return children

    def __mate_parents(self, parents_pair):
        parent1 = parents_pair[0]
        parent2 = parents_pair[1]
        merged_highways = geometry_utils.get_average_lines(parent1.highways, parent2.highways,
                                                           parent1.cost / (parent2.cost + parent1.cost))
        child = Map(merged_highways, parent1.cities, parent1.highway_km_cost, parent1.route_km_cost, parent1.turn_cost)
        return child

    def __mutate_children(self, children):
        for child in children:
            if self.child_mutation_chance < numpy.random.random():
                if self.child_add_highway_chance < numpy.random.random():
                    child.add_highway(self._get_random_highway_in_bounds())
                else:
                    child.rem_random_highway()
        return children

    def __mutate_parents(self):
        mutated_parents = []
        for curr_map in self.maps:
            if self.parent_mutation_chance < numpy.random.random():
                mutated_highways = []
                for highway in curr_map.highways:
                    start_x = highway.start.x + (self.x_max - self.x_min) * random.random()
                    start_y = highway.start.y + (self.y_max - self.y_min) * random.random()
                    end_x = highway.end.x + (self.x_max - self.x_min) * random.random()
                    end_y = highway.end.y + (self.y_max - self.y_min) * random.random()
                    mutated_highways.append(Highway(Point(start_x, start_y), Point(end_x, end_y)))
                mutated_parents.append(
                    Map(mutated_highways, curr_map.cities, curr_map.highway_km_cost, curr_map.route_km_cost, curr_map.turn_cost))
        return mutated_parents