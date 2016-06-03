from evolutionary_highways import EvolutionaryHighways
from evolutionary_turns import EvolutionaryTurns
import geometry_utils
from model import Point

highway_populations = [5, 50, 100, 400, 1000]
turns_populations = [5, 50, 100, 400, 1000]
max_iterations = [5, 50, 500, 5000]
highway_km_cost = [5, 20, 50, 100, 500]
route_km_cost = [5, 20, 50, 100, 500]
turn_cost = [5, 20, 50]
turn_min_dist = [0.5, 2, 5]
num_analyzed=[2, 10, 20, 40]
parent_mut_chance = [0.2, 0.5, 0.8]
child_mut_chance = [0.2, 0.5, 0.8]
child_add_highway_chance = [0.3, 0.5, 0.7, 0.9]
turn_mut_chance = [0.1, 0.4, 0.7, 0.9]


for pmc in parent_mut_chance:
    for cmc in child_mut_chance:
        for cahc in child_add_highway_chance:
            for tmc in turn_mut_chance:
                test = EvolutionaryTurns()
                selected_map = test.select_best_map_with_best_turns(50, 50, 250, 50, 20, 5, 2, 40, True, pmc, cmc, cahc, tmc)
                selected_map.print_self()
                print('--------------------------------')
