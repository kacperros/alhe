import math
import numpy
from model import Point, Highway

def get_distance_point_to_segment(p1, p2, p):
    ps1 = [p1.x, p1.y]
    ps2 = [p2.x, p2.y]
    point = [p.x, p.y]
    v_p1p = [point[0] - ps1[0], point[1] - ps1[1]]
    v_p2p = [point[0] - ps2[0], point[1] - ps2[1]]
    v_p1p2 = [ps2[0] - ps1[0], ps2[1] - ps1[1]]
    v_p2p1 = [ps1[0] - ps2[0], ps1[1] - ps2[1]]
    if _2dvectors_form_obtuse_angle(v_p1p, v_p1p2) or _2dvectors_form_obtuse_angle(v_p2p, v_p2p1):
        return min(math.sqrt(_get_distance_between_points_squared(ps1, point)),
                   math.sqrt(_get_distance_between_points_squared(ps2, point)))
    return _2dvector_len(v_p1p) * math.sin(__get_angle_between_vectors(v_p1p, v_p1p2))


def __get_angle_between_vectors(v1, v2):
    temp = numpy.dot(v1, v2) / (_2dvector_len(v1) * _2dvector_len(v2))
    angle = math.acos(temp)
    return angle


def _2dvectors_form_obtuse_angle(v_1, v_2):
    angle = __get_angle_between_vectors(v_1, v_2)
    if math.pi/2 <= angle:
        return True
    else:
        return False


def _get_distance_between_points_squared(point_1, point_2):
    return ((point_1[0] - point_2[0]) ** 2) + (point_1[1] - point_2[1]) ** 2


def _2dvector_len(vect):
    return math.sqrt(vect[0] ** 2 + vect[1] ** 2)


def get_distance_between_points(point1, point2):
    p1 = [point1.x, point1.y]
    p2 = [point2.x, point2.y]
    return math.sqrt(_get_distance_between_points_squared(p1, p2))


def get_point_in_between_points(point1, point2, ratio):
    x_range = math.fabs(point1.x - point2.x)
    y_range = math.fabs(point1.y - point2.y)
    move_x = x_range * ratio
    move_y = y_range * ratio
    x = 0
    y = 0
    if point1.x < point2.x:
        x = point1.x + move_x
    else:
        x = point1.x - move_x
    if point1.y < point2.y:
        y = point1.y + move_y
    else:
        y = point1.y - move_y
    return Point(x, y)


def get_average_lines(lines1, lines2, proportion):
    if len(lines1) > len(lines2):
        return __get_average_points(lines1, lines2, proportion)
    else:
        return __get_average_points(lines2, lines1, 1-proportion)


def __get_average_points(longer_list, shorter_list, proportion):
    result = []
    for line in longer_list:
        nearest_line = __get_nearest_line(line, shorter_list)
        result.append(__average_two_lines(line, nearest_line, proportion))
    return result


def __get_nearest_line(line, shorter_list):
    nearest_line = None
    distance = float('Inf')
    for checked_line in shorter_list:
        if get_distance_between_points(checked_line.start, line.start) < distance or \
            get_distance_between_points(checked_line.start, line.end) < distance or \
            get_distance_between_points(checked_line.end, line.start) < distance or \
            get_distance_between_points(checked_line.end, line.end) < distance:
            nearest_line = checked_line
    return nearest_line


def __average_two_lines(line1, line2, proportion):
    start1 = line1.start
    end1 = line1.end
    start2 = None
    end2 = None
    if get_distance_between_points(start1, line2.start) < get_distance_between_points(start1, line2.end):
        start2 = line2.start
        end2 = line2.end
    else:
        start2 = line2.end
        end2 = line2.start
    merged_start = get_point_in_between_points(start1, start2, proportion)
    merged_end = get_point_in_between_points(end1, end2, proportion)
    return Highway(merged_start, merged_end)