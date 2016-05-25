import geometry_utils
import math


def highway_cost_function(highways, cities, per_km_cost):
    cost = 0
    for city in cities:
        cost += __get_distance_to_closest_highway(city, highways)
    return cost * per_km_cost


def __get_distance_to_closest_highway(city, highways):
    min_distance = float('Inf')
    for highway in highways:
        distance = __get_distance_to_highway(city, highway)
        if distance < min_distance:
            min_distance = distance
    return min_distance


def __get_distance_to_highway(city, highway):
    return geometry_utils.get_distance_point_to_segment(highway[0], highway[1], city)


def turn_cost_function(turns, cities, per_km_cost):
    distance = 0
    for city in cities:
        distance += __get_distance_to_closest_turn(turns, city)
    return distance * per_km_cost


def __get_distance_to_closest_turn(turns, city):
    min_distance = float('Inf')
    for turn in turns:
        min_distance = min(min_distance, math.sqrt(geometry_utils.get_distance_between_points(turn, city)))
    return min_distance
