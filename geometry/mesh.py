# CENG 487 Assignment1 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from __future__ import annotations
from .vertex import Vertex
from .edge import Edge
from .face import Face
from .mesh_algoritms import MeshAlgorithms
import numpy as np


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
    is_render_data_dirty:bool
    
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
        self.is_render_data_dirty = True

    def __repr__(self) -> str:
        return f"Mesh with name={self.name}, #vertices:{len(self.vertices)} #edges:{len(self.edges)} #faces:{len(self.faces)}"

    def copy(self) -> Mesh:
        vertex_map = {v:v.copy() for v in self.base_vertices}
        new_base_vertices = list(vertex_map.values())
        new_base_edges = [e.copy(vertex_map) for e in self.base_edges]
        new_base_faces = [f.copy(vertex_map) for f in self.base_faces]
        new_mesh = Mesh(f"{self.name}_Copy", new_base_vertices, new_base_edges, new_base_faces)

        new_mesh.current_subdivision_level = self.current_subdivision_level
        new_mesh.is_cache_dirty = True
        new_mesh.apply_subdivision()

        return new_mesh
    
    def add_vertex(self, v:Vertex) -> None:...

    def add_edge(self, e:Edge) -> None:...

    def add_face(self, f:Face) -> None:...

#    def apply_transform(self, matrix: Mat3D) -> None:
#        for v in self.vertices:
#            v.transform(matrix)
#
#        for v in self.base_vertices:
#            v.transform(matrix)
#
#        self.subdivision_cache.clear()
#        self.subdivision_cache[0] = (self.base_vertices, self.base_edges, self.base_faces)
#        self.is_cache_dirty = True
#        #self.apply_subdivision()
        
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
        self.is_render_data_dirty = True
        self.vertices, self.edges, self.faces = self.subdivision_cache[self.current_subdivision_level]
        

    def get_render_arrays(self) -> tuple[int, np.ndarray,  np.ndarray, np.ndarray, np.ndarray, int]:
        if self.faces :
            return 1, *self.__prepare_face_arrays()
        elif self.edges:
            return 2, *self.__prepare_line_arrays()
        #elif self.vertices:
        #    return 3, *self.__prepare_point_arrays()

        empty_array = np.array([], dtype=np.float32)
        return 0, empty_array, empty_array.copy(), empty_array.copy(), empty_array.copy(), 0
        
    def __prepare_face_arrays(self) -> tuple[np.ndarray,  np.ndarray, np.ndarray, np.ndarray, int]:
        positions_list = []
        uvs_list = []
        normals_list = []
        colors_list = []
        
        for face in self.faces:
            face_vertices = face.vertices
            if len(face_vertices) < 3:
                continue

            v0 = face_vertices[0]
            for i in range(1, len(face_vertices) - 1):
                triangle_v = [v0, face_vertices[i], face_vertices[i + 1]]
                for vertex in triangle_v:
                    positions_list.extend([vertex[0].position.x, vertex[0].position.y, vertex[0].position.z])
                    uvs_list.extend([vertex[1].uv.u, vertex[1].uv.v])
                    normals_list.extend([vertex[1].normal.x, vertex[1].normal.y, vertex[1].normal.z])
                    colors_list.extend([vertex[1].color.r, vertex[1].color.g, vertex[1].color.b, vertex[1].color.a])
                    
        positions = np.array(positions_list, dtype=np.float32)
        uvs = np.array(uvs_list, dtype=np.float32)
        normals = np.array(normals_list, dtype=np.float32)
        colors = np.array(colors_list, dtype=np.float32)
        
        count_vertices = len(positions) // 3 if positions.size > 0 else 0
        return positions, normals, uvs, colors, count_vertices

#Seperating Vertex and normal-uv informating to store mesh in geometric plane(A box should has 8 vertices not 24) leave vertices and edges unaware of normal-uv informations
#Geometry classes have implemented in first week, before learning winged edge structure. I am very aware of things can be better but changing whole code base at this phase
#would be a unfesible decision. Commented "__prepare_point_arrays" is deprecated due to this problem. Also, "__prepare_line_arrays" function became a very speacialist function.
#It didnt deprecated for using on grids, I aware of its not usable for all type of lines due to its hardcoded nature.
    def __prepare_line_arrays(self) -> tuple[np.ndarray,  np.ndarray, np.ndarray, np.ndarray, int]:
        positions_list = []
        normals_list = []
        uvs_list = []
        colors_list = []

        for edge in self.edges:
            edge_vertices = [edge.v1, edge.v2]
            for vertex in edge_vertices:
                positions_list.extend([vertex.position.x, vertex.position.y, vertex.position.z])
                uvs_list.extend([0, 0])
                normals_list.extend([0, 0, 1])
                colors_list.extend([0.9, 0.9, 0.9, 1])
        
        positions = np.array(positions_list, dtype=np.float32)
        uvs = np.array(uvs_list, dtype=np.float32)
        normals = np.array(normals_list, dtype=np.float32)
        colors = np.array(colors_list, dtype=np.float32)
        
        count_vertices = len(positions) // 3 if positions.size > 0 else 0
        return positions, normals, uvs, colors, count_vertices

"""
    def __prepare_point_arrays(self) -> tuple[np.ndarray,  np.ndarray, np.ndarray, int]:
        positions_list = []
        uvs_list = []
        normals_list = []

        for vertex in self.vertices:
            positions_list.extend([vertex.position.x, vertex.position.y, vertex.position.z])
            uvs_list.extend([vertex.uv.u, vertex.uv.v])
            normals_list.extend([vertex.normal.x, vertex.normal.y, vertex.normal.z])

        positions = np.array(positions_list, dtype=np.float32)
        uvs = np.array(uvs_list, dtype=np.float32)
        normals = np.array(normals_list, dtype=np.float32)

        count_vertices = len(positions) // 3 if positions.size > 0 else 0
        return positions, normals, uvs, count_vertices
"""
