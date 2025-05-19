# CENG 487 Assignment1 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from __future__ import annotations
from .vertex import Vertex
from .edge import Edge
from .face import Face
from .mesh_algoritms import MeshAlgorithms
from math3d import Mat3D



class Mesh:
    name:str
    vertices: list[Vertex]
    edges: list[Edge]
    faces: list[Face]

    base_vertices:list[Vertex]
    base_edges:list[Edge]
    base_faces:list[Face]
    
    current_subdivision_level:int    
    subdivision_cache:dict[int, tuple[list[Vertex], list[Edge], list[Face]]]
    is_cache_dirty:bool 
    
    def __init__(self, name:str="Default", vertices:list[Vertex]=[], edges:list[Edge]=[], faces:list[Face]=[]) -> None:
        self.name = name
        self.current_subdivision_level = 0

        vertex_map = {v: v.copy() for v in vertices}
        self.base_vertices = list(vertex_map.values())
        self.base_edges = [e.copy(vertex_map) for e in edges]
        self.base_faces = [f.copy(vertex_map) for f in faces]
        
        self.vertices = vertices
        self.edges = edges
        self.faces = faces

        self.subdivision_cache = {}
        self.subdivision_cache[0] = (self.base_vertices, self.base_edges, self.base_faces)
        self.is_cache_dirty = False

    def __repr__(self) -> str:
        return f"Mesh with name={self.name}, #vertices:{len(self.vertices)} #edges:{len(self.edges)} #faces:{len(self.faces)}"

    def copy(self) -> Mesh:
        vertex_map = {v:v.copy() for v in self.vertices}
        new_vertices = list(vertex_map.values())
        new_edges = [e.copy(vertex_map) for e in self.edges]
        new_faces = [f.copy(vertex_map) for f in self.faces]
        new_mesh = Mesh(f"{self.name}_Copy", new_vertices, new_edges, new_faces)

        vertex_map = {v:v.copy() for v in self.base_vertices}
        new_base_vertices = list(vertex_map.values())
        new_base_edges = [e.copy(vertex_map) for e in self.base_edges]
        new_base_faces = [f.copy(vertex_map) for f in self.base_faces]

        new_mesh.base_vertices = new_base_vertices
        new_mesh.base_edges = new_base_edges
        new_mesh.base_faces = new_base_faces
        
        new_mesh.current_subdivision_level = self.current_subdivision_level
        new_mesh.subdivision_cache = {}
        new_mesh.subdivision_cache[0] = (new_base_vertices, new_base_edges, new_base_faces)
        new_mesh.is_cache_dirty = True

        return new_mesh
    
    def add_vertex(self, v:Vertex) -> None:...

    def add_edge(self, e:Edge) -> None:...

    def add_face(self, f:Face) -> None:...

    def apply_transform(self, matrix: Mat3D) -> None:
        for v in self.vertices:
            v.transform(matrix)

        for v in self.base_vertices:
            v.transform(matrix)

        self.subdivision_cache.clear()
        self.subdivision_cache[0] = (self.base_vertices, self.base_edges, self.base_faces)
        self.is_cache_dirty = True
        #self.apply_subdivision()
        
    def increase_subdivision_level(self) -> None:
        self.current_subdivision_level += 1
        
    def decrease_subdivision_level(self) -> None:
        if self.current_subdivision_level != 0:
            self.current_subdivision_level -= 1
                    
    def set_subdivision_level(self, level:int) -> None:
        if level >= 0:
            self.current_subdivision_level = level
        
    def apply_subdivision(self) -> None:
        if len(self.subdivision_cache) - 1 == self.current_subdivision_level and not self.is_cache_dirty:
            return

        if not self.is_cache_dirty:
            if not self.current_subdivision_level in self.subdivision_cache:
                last_subdivision = len(self.subdivision_cache) - 1
                for _ in range(self.current_subdivision_level - last_subdivision):
                    last_vertices, last_edges, last_faces = self.subdivision_cache[last_subdivision]
                    new_vertices, new_edges, new_faces = MeshAlgorithms.calculate_catmull_clark(last_vertices, last_edges, last_faces)
                    last_subdivision += 1
                    self.subdivision_cache[last_subdivision] = (new_vertices, new_edges, new_faces)

        else:
            self.subdivision_cache.clear()
            self.subdivision_cache[0] = (self.base_vertices, self.base_edges, self.base_faces)
        
            for i in range(self.current_subdivision_level):
                last_vertices, last_edges, last_faces = self.subdivision_cache[i]
                new_vertices, new_edges, new_faces = MeshAlgorithms.calculate_catmull_clark(last_vertices, last_edges, last_faces)
                self.subdivision_cache[i + 1] = (new_vertices, new_edges, new_faces)

        self.is_cache_dirty = False
        self.vertices, self.edges, self.faces = self.subdivision_cache[self.current_subdivision_level]
