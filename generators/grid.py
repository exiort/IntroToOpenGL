# CENG 487 Assignment2 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from .line import create_line
from math3d import Vec3D
from object3d import Object3D



def create_grid_lines(count:int=21, spacing:float=1) -> list[Object3D]:
    lines = []
    extent = (count - 1) * spacing / 2
    for i in range(count):
        offset = -extent + i * spacing
        lines.append(create_line(Vec3D(-extent, offset, 0), Vec3D(extent, offset, 0)))
        lines.append(create_line(Vec3D(offset, -extent, 0), Vec3D(offset, extent, 0)))
    return lines
        
