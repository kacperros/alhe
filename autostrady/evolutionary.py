import cost_utils
import ast


def read_cities():
    with open('cities.txt') as cities_file:
        content = cities_file.read()
    return ast.literal_eval(content)


def __get_bounds(cities):
    max_x = float('Inf')
    min_x = float('-Inf')
    max_y = float('Inf')
    min_y = float('-Inf')