# CENG 487 Assignment1 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from math3d import Mat3D, Vec3D



def set_pivot(pivot:Vec3D) -> list[Mat3D]:
    to_origin = Mat3D.translation(-pivot.x, -pivot.y, -pivot.z)
    to_pivot = Mat3D.translation(pivot.x, pivot.y, pivot.z)
    return [to_origin, to_pivot]


def rotate_around_vec(axis:str, angle_rad:float, pivot:Vec3D) -> Mat3D:
    to_origin, to_pivot = set_pivot(pivot)
    return to_pivot @ Mat3D.rotation(axis, angle_rad) @ to_origin 

