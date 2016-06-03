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
        self.turns = [self.start, self.end]
        self.connected = False

    def get_length(self):
        return geometry_utils.get_distance_between_points(self.start, self.end)

    def append_random_turn(self, min_dist):
        bounding_points_list = []
        if min_dist < geometry_utils.get_distance_between_points(self.start, self.end):
            for point_start in self.turns:
                for point_end in self.turns:
                    if point_start != point_end:
                        bounding_points_list.append(geometry_utils.get_bounding_points(point_start, point_end, min_dist))
            bounding_points = bounding_points_list[random.randint(0, len(bounding_points_list) - 1)]
            appended = geometry_utils.get_point_in_between_points(bounding_points[0],
                                                                              bounding_points[1], random.random())
            self.turns.append(appended)

    def print_self(self):
        print('Highway:\t start: x: ', self.start.x, ' y: ', self.start.y, '\t end: x: ', self.end.x, 'y: ', self.end.y)
        for turn in self.turns:
            print('\t Gateway: x: ', turn.x, 'y: ', turn.y)


class Map:
    def __init__(self, highways, cities, highway_km_cost, route_km_cost, turn_cost):
        self.highways = highways
        self.cities = cities
        self.highway_km_cost = highway_km_cost
        self.route_km_cost = route_km_cost
        self.turn_cost = turn_cost
        self.cost = 0
        self.calculate_highways_costs()

    def calculate_highways_costs(self):
        cost = 0
        distance = 0
        for city in self.cities:
            cost += self.__get_distance_to_closest_highway(city)
        cost = cost * self.route_km_cost
        for highway in self.highways:
            distance += highway.get_length()
        cost += distance * self.highway_km_cost
        self.cost = cost

    def calculate_highways_with_turns_costs(self):
        turns = self._get_turns()
        highways_length = 0
        route_length = 0
        for highway in self.highways:
            highways_length += highway.get_length()
        for city in self.cities:
            closest_turn = geometry_utils.get_closest_point(city, turns)
            route_length += geometry_utils.get_distance_between_points(city, closest_turn)
        return len(turns) * self.turn_cost + highways_length * self.highway_km_cost + route_length * self.route_km_cost

    def _get_turns(self):
        turns = []
        for highway in self.highways:
            turns.extend(highway.turns)
        return turns

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

    def improve_map(self):
        best_cost = self.cost
        for highway in self.highways:
            del highway
            self.calculate_highways_costs()
            if best_cost < self.cost:
                self.add_highway(highway)

    def connect_map(self):
        for highway in self.highways:
            if not highway.connected:
                closest_highway = self.__find_closest_highway(highway)
                self.__connect_highways(highway, closest_highway)

    def __find_closest_highway(self, highway):
        closest_highway = None
        closest_distance = float('Inf')
        for checked_highway in self.highways:
            if highway.start.x == checked_highway.start.x and highway.start.y == checked_highway.start.y \
                    and highway.end.x == checked_highway.end.x and highway.end.y == checked_highway.end.y:
                continue
            start_start = geometry_utils.get_distance_between_points(checked_highway.start, highway.start)
            start_end = geometry_utils.get_distance_between_points(checked_highway.start, highway.end)
            end_end = geometry_utils.get_distance_between_points(checked_highway.end, highway.end)
            end_start = geometry_utils.get_distance_between_points(checked_highway.end, highway.start)
            minimum_distance = min(closest_distance, start_end, start_start, end_end, end_start)
            if minimum_distance != closest_distance:
                closest_distance = minimum_distance
                closest_highway = checked_highway
        return closest_highway

    def __connect_highways(self, highway1, highway2):
        highway1.connected = True
        highway2.connected = True
        distances = [(geometry_utils.get_distance_between_points(highway1.start, highway2.start),
                      highway1.start, highway2.start),
                     (geometry_utils.get_distance_between_points(highway1.start, highway2.end),
                      highway1.start, highway2.end),
                     (geometry_utils.get_distance_between_points(highway1.end, highway2.end),
                      highway1.end, highway2.end),
                     (geometry_utils.get_distance_between_points(highway1.end, highway2.start),
                      highway1.end, highway2.start)]
        distances.sort(key=lambda x: x[0])
        connecting_highway = Highway(distances[0][1], distances[0][2])
        connecting_highway.connected = True
        self.add_highway(connecting_highway)
