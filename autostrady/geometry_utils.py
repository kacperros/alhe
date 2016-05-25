import math
import numpy


def get_distance_point_to_segment(ps1, ps2, p):
    v_p1p = [p[0] - ps1[0], p[1] - ps1[1]]
    v_p2p = [p[0] - ps2[0], p[1] - ps2[1]]
    v_p1p2 = [ps2[0] - ps1[0], ps2[1] - ps1[1]]
    v_p2p1 = [ps1[0] - ps2[0], ps1[1] - ps2[1]]
    if _2dvectors_form_obtuse_angle(v_p1p, v_p1p2) or _2dvectors_form_obtuse_angle(v_p2p, v_p2p1):
        return min(math.sqrt(_get_distance_between_points_squared(ps1, p)),
                   math.sqrt(_get_distance_between_points_squared(ps2, p)))
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


def get_distance_between_points(p1, p2):
    return math.sqrt(_get_distance_between_points_squared(p1, p2))