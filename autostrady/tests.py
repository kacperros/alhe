import geometry_utils
from model import Point
from evolutionary_highways import EvolutionaryHighways
import numpy as np


test = EvolutionaryHighways()
selected_map = test.select_best_map_with_improvement(50, 500, 50, 20, 10, True, 10)
selected_map.print_self()
