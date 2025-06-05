# CENG 487 Assignment4 by
# Bugrahan Imal
# StudentId: 280201012
# May 2025
from math3d import Vec4D, Vec3D, Vec2D
from geometry import Vertex, VertexAttributes, Face, Mesh, edge_extractor
from object3d import Object3D
from shaders import Shader
import math



def _create_square_geometry(size:float = 2, normal:Vec3D|None=None, color:Vec4D|None=None) -> tuple[list[Vertex], list[Face]]:
    if normal is None:
        normal = Vec3D(0, 0, 1, 0)
    if color is None:
        color = Vec4D(0.3, 0.3, 0, 1)
        
    h = size / 2

    vertices = [
        Vertex(Vec3D(-h, -h, 0)),
        Vertex(Vec3D(h, -h, 0)),
        Vertex(Vec3D(h, h, 0)),
        Vertex(Vec3D(-h, h, 0))
    ]
    attributes = [
        VertexAttributes(normal, Vec2D(0, 0), color),
        VertexAttributes(normal, Vec2D(1, 0), color),
        VertexAttributes(normal, Vec2D(1, 1), color),
        VertexAttributes(normal, Vec2D(0, 1), color)
    ]

    faces = [Face([(vertices[0], attributes[0]), (vertices[1], attributes[1]), (vertices[2], attributes[2]), (vertices[3], attributes[3])], 0)]

    return vertices, faces

def create_square_object(shader:Shader, name:str="Square", size:float=2) -> Object3D:
    vertices, faces = _create_square_geometry(size)
    edges = edge_extractor(vertices, faces)
    mesh = Mesh(name, vertices, edges, faces)
    obj = Object3D(shader, name, mesh)

    return obj

def _create_triangle_geometry(normal:Vec3D|None=None, color:Vec4D|None=None) -> tuple[list[Vertex], list[Face]]:
    if normal is None:
        normal = Vec3D(0, 0, 1, 0)
    if color is None:
        color = Vec4D(0.3, 0.3, 0, 1)
        
    vertices = [
        Vertex(Vec3D(0, 1, 0)),
        Vertex(Vec3D(-math.sqrt(3)/2, -0.5, 0)),
        Vertex(Vec3D(math.sqrt(3)/2, -0.5, 0))
    ]
    
    attributes = [
        VertexAttributes(normal, Vec2D(0.5, 1), color),
        VertexAttributes(normal, Vec2D(0, 0), color),
        VertexAttributes(normal, Vec2D(1, 1), color)
    ]
    
    faces = [Face([(vertices[0], attributes[0]), (vertices[1], attributes[1]), (vertices[2], attributes[2])], 0)]

    return vertices, faces

def create_triangle_object(shader:Shader, name:str="Triangle") -> Object3D:
    vertices, faces = _create_triangle_geometry()
    edges = edge_extractor(vertices, faces)
    mesh = Mesh(name, vertices, edges, faces)
    obj = Object3D(shader, name, mesh)

    return obj 
    
def _create_disk_geometry(radius:float=1, segments:int=16, normal:Vec3D|None=None, color:Vec4D|None=None) -> tuple[list[Vertex], list[Face]]:
    if segments < 3:
        segments = 3
    if normal is None:
        normal = Vec3D(0, 0, 1, 0)
    if color is None:
        color = Vec4D(0.3, 0.3, 0, 1)
        
    vertices:list[Vertex] = []
    attributes:list[VertexAttributes] = []
    faces:list[Face] = []

    v_center = Vertex(Vec3D(0, 0, 0))
    a_center = VertexAttributes(normal, Vec2D(0.5, 0.5), color)
    vertices.append(v_center)
    attributes.append(a_center)
    
    angle_step = 2 * math.pi / segments

    for i in range(segments):
        angle = i * angle_step
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        u = (math.cos(angle) +  1) / 2
        v = (math.sin(angle) + 1) / 2
        vertices.append((Vertex(Vec3D(x, y, 0))))
        attributes.append(VertexAttributes(normal, Vec2D(u, v), color))
        
    for i in range(segments):
        crr_idx = i + 1
        next_idx = ((i + 1) % segments) + 1

        v_crr = vertices[crr_idx]
        a_crr = attributes[crr_idx]
        v_next = vertices[next_idx]
        a_next = attributes[next_idx]
        
        faces.append(Face([(v_center, a_center), (v_crr, a_crr), (v_next, a_next)], 0))

    return vertices, faces

def create_disk_object(shader:Shader, name:str="Disk", radius:float=1, segments:int=16) -> Object3D:
    vertices, faces = _create_disk_geometry(radius, segments)
    edges = edge_extractor(vertices, faces)
    mesh = Mesh(name, vertices, edges, faces)
    obj = Object3D(shader, name, mesh)

    return obj

