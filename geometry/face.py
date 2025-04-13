# CENG 487 Assignment1 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from .vertex import Vertex

from math3d import Vec3D


class Face:
    vertices: list[Vertex]
    
    def __init__(self, vertices: list[Vertex]) -> None:
        self.vertices = vertices

    def __repr__(self) -> str:
        return f"Face with : {self.vertices}"

    def copy(self, vertex_map:dict[Vertex,Vertex]):
        new_vertices = [vertex_map[v] for v in self.vertices]
        return Face(new_vertices)
    
    def center(self) -> Vec3D:
        total = Vec3D()
        for v in self.vertices:
            total += v.possition
        return total * (1 / len(self.vertices))
    
