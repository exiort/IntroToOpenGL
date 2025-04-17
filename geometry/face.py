# CENG 487 Assignment1 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from __future__ import annotations
from .vertex import Vertex
from math3d import Vec3D



class Face:
    vertices: list[Vertex]
    surface_id:int
    
    def __init__(self, vertices: list[Vertex], surface_id:int) -> None:
        self.vertices = vertices
        self.surface_id = surface_id
        
    def __repr__(self) -> str:
        return f"Face with : {self.vertices}"

    def copy(self, vertex_map:dict[Vertex,Vertex]) -> Face:
        new_vertices = [vertex_map[v] for v in self.vertices]
        return Face(new_vertices, self.surface_id)
    
    def center(self) -> Vec3D:
        total = Vec3D()
        for v in self.vertices:
            total += v.position
        return total * (1 / len(self.vertices))
    
