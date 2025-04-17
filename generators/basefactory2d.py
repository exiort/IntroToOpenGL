# CENG 487 Assignment1 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from geometry import Vertex, Edge, Face, Mesh
from object3d import Object3D
from math3d import Vec3D



def create_base_triangle(name:str="Triange") -> Object3D:
    v0 = Vertex(Vec3D(0, 1, 0))
    v1 = Vertex(Vec3D(-1, -1, 0))
    v2 = Vertex(Vec3D(1, -1, 0))

    edges = [Edge(v0, v1), Edge(v1, v2), Edge(v2, v0)]
    face = Face([v0, v1, v2], 0)
    mesh = Mesh(name, vertices=[v0, v1, v2], edges=edges, faces=[face])
    return Object3D(name, mesh)


def create_base_square(name:str="Square") -> Object3D:
    v0 = Vertex(Vec3D(-1, 1, 0))
    v1 = Vertex(Vec3D(-1, -1, 0))
    v2 = Vertex(Vec3D(1, -1, 0))
    v3 = Vertex(Vec3D(1, 1, 0))

    edges = [Edge(v0, v1), Edge(v1, v2), Edge(v2, v3), Edge(v3, v0)]
    face = Face([v0, v1, v2, v3], 0)
    mesh = Mesh(name, vertices=[v0, v1, v2, v3], edges=edges, faces=[face])
    return Object3D(name, mesh)

