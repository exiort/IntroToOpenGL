# CENG 487 Assignment1 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from .basefactory2d import create_base_square, create_base_triangle
from object3d.object3d import Object3D
from math3d import Mat3D



def create_triangle(
        name:str="Triangle",
        sx:float=1, sy:float=1, sz:float=1,
) -> Object3D:
    base_triangle = create_base_triangle(name)
    base_triangle.do_transform(Mat3D.scaling(sx, sy, sz))
    base_triangle.apply_transform()
    return base_triangle

def create_square(
        name:str="Square",
        sx:float=1, sy:float=1, sz:float=1
)-> Object3D:
    base_square = create_base_square(name)
    base_square.do_transform(Mat3D.scaling(sx, sy, sz))
    base_square.apply_transform()
    return base_square

