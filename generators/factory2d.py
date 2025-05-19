# CENG 487 Assignment4 by
# Bugrahan Imal
# StudentId: 280201012
# May 2025
from math3d import Vec3D
from geometry import Vertex, Face, Mesh, edge_extractor
from object3d import Object3D
import math



def _create_square_geometry(size:float = 2) -> tuple[list[Vertex], list[Face]]:
    h = size / 2
    vertices = [
        Vertex(Vec3D(-h, -h, 0)),
        Vertex(Vec3D(h, -h, 0)),
        Vertex(Vec3D(h, h, 0)),
        Vertex(Vec3D(-h, h, 0))
    ]

    faces = [Face([vertices[0], vertices[1], vertices[2], vertices[3]], 0)]

    return vertices, faces

def create_square_object(name:str="Square", size:float=2) -> Object3D:
    vertices, faces = _create_square_geometry(size)
    edges = edge_extractor(vertices, faces)
    mesh = Mesh(name, vertices, edges, faces)
    obj = Object3D(name, mesh)

    return obj

def _create_triangle_geometry() -> tuple[list[Vertex], list[Face]]:
    vertices = [
        Vertex(Vec3D(0, 1, 0)),
        Vertex(Vec3D(-math.sqrt(3)/2, -0.5, 0)),
        Vertex(Vec3D(math.sqrt(3)/2, -0.5, 0))
    ]

    faces = [Face([vertices[0], vertices[1], vertices[2]], 0)]

    return vertices, faces

def create_triangle_object(name:str="Triangle") -> Object3D:
    vertices, faces = _create_triangle_geometry()
    edges = edge_extractor(vertices, faces)
    mesh = Mesh(name, vertices, edges, faces)
    obj = Object3D(name, mesh)

    return obj 
    
def _create_disk_geometry(radius:float=1, segments:int=16) -> tuple[list[Vertex], list[Face]]:
    if segments < 3:
        segments = 3

    vertices:list[Vertex] = []
    faces:list[Face] = []

    v_center = Vertex(Vec3D(0, 0, 0))
    vertices.append(v_center)

    angle_step = 2 * math.pi / segments

    for i in range(segments):
        angle = i * angle_step
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        vertices.append(Vertex(Vec3D(x, y, 0)))
        
    for i in range(segments):
        v_crr_idx = i + 1
        v_next_idx = ((i + 1) % segments) + 1

        v_crr = vertices[v_crr_idx]
        v_next = vertices[v_next_idx]

        faces.append(Face([v_center, v_crr, v_next], 0))

    return vertices, faces

def create_disk_object(name:str="Disk", radius:float=1, segments:int=16) -> Object3D:
    vertices, faces = _create_disk_geometry(radius, segments)
    edges = edge_extractor(vertices, faces)
    mesh = Mesh(name, vertices, edges, faces)
    obj = Object3D(name, mesh)

    return obj

