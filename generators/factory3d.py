# CENG 487 Assignment4 by
# Bugrahan Imal
# StudentId: 280201012
# May 2025
from math3d import Vec3D
from geometry import Vertex, Face, Mesh, edge_extractor
from object3d import Object3D
import math


def _create_box_geometry(size_x:float=1, size_y:float=1, size_z:float=1) -> tuple[list[Vertex], list[Face]]:
    hx, hy, hz = size_x/2, size_y/2, size_z/2

    vertices = [
        Vertex(Vec3D(-hx, -hy, -hz)),
        Vertex(Vec3D( hx, -hy, -hz)),
        Vertex(Vec3D( hx,  hy, -hz)),
        Vertex(Vec3D(-hx,  hy, -hz)),
        
        Vertex(Vec3D(-hx, -hy,  hz)),
        Vertex(Vec3D( hx, -hy,  hz)),
        Vertex(Vec3D( hx,  hy,  hz)),
        Vertex(Vec3D(-hx,  hy,  hz))
    ]

    faces = [
        Face([vertices[0], vertices[1], vertices[2], vertices[3]], 0),
        Face([vertices[4], vertices[7], vertices[6], vertices[5]], 1),
        Face([vertices[3], vertices[2], vertices[6], vertices[7]], 2),
        Face([vertices[1], vertices[0], vertices[4], vertices[5]], 3),
        Face([vertices[2], vertices[1], vertices[5], vertices[6]], 4),
        Face([vertices[0], vertices[3], vertices[7], vertices[4]], 5)
    ]

    return vertices, faces

def create_box_object(name:str="Box", size_x:float=1, size_y:float=1, size_z:float=1) -> Object3D:
    vertices, faces = _create_box_geometry(size_x, size_y, size_z)
    edges = edge_extractor(vertices, faces)
    mesh = Mesh(name, vertices, edges, faces)
    obj = Object3D(name, mesh)

    return obj

def _create_cylinder_geometry(radius:float=1, height:float=2, segments:int=16) -> tuple[list[Vertex], list[Face]]:
    if segments < 3:
        segments = 3

    vertices:list[Vertex] = []
    faces:list[Face] = []
    h = height / 2

    v_bottom_center = Vertex(Vec3D(0, 0, -h))
    vertices.append(v_bottom_center)
    bottom_idx_start = len(vertices)

    angle_step = 2 * math.pi / segments
    for i in range(segments):
        angle = i * angle_step
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        vertices.append(Vertex(Vec3D(x, y, -h)))

    v_top_center = Vertex(Vec3D(0, 0, h))
    vertices.append(v_top_center)
    top_idx_start = len(vertices)

    for i in range(segments):
        angle = i * angle_step
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        vertices.append(Vertex(Vec3D(x, y, h)))
    
    bottom_center_idx = 0
    v_bottom = vertices[bottom_center_idx]
    for i in range(segments):
        v_crr_idx = bottom_idx_start + i
        v_next_idx = bottom_idx_start + ((i + 1) % segments)

        v_crr = vertices[v_crr_idx]
        v_next = vertices[v_next_idx]
        
        faces.append(Face([v_bottom, v_next, v_crr], 0))

    top_center_idx = bottom_idx_start + segments
    v_top = vertices[top_center_idx]
    for i in range(segments):
        v_crr_idx = top_idx_start + i
        v_next_idx = top_idx_start + ((i + 1) % segments)

        v_crr = vertices[v_crr_idx]
        v_next = vertices[v_next_idx]

        faces.append(Face([v_top, v_crr, v_next], 1))

    for i in range(segments):
        idx_bl = bottom_idx_start + i
        idx_br = bottom_idx_start + ((i + 1) % segments)
        idx_tr = top_idx_start + ((i + 1) % segments)
        idx_tl = top_idx_start + i

        faces.append(Face([vertices[idx_bl], vertices[idx_br], vertices[idx_tr], vertices[idx_tl]], 2))

    return vertices, faces

def create_cylinder_object(name:str="Cylinder", radius:float=1, height:float=2, segments:int=16) -> Object3D:
    vertices, faces = _create_cylinder_geometry(radius, height, segments)
    edges = edge_extractor(vertices, faces)
    mesh = Mesh(name, vertices, edges, faces)
    obj = Object3D(name, mesh)

    return obj

def _create_pyramid_geometry(base_size_x:float=2, base_size_y:float=2, height:float=2) -> tuple[list[Vertex], list[Face]]:
    hx = base_size_x / 2
    hy = base_size_y / 2

    vertices:list[Vertex] = []
    faces:list[Face] = []

    vertices = [
        Vertex(Vec3D(-hx, -hy, -height/4)),
        Vertex(Vec3D(hx, -hy, -height/4)),
        Vertex(Vec3D(hx, hy, -height/4)),
        Vertex(Vec3D(-hx, hy, -height/4)),
        Vertex(Vec3D(0, 0, (3/4)*height))
    ]

    faces = [
        Face([vertices[0], vertices[1], vertices[2], vertices[3]], 0),
        Face([vertices[3], vertices[2], vertices[4]], 1),
        Face([vertices[1], vertices[0], vertices[4]], 2),
        Face([vertices[2], vertices[1], vertices[4]], 3),
        Face([vertices[0], vertices[3], vertices[4]], 4)
    ]

    return vertices, faces

def create_pyramid_object(name:str="Pyramid", base_size_x:float=2, base_size_y:float=2, height:float=2) -> Object3D:
    vertices, faces = _create_pyramid_geometry(base_size_x, base_size_y, height)
    edges = edge_extractor(vertices, faces)
    mesh = Mesh(name, vertices, edges, faces)
    obj = Object3D(name, mesh)

    return obj

def _create_sphere_geometry(radius:float=1, segments:int=16, rings:int=8) -> tuple[list[Vertex], list[Face]]:
    if segments < 3:
        segments = 3
    if rings < 2:
        rings = 2

    vertices:list[Vertex] = []
    faces:list[Face] = []

    vertices.append(Vertex(Vec3D(0, 0, radius)))
    vertices.append(Vertex(Vec3D(0, 0, -radius)))

    angle_step = 2 * math.pi / segments 
    for i in range(1, rings):
        phi = math.pi * (i / rings)

        for j in range(segments):
            theta = j * angle_step
            x = radius * math.sin(phi) * math.cos(theta)
            y = radius * math.sin(phi) * math.sin(theta)
            z = radius * math.cos(phi)
            vertices.append(Vertex(Vec3D(x, y, z)))

    north_pole_idx = 0
    for i in range(segments):
        v1_idx = 2 + i
        v2_idx = 2 + ((i + 1) % segments)
        faces.append(Face([vertices[north_pole_idx], vertices[v2_idx], vertices[v1_idx]], 0))

    for i in range(rings - 2):
        ring_start_idx1 = 2 + i * segments
        ring_start_idx2 = 2 + (i + 1) * segments

        for j in range(segments):
            v1 = vertices[ring_start_idx1 + j]
            v2 = vertices[ring_start_idx1 + ((j + 1)) % segments]
            v3 = vertices[ring_start_idx2 + ((j + 1)) % segments]
            v4 = vertices[ring_start_idx2 + j]
            faces.append(Face([v1, v2, v3, v4], 0))

    south_pole_idx = 1
    ring_start_idx = 2 + (rings - 2) * segments
    for i in range(segments):
        v1_idx = ring_start_idx + i
        v2_idx = ring_start_idx + ((i + 1) % segments) 
        faces.append(Face([vertices[south_pole_idx], vertices[v1_idx], vertices[v2_idx]], 0))

    return vertices, faces

def create_sphere_object(name:str="Sphare", radius:float=1, segments:int=16, rings:int=8) -> Object3D:
    vertices, faces = _create_sphere_geometry(radius, segments, rings)
    edges = edge_extractor(vertices, faces)
    mesh = Mesh(name, vertices, edges, faces)
    obj = Object3D(name, mesh)

    return obj

def _create_torus_geometry(outside_radius:float=4, inside_radius:float=1, outside_segments:int=24, inside_segments:int=12) -> tuple[list[Vertex], list[Face]]:
    if inside_segments < 3:
        inside_segments = 3
    if outside_segments < 3:
        outside_segments = 3

    vertices:list[Vertex] = []
    faces:list[Face] = []

    for i in range(outside_segments):
        phi = 2 * math.pi * (i / outside_segments)
        cos_phi = math.cos(phi)
        sin_phi = math.sin(phi)

        for j in range(inside_segments):
            theta = 2 * math.pi * (j / inside_segments)
            cos_theta = math.cos(theta)
            sin_theta = math.sin(theta)

            x = (outside_radius + inside_radius * cos_theta) * cos_phi
            y = (outside_radius + inside_radius * cos_theta) * sin_phi
            z = inside_radius * sin_theta
            vertices.append(Vertex(Vec3D(x, y, z)))

    for i in range(outside_segments):
        for j in range(inside_segments):
            v1_idx = i * inside_segments + j
            v2_idx = ((i + 1) % outside_segments) * inside_segments + j
            v3_idx = ((i + 1) % outside_segments) *inside_segments + ((j + 1) % inside_segments)
            v4_idx = i * inside_segments + ((j + 1) % inside_segments)
            faces.append(Face([vertices[v1_idx], vertices[v2_idx], vertices[v3_idx], vertices[v4_idx]], 0))

    return vertices, faces

def create_torus_object(name:str="Torus", outside_radius:float=4, inside_radius:float=1, outside_segments:int=24, inside_segments:int=12) -> Object3D:
    vertices, faces = _create_torus_geometry(outside_radius, inside_radius, outside_segments, inside_segments)
    edges = edge_extractor(vertices, faces)
    mesh = Mesh(name, vertices, edges, faces)
    obj = Object3D(name, mesh)

    return obj

def _create_tetrahedron_geometry(size:float=1) -> tuple[list[Vertex], list[Face]]:
    vertices:list[Vertex] = [
        Vertex(Vec3D(size, size, size)),
        Vertex(Vec3D(size, -size, -size)),
        Vertex(Vec3D(-size, size, -size)),
        Vertex(Vec3D(-size, -size, size))
    ]
    faces:list[Face] = [
        Face([vertices[0], vertices[2], vertices[1]], 0),
        Face([vertices[0], vertices[1], vertices[3]], 1),
        Face([vertices[0], vertices[3], vertices[2]], 2),
        Face([vertices[1], vertices[2], vertices[3]], 3)
    ]

    return vertices, faces

def create_tetrahedron_object(name:str="Tetrahedron", size:float=1) -> Object3D:
    vertices, faces = _create_tetrahedron_geometry(size)
    edges = edge_extractor(vertices, faces)
    mesh = Mesh(name, vertices, edges, faces)
    obj = Object3D(name, mesh)

    return obj
    
