# CENG 487 Assignment1 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from __future__ import annotations
from .vertex import Vertex
from .edge import Edge
from .face import Face
from math3d import Mat3D, Vec3D



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
                    new_vertices, new_edges, new_faces = Mesh.calculate_subdivision(last_vertices, last_edges, last_faces)
                    last_subdivision += 1
                    self.subdivision_cache[last_subdivision] = (new_vertices, new_edges, new_faces)

        else:
            self.subdivision_cache.clear()
            self.subdivision_cache[0] = (self.base_vertices, self.base_edges, self.base_faces)
        
            for i in range(self.current_subdivision_level):
                last_vertices, last_edges, last_faces = self.subdivision_cache[i]
                new_vertices, new_edges, new_faces = Mesh.calculate_subdivision(last_vertices, last_edges, last_faces)
                self.subdivision_cache[i + 1] = (new_vertices, new_edges, new_faces)

        self.is_cache_dirty = False
        self.vertices, self.edges, self.faces = self.subdivision_cache[self.current_subdivision_level]

    @staticmethod
    def split_geometry(vertices:list[Vertex], edges:list[Edge], faces:list[Face]) -> tuple[list[Vertex], list[Edge], list[Face]]:
        new_vertices:list[Vertex] = []
        new_edges_set:set[tuple[int, ...]] = set()
        new_faces:list[Face] = []

        vertex_map:dict[Vertex, Vertex] = {}
        edge_midpoint_map:dict[tuple[int, ...], Vertex] = {}
        face_centroid_map:dict[Face, Vertex] = {}

        for v_orig in vertices:
            v_copy = v_orig.copy()
            new_vertices.append(v_copy)
            vertex_map[v_orig] = v_copy
        
        for edge in edges:
            v1_orig, v2_orig = edge.v1, edge.v2
            edge_key = tuple(sorted((id(v1_orig), id(v2_orig))))
            if edge_key not in edge_midpoint_map:
                 v1_copy = vertex_map[v1_orig]
                 v2_copy = vertex_map[v2_orig]
                 mid_pos = Vec3D.middle_point(v1_copy.position, v2_copy.position)
                 mid_vertex = Vertex(mid_pos)
                 new_vertices.append(mid_vertex)
                 edge_midpoint_map[edge_key] = mid_vertex

        for face_orig in faces:
            center_pos_sum = Vec3D(0, 0, 0, 0)
            num_face_verts = len(face_orig.vertices)
            if num_face_verts > 0:
                for v_orig in face_orig.vertices:
                    v_copy = vertex_map[v_orig]
                    center_pos_sum += v_copy.position.vectorize()
                center_pos_sum = center_pos_sum * (1.0 / num_face_verts)
                center_pos = center_pos_sum.pointize()
            else:
                center_pos = Vec3D(0,0,0)
            center_vertex = Vertex(center_pos)
            new_vertices.append(center_vertex)
            face_centroid_map[face_orig] = center_vertex         
                 
        for face_orig in faces:
            orig_verts = face_orig.vertices
            num_orig_verts = len(orig_verts)
            sid = face_orig.surface_id
            copied_orig_verts = [vertex_map[v] for v in orig_verts]
            center_vert = face_centroid_map[face_orig]

            if num_orig_verts == 4:
                v0, v1, v2, v3 = copied_orig_verts
                m01 = edge_midpoint_map[tuple(sorted((id(orig_verts[0]), id(orig_verts[1]))))]
                m12 = edge_midpoint_map[tuple(sorted((id(orig_verts[1]), id(orig_verts[2]))))]
                m23 = edge_midpoint_map[tuple(sorted((id(orig_verts[2]), id(orig_verts[3]))))]
                m30 = edge_midpoint_map[tuple(sorted((id(orig_verts[3]), id(orig_verts[0]))))]
                f1 = Face([v0, m01, center_vert, m30], sid)
                f2 = Face([v1, m12, center_vert, m01], sid)
                f3 = Face([v2, m23, center_vert, m12], sid)
                f4 = Face([v3, m30, center_vert, m23], sid)
                new_faces.extend([f1, f2, f3, f4])
                edges_to_add = [(v0, m01), (m01, center_vert), (center_vert, m30), (m30, v0), (v1, m12), (m12, center_vert), (center_vert, m01), (m01, v1), (v2, m23), (m23, center_vert), (center_vert, m12), (m12, v2), (v3, m30), (m30, center_vert), (center_vert, m23), (m23, v3)]
                for v_a, v_b in edges_to_add: new_edges_set.add(tuple(sorted((id(v_a), id(v_b)))))

            elif num_orig_verts == 3:
                v0, v1, v2 = copied_orig_verts
                m01 = edge_midpoint_map[tuple(sorted((id(orig_verts[0]), id(orig_verts[1]))))]
                m12 = edge_midpoint_map[tuple(sorted((id(orig_verts[1]), id(orig_verts[2]))))]
                m20 = edge_midpoint_map[tuple(sorted((id(orig_verts[2]), id(orig_verts[0]))))]
                f1 = Face([v0, m01, m20], sid)
                f2 = Face([v1, m12, m01], sid)
                f3 = Face([v2, m20, m12], sid)
                f4 = Face([m01, m12, m20], sid)
                new_faces.extend([f1, f2, f3, f4])
                edges_to_add = [(v0, m01), (m01, m20), (m20, v0), (v1, m12), (m12, m01), (m01, v1), (v2, m20), (m20, m12), (m12, v2), (m01, m12), (m12, m20), (m20, m01)]
                for v_a, v_b in edges_to_add: new_edges_set.add(tuple(sorted((id(v_a), id(v_b)))))

        vertex_id_map = {id(v): v for v in new_vertices}
        new_edges = []
        for id1, id2 in new_edges_set:
            if id1 in vertex_id_map and id2 in vertex_id_map:
                new_edges.append(Edge(vertex_id_map[id1], vertex_id_map[id2]))

        return new_vertices, new_edges, new_faces      


    @staticmethod
    def smooth_vertices(vertices:list[Vertex], edges:list[Edge], faces:list[Face]) -> list[Vertex]:...

    @staticmethod
    def calculate_subdivision(vertices:list[Vertex], edges:list[Edge], faces:list[Face]) -> tuple[list[Vertex], list[Edge], list[Face]]:
        new_vertices, new_edges, new_faces = Mesh.split_geometry(vertices, edges, faces)

        return new_vertices, new_edges, new_faces
    
