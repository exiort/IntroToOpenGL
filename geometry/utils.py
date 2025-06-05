# CENG 487 Assignment4 by
# Bugrahan Imal
# StudentId: 280201012
# May 2025
from .vertex import Vertex
from .edge import Edge
from .face import Face
from math3d import Vec3D


def edge_extractor(vertices:list[Vertex], faces:list[Face]) -> list[Edge]:
    edges:list[Edge] = []
    edge_keys:set[tuple[int,...]] = set()
    for face in faces:
        v_count = len(face.vertices)
        for i in range(v_count):
            v1 = face.vertices[i][0]
            v2 = face.vertices[(i+1)%v_count][0]

            key = tuple(sorted((id(v1), id(v2))))
            edge_keys.add(key)

    vertex_id_map:dict[int, Vertex] = {id(v): v for v in vertices}
        
    for vid1, vid2 in edge_keys:
        v1 = vertex_id_map.get(vid1)
        v2 = vertex_id_map.get(vid2)

        if v1 is not None and v2 is not None:
            edges.append(Edge(v1, v2))

    return edges

def calculate_face_normal(v1:Vec3D, v2:Vec3D, v3:Vec3D):
    edge1 = v2 - v1
    edge2 = v3 - v1
    normal = edge1.cross(edge2).normalize()
    return Vec3D(normal.x, normal.y, normal.z, 0)

