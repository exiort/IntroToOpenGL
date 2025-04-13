# CENG 487 Assignment1 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from __future__ import annotations
from .vertex import Vertex
from .edge import Edge
from .face import Face
from math3d import Mat3D



class Mesh:
    name:str
    vertices: list[Vertex]
    edges: list[Edge]
    faces: list[Face]
    
    def __init__(self, name:str="Default", vertices:list[Vertex]=[], edges:list[Edge]=[], faces:list[Face]=[]) -> None:
        self.name = name
        self.vertices = vertices
        self.edges = edges
        self.faces = faces

    def __repr__(self) -> str:
        return f"Mesh with name={self.name}, #vertices:{len(self.vertices)} #edges:{len(self.edges)} #faces:{len(self.faces)}"

    def copy(self) -> Mesh:
        vertex_map = {v:v.copy() for v in self.vertices}
        new_vertices = list(vertex_map.values())
        new_edges = [e.copy(vertex_map) for e in self.edges]
        new_faces = [f.copy(vertex_map) for f in self.faces]
        return Mesh(f"{self.name}_Copy", new_vertices, new_edges, new_faces)
        
    def add_vertex(self, v:Vertex) -> None:
        self.vertices.append(v)

    def add_edge(self, e:Edge) -> None:
        self.edges.append(e)

    def add_face(self, f:Face) -> None:
        self.faces.append(f)

    def transform(self, matrix: Mat3D) -> None:
        for v in self.vertices:
            v.transform(matrix)
    
