import geometry_utils
import math
import random

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Highway:
    def __init__(self, start_point, end_point):
        self.start = start_point
        self.end = end_point
        self.cost = float('Inf')
        self.turns = []

    def print_self(self):
        print('Highway:\t start: x: ', self.start.x, ' y: ', self.start.y, '\t end: x: ', self.end.x, 'y: ', self.end.y)


class Map:
    def __init__(self, highways, cities, highway_km_cost, route_km_cost):
        self.highways = highways
        self.cities = cities
        self.highway_km_cost = highway_km_cost
        self.route_km_cost = route_km_cost
        self.cost = 0
        self.calculate_highways_costs()

    def calculate_highways_costs(self):
        cost = 0
        distance = 0
        for city in self.cities:
            cost += self.__get_distance_to_closest_highway(city)
        cost = cost * self.route_km_cost
        for highway in self.highways:
            distance += geometry_utils.get_distance_between_points(highway.start, highway.end)
        cost += distance * self.highway_km_cost
        self.cost = cost

    def __get_distance_to_closest_highway(self, city):
        min_distance = float('Inf')
        for highway in self.highways:
            distance = self.__get_distance_to_highway(city, highway)
            if distance < min_distance:
                min_distance = distance
        return min_distance

    def __get_distance_to_highway(self, city, highway):
        return geometry_utils.get_distance_point_to_segment(highway.start, highway.end, city)

    def print_self(self):
        for highway in self.highways:
            highway.print_self()
        print(self.cost)

    def add_highway(self, highway):
        self.highways.append(highway)
        self.calculate_highways_costs()

    def rem_random_highway(self):
        del self.highways[random.randrange(0, len(self.highways))]
        self.calculate_highways_costs()