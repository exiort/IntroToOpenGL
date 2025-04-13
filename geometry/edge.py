# CENG 487 Assignment1 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from __future__ import annotations
from .vertex import Vertex
from math3d import Vec3D



class Edge:
    v1: Vertex
    v2: Vertex
    
    def __init__(self, v1:Vertex, v2:Vertex) -> None:
        self.v1 = v1
        self.v2 = v2

    def __repr__(self) -> str:
        return f"Edge with {self.v1}, {self.v2}"

    def copy(self, vertex_map:dict[Vertex, Vertex]) -> Edge:
        return Edge(vertex_map[self.v1], vertex_map[self.v2])
    
    def length(self) -> float:
        return (self.v1.possition - self.v2.possition).magnitude()

    def midpoint(self) -> Vec3D:
        return (self.v1.possition + self.v2.possition) * 0.5

