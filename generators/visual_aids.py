# CENG 487 Assignment4 by
# Bugrahan Imal
# StudentId: 280201012
# May 2025
from math3d import Vec3D
from object3d import Object3D
from geometry import Mesh, Edge, Vertex
from shaders import Shader


def create_line(shader:Shader, start:Vec3D, end:Vec3D) -> Object3D:
    v0 = Vertex(start)
    v1 = Vertex(end)
    edge = Edge(v0, v1)

    mesh = Mesh("Line", vertices=[v0, v1], edges=[edge])

    obj = Object3D(shader, "Line", data=mesh)
    return obj

def create_grid_lines(shader:Shader, count:int=101, spacing:float=1) -> list[Object3D]:
    lines = []
    extent = (count - 1) * spacing / 2
    for i in range(count):
        offset = -extent + i * spacing
        lines.append(create_line(shader, Vec3D(-extent, offset, 0), Vec3D(extent, offset, 0)))
        lines.append(create_line(shader, Vec3D(offset, -extent, 0), Vec3D(offset, extent, 0)))
    return lines        
