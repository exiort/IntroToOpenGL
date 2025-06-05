# CENG 487 Assignment1 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from __future__ import annotations
from .vertex import Vertex
from .vertex_attributes import VertexAttributes
from math3d import Vec3D



class Face:
    vertices: list[tuple[Vertex, VertexAttributes]]
    surface_id:int
    
    def __init__(self, vertices: list[tuple[Vertex, VertexAttributes]], surface_id:int) -> None:
        self.vertices = vertices
        self.surface_id = surface_id
        
    def __repr__(self) -> str:
        return f"Face with : {self.vertices}"

    def copy(self, vertex_map:dict[Vertex,Vertex]) -> Face:
        new_vertices:list[tuple[Vertex, VertexAttributes]] = []
        for vertex, attribute in self.vertices:
            new_vertex = vertex_map[vertex]
            new_attribute = attribute.copy()
            new_vertices.append((new_vertex, new_attribute))
        return Face(new_vertices, self.surface_id)

    def get_vertices(self) -> tuple[Vertex, ...]:
        return tuple([v[0] for v in self.vertices])

    def get_attributes(self) -> tuple[VertexAttributes, ...]:
        return tuple([v[1] for v in self.vertices])
    
    def center(self) -> Vec3D:
        total = Vec3D(0, 0, 0, 0)
        for v in self.vertices:
            total += v[0].position.vectorize()
        total = total * (1 / len(self.vertices))
        return total.pointize()
