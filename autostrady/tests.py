import geometry_utils
from model import Point
from evolutionary_highways import EvolutionaryHighways
import numpy as np


test = EvolutionaryHighways()
selected_map = test.select_best_map(125, 40000, 50, 20)
selected_map.print_self()
maps = test.maps
print("---------------------------------------------")
for single_map in maps:
    single_map.print_self()