# CENG 487 Assignment2 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from object3d import Object3D
from geometry import Mesh, Edge, Vertex
from math3d import Vec3D



def create_line(start:Vec3D, end:Vec3D) -> Object3D:
    v0 = Vertex(start)
    v1 = Vertex(end)
    edge = Edge(v0, v1)

    mesh = Mesh("Line", vertices=[v0, v1], edges=[edge])

    obj = Object3D("Line", data=mesh)
    return obj

