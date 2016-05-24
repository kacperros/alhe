import geometry_utils

points = [[4, 3], [3, 8], [10, 0]]
print(geometry_utils.get_distance_point_to_segment(points[1], points[2], points[0]))

points = [[1, 1], [3, 8], [10, 0]]
print(geometry_utils.get_distance_point_to_segment(points[1], points[2], points[0]))

points = [[1, 1], [3, 8], [10, 10]]
print(geometry_utils.get_distance_point_to_segment(points[1], points[2], points[0]))

points = [[4, 3], [3, 8], [10, 0]]
print(geometry_utils.get_distance_point_to_segment(points[1], points[2], points[0]))