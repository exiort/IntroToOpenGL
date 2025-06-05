# CENG 487 Assignment4 by
# Bugrahan Imal
# StudentId: 280201012
# May 2025
from shaders import Shader
from math3d import Vec3D, Vec2D, Vec4D
from geometry import Vertex, VertexAttributes, Face, Mesh, edge_extractor, calculate_face_normal
from object3d import Object3D
import math


def _create_box_geometry(size_x:float=1, size_y:float=1, size_z:float=1, color:Vec4D|None=None) -> tuple[list[Vertex], list[Face]]:
    if color is None:
        color = Vec4D(0.4, 0.4, 0.4, 1)
        
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
    normals = [
        Vec3D( 0,  0, -1, 0),
        Vec3D( 0,  0,  1, 0),
        Vec3D( 0,  1,  0, 0),
        Vec3D( 0, -1,  0, 0),
        Vec3D( 1,  0,  0, 0),
        Vec3D(-1,  0,  0, 0)
    ]
    uvs = [
        Vec2D(0.0, 0.0),
        Vec2D(1.0, 0.0),
        Vec2D(1.0, 1.0),
        Vec2D(0.0, 1.0)
    ]
    
    faces = [
        Face([(vertices[0], VertexAttributes(normals[0], uvs[0], color)),
              (vertices[1], VertexAttributes(normals[0], uvs[1], color)),
              (vertices[2], VertexAttributes(normals[0], uvs[2], color)),
              (vertices[3], VertexAttributes(normals[0], uvs[3], color))],
             0),
        Face([(vertices[4], VertexAttributes(normals[1], uvs[0], color)),
              (vertices[7], VertexAttributes(normals[1], uvs[1], color)),
              (vertices[6], VertexAttributes(normals[1], uvs[2], color)),
              (vertices[5], VertexAttributes(normals[1], uvs[3], color))],
             1),
        Face([(vertices[3], VertexAttributes(normals[2], uvs[0], color)),
              (vertices[2], VertexAttributes(normals[2], uvs[1], color)),
              (vertices[6], VertexAttributes(normals[2], uvs[2], color)),
              (vertices[7], VertexAttributes(normals[2], uvs[3], color))],
             2),
        Face([(vertices[1], VertexAttributes(normals[3], uvs[0], color)),
              (vertices[0], VertexAttributes(normals[3], uvs[1], color)),
              (vertices[4], VertexAttributes(normals[3], uvs[2], color)),
              (vertices[5], VertexAttributes(normals[3], uvs[3], color))],
             3),
        Face([(vertices[2], VertexAttributes(normals[4], uvs[0], color)),
              (vertices[1], VertexAttributes(normals[4], uvs[1], color)),
              (vertices[5], VertexAttributes(normals[4], uvs[2], color)),
              (vertices[6], VertexAttributes(normals[4], uvs[3], color))],
             4),
        Face([(vertices[0], VertexAttributes(normals[5], uvs[0], color)),
              (vertices[3], VertexAttributes(normals[5], uvs[1], color)),
              (vertices[7], VertexAttributes(normals[5], uvs[2], color)),
              (vertices[4], VertexAttributes(normals[5], uvs[3], color))],
             5),
    ]

    return vertices, faces

def create_box_object(shader:Shader, name:str="Box", size_x:float=1, size_y:float=1, size_z:float=1) -> Object3D:
    vertices, faces = _create_box_geometry(size_x, size_y, size_z)
    edges = edge_extractor(vertices, faces)
    mesh = Mesh(name, vertices, edges, faces)
    obj = Object3D(shader, name, mesh)

    return obj

def _create_cylinder_geometry(radius:float=1, height:float=2, segments:int=16, color:Vec4D|None=None) -> tuple[list[Vertex], list[Face]]:
    if segments < 3:
        segments = 3
    if color is None:
        color = Vec4D(0.75, 0.75, 0.75, 1)

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
    bottom_normal = Vec3D(0, 0, -1, 0)
    for i in range(segments):
        v_crr_idx = bottom_idx_start + i
        v_next_idx = bottom_idx_start + ((i + 1) % segments)

        v_crr = vertices[v_crr_idx]
        v_next = vertices[v_next_idx]
        
        center_uv = Vec2D(0.5, 0.5)
        crr_uv = Vec2D(0.5 + 0.5 * math.cos(i * angle_step), 0.5 + 0.5 * math.sin(i * angle_step))
        next_uv = Vec2D(0.5 + 0.5 * math.cos(((i + 1) % segments) * angle_step), 0.5 + 0.5 * math.sin(((i + 1) % segments) * angle_step))
        
        faces.append(Face([
            (v_bottom, VertexAttributes(bottom_normal, center_uv, color)),
            (v_next, VertexAttributes(bottom_normal, next_uv, color)),
            (v_crr, VertexAttributes(bottom_normal, crr_uv, color))
        ], 0))

    top_center_idx = bottom_idx_start + segments
    v_top = vertices[top_center_idx]
    top_normal = Vec3D(0, 0, 1, 0)
    for i in range(segments):
        v_crr_idx = top_idx_start + i
        v_next_idx = top_idx_start + ((i + 1) % segments)

        v_crr = vertices[v_crr_idx]
        v_next = vertices[v_next_idx]

        center_uv = Vec2D(0.5, 0.5)
        crr_uv = Vec2D(0.5 + 0.5 * math.cos(i * angle_step), 0.5 + 0.5 * math.sin(i * angle_step))
        next_uv = Vec2D(0.5 + 0.5 * math.cos(((i + 1) % segments) * angle_step), 0.5 + 0.5 * math.sin(((i + 1) % segments) * angle_step))

        faces.append(Face([
            (v_top, VertexAttributes(top_normal, center_uv, color)),
            (v_crr, VertexAttributes(top_normal, crr_uv, color)),
            (v_next, VertexAttributes(top_normal, next_uv, color))
        ], 1))

    for i in range(segments):
        idx_bl = bottom_idx_start + i
        idx_br = bottom_idx_start + ((i + 1) % segments)
        idx_tr = top_idx_start + ((i + 1) % segments)
        idx_tl = top_idx_start + i

        angle = i * angle_step
        normal = Vec3D(math.cos(angle), math.sin(angle), 0, 0)
        
        u_left = i / segments
        u_right = (i + 1) / segments
        
        faces.append(Face([
            (vertices[idx_bl], VertexAttributes(normal, Vec2D(u_left, 0.0), color)),
            (vertices[idx_br], VertexAttributes(normal, Vec2D(u_right, 0.0), color)),
            (vertices[idx_tr], VertexAttributes(normal, Vec2D(u_right, 1.0), color)),
            (vertices[idx_tl], VertexAttributes(normal, Vec2D(u_left, 1.0), color))
        ], 2))

    return vertices, faces

def create_cylinder_object(shader:Shader, name:str="Cylinder", radius:float=1, height:float=2, segments:int=16) -> Object3D:
    vertices, faces = _create_cylinder_geometry(radius, height, segments)
    edges = edge_extractor(vertices, faces)
    mesh = Mesh(name, vertices, edges, faces)
    obj = Object3D(shader, name, mesh)

    return obj

def _create_pyramid_geometry(base_size_x:float=2, base_size_y:float=2, height:float=2, color:Vec4D|None=None) -> tuple[list[Vertex], list[Face]]:
    if color is None:
        color = Vec4D(0.75, 0.75, 0.75, 1)
        
    hx = base_size_x / 2
    hy = base_size_y / 2

    vertices = [
        Vertex(Vec3D(-hx, -hy, -height/4)),
        Vertex(Vec3D(hx, -hy, -height/4)), 
        Vertex(Vec3D(hx, hy, -height/4)),
        Vertex(Vec3D(-hx, hy, -height/4)), 
        Vertex(Vec3D(0, 0, (3/4)*height)) 
    ]

    base_normal = Vec3D(0, 0, -1, 0)
    
    
    side_normal_1 = calculate_face_normal(vertices[3].position, vertices[2].position, vertices[4].position)
    side_normal_2 = calculate_face_normal(vertices[1].position, vertices[0].position, vertices[4].position)
    side_normal_3 = calculate_face_normal(vertices[2].position, vertices[1].position, vertices[4].position)
    side_normal_4 = calculate_face_normal(vertices[0].position, vertices[3].position, vertices[4].position)

    faces = [
        Face([
            (vertices[0], VertexAttributes(base_normal, Vec2D(0.0, 0.0), color)),
            (vertices[1], VertexAttributes(base_normal, Vec2D(1.0, 0.0), color)),
            (vertices[2], VertexAttributes(base_normal, Vec2D(1.0, 1.0), color)),
            (vertices[3], VertexAttributes(base_normal, Vec2D(0.0, 1.0), color))
        ], 0),
        
        Face([
            (vertices[3], VertexAttributes(side_normal_1, Vec2D(0.0, 0.0), color)),
            (vertices[2], VertexAttributes(side_normal_1, Vec2D(1.0, 0.0), color)),
            (vertices[4], VertexAttributes(side_normal_1, Vec2D(0.5, 1.0), color))
        ], 1),
        
        Face([
            (vertices[1], VertexAttributes(side_normal_2, Vec2D(0.0, 0.0), color)),
            (vertices[0], VertexAttributes(side_normal_2, Vec2D(1.0, 0.0), color)),
            (vertices[4], VertexAttributes(side_normal_2, Vec2D(0.5, 1.0), color))
        ], 2),
        
        Face([
            (vertices[2], VertexAttributes(side_normal_3, Vec2D(0.0, 0.0), color)),
            (vertices[1], VertexAttributes(side_normal_3, Vec2D(1.0, 0.0), color)),
            (vertices[4], VertexAttributes(side_normal_3, Vec2D(0.5, 1.0), color))
        ], 3),
        
        Face([
            (vertices[0], VertexAttributes(side_normal_4, Vec2D(0.0, 0.0), color)),
            (vertices[3], VertexAttributes(side_normal_4, Vec2D(1.0, 0.0), color)),
            (vertices[4], VertexAttributes(side_normal_4, Vec2D(0.5, 1.0), color))
        ], 4)
    ]

    return vertices, faces

def create_pyramid_object(shader:Shader, name:str="Pyramid", base_size_x:float=2, base_size_y:float=2, height:float=2) -> Object3D:
    vertices, faces = _create_pyramid_geometry(base_size_x, base_size_y, height)
    edges = edge_extractor(vertices, faces)
    mesh = Mesh(name, vertices, edges, faces)
    obj = Object3D(shader, name, mesh)

    return obj

def _create_sphere_geometry(radius:float=1, segments:int=16, rings:int=8, color:Vec4D|None=None) -> tuple[list[Vertex], list[Face]]:
    if segments < 3:
        segments = 3
    if rings < 2:
        rings = 2
    if color is None:
        color = Vec4D(0.75, 0.75, 0.75, 1)

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
        
        normal_north = vertices[north_pole_idx].position.vectorize().normalize()
        normal_v1 = vertices[v1_idx].position.vectorize().normalize()
        normal_v2 = vertices[v2_idx].position.vectorize().normalize()
        
        u1 = i / segments
        u2 = (i + 1) / segments
        
        faces.append(Face([
            (vertices[north_pole_idx], VertexAttributes(Vec3D(normal_north.x, normal_north.y, normal_north.z, 0), Vec2D(u1 + 0.5/segments, 1.0), color)),
            (vertices[v2_idx], VertexAttributes(Vec3D(normal_v2.x, normal_v2.y, normal_v2.z, 0), Vec2D(u2, 1.0 - 1.0/rings), color)),
            (vertices[v1_idx], VertexAttributes(Vec3D(normal_v1.x, normal_v1.y, normal_v1.z, 0), Vec2D(u1, 1.0 - 1.0/rings), color))
        ], 0))

    for i in range(rings - 2):
        ring_start_idx1 = 2 + i * segments
        ring_start_idx2 = 2 + (i + 1) * segments

        for j in range(segments):
            v1 = vertices[ring_start_idx1 + j]
            v2 = vertices[ring_start_idx1 + ((j + 1) % segments)]
            v3 = vertices[ring_start_idx2 + ((j + 1) % segments)]
            v4 = vertices[ring_start_idx2 + j]
            
            normal_v1 = v1.position.vectorize().normalize()
            normal_v2 = v2.position.vectorize().normalize()
            normal_v3 = v3.position.vectorize().normalize()
            normal_v4 = v4.position.vectorize().normalize()
            
            u_left = j / segments
            u_right = (j + 1) / segments
            v_top = 1.0 - (i + 1) / rings
            v_bottom = 1.0 - (i + 2) / rings
            
            faces.append(Face([
                (v1, VertexAttributes(Vec3D(normal_v1.x, normal_v1.y, normal_v1.z, 0), Vec2D(u_left, v_top), color)),
                (v2, VertexAttributes(Vec3D(normal_v2.x, normal_v2.y, normal_v2.z, 0), Vec2D(u_right, v_top), color)),
                (v3, VertexAttributes(Vec3D(normal_v3.x, normal_v3.y, normal_v3.z, 0), Vec2D(u_right, v_bottom), color)),
                (v4, VertexAttributes(Vec3D(normal_v4.x, normal_v4.y, normal_v4.z, 0), Vec2D(u_left, v_bottom), color))
            ], 0))

    south_pole_idx = 1
    ring_start_idx = 2 + (rings - 2) * segments
    for i in range(segments):
        v1_idx = ring_start_idx + i
        v2_idx = ring_start_idx + ((i + 1) % segments)
        
        normal_south = vertices[south_pole_idx].position.vectorize().normalize()
        normal_v1 = vertices[v1_idx].position.vectorize().normalize()
        normal_v2 = vertices[v2_idx].position.vectorize().normalize()
        
        u1 = i / segments
        u2 = (i + 1) / segments
        
        faces.append(Face([
            (vertices[south_pole_idx], VertexAttributes(Vec3D(normal_south.x, normal_south.y, normal_south.z, 0), Vec2D(u1 + 0.5/segments, 0.0), color)),
            (vertices[v1_idx], VertexAttributes(Vec3D(normal_v1.x, normal_v1.y, normal_v1.z, 0), Vec2D(u1, 1.0/rings), color)),
            (vertices[v2_idx], VertexAttributes(Vec3D(normal_v2.x, normal_v2.y, normal_v2.z, 0), Vec2D(u2, 1.0/rings), color))
        ], 0))

    return vertices, faces

def create_sphere_object(shader:Shader, name:str="Sphere", radius:float=1, segments:int=16, rings:int=8) -> Object3D:
    vertices, faces = _create_sphere_geometry(radius, segments, rings)
    edges = edge_extractor(vertices, faces)
    mesh = Mesh(name, vertices, edges, faces)
    obj = Object3D(shader, name, mesh)

    return obj

def _create_torus_geometry(outside_radius:float=4, inside_radius:float=1, outside_segments:int=24, inside_segments:int=12, color:Vec4D|None=None) -> tuple[list[Vertex], list[Face]]:
    if inside_segments < 3:
        inside_segments = 3
    if outside_segments < 3:
        outside_segments = 3
    if color is None:
        color = Vec4D(0.75, 0.75, 0.75, 1)

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
            v3_idx = ((i + 1) % outside_segments) * inside_segments + ((j + 1) % inside_segments)
            v4_idx = i * inside_segments + ((j + 1) % inside_segments)
            
            def calculate_torus_normal(outer_idx, inner_idx):
                phi = 2 * math.pi * (outer_idx / outside_segments)
                theta = 2 * math.pi * (inner_idx / inside_segments)
    
                cos_phi = math.cos(phi)
                sin_phi = math.sin(phi)
                cos_theta = math.cos(theta)
                sin_theta = math.sin(theta)
    
                nx = cos_theta * cos_phi
                ny = cos_theta * sin_phi
                nz = sin_theta
                
                return Vec3D(nx, ny, nz, 0)

            normal_v1 = calculate_torus_normal(i, j)
            normal_v2 = calculate_torus_normal((i + 1) % outside_segments, j)
            normal_v3 = calculate_torus_normal((i + 1) % outside_segments, (j + 1) % inside_segments)
            normal_v4 = calculate_torus_normal(i, (j + 1) % inside_segments)
            
            u1 = i / outside_segments
            u2 = (i + 1) / outside_segments
            v1 = j / inside_segments
            v2 = (j + 1) / inside_segments
            
            faces.append(Face([
                (vertices[v1_idx], VertexAttributes(normal_v1, Vec2D(u1, v1), color)),
                (vertices[v2_idx], VertexAttributes(normal_v2, Vec2D(u2, v1), color)),
                (vertices[v3_idx], VertexAttributes(normal_v3, Vec2D(u2, v2), color)),
                (vertices[v4_idx], VertexAttributes(normal_v4, Vec2D(u1, v2), color))
            ], 0))

    return vertices, faces

def create_torus_object(shader:Shader, name:str="Torus", outside_radius:float=4, inside_radius:float=1, outside_segments:int=24, inside_segments:int=12) -> Object3D:
    vertices, faces = _create_torus_geometry(outside_radius, inside_radius, outside_segments, inside_segments)
    edges = edge_extractor(vertices, faces)
    mesh = Mesh(name, vertices, edges, faces)
    obj = Object3D(shader, name, mesh)

    return obj

def _create_tetrahedron_geometry(size:float=1, color:Vec4D|None=None) -> tuple[list[Vertex], list[Face]]:
    if color is None:
        color = Vec4D(0.75, 0.75, 0.75, 1)
        
    vertices:list[Vertex] = [
        Vertex(Vec3D(size, size, size)),
        Vertex(Vec3D(size, -size, -size)), 
        Vertex(Vec3D(-size, size, -size)), 
        Vertex(Vec3D(-size, -size, size)) 
    ]
    
    normal_0 = calculate_face_normal(vertices[0].position, vertices[2].position, vertices[1].position)
    normal_1 = calculate_face_normal(vertices[0].position, vertices[1].position, vertices[3].position)
    normal_2 = calculate_face_normal(vertices[0].position, vertices[3].position, vertices[2].position)
    normal_3 = calculate_face_normal(vertices[1].position, vertices[2].position, vertices[3].position)
    
    faces:list[Face] = [
        Face([
            (vertices[0], VertexAttributes(normal_0, Vec2D(0.5, 1.0), color)),
            (vertices[2], VertexAttributes(normal_0, Vec2D(0.0, 0.0), color)),
            (vertices[1], VertexAttributes(normal_0, Vec2D(1.0, 0.0), color))
        ], 0),
        
        Face([
            (vertices[0], VertexAttributes(normal_1, Vec2D(0.5, 1.0), color)),
            (vertices[1], VertexAttributes(normal_1, Vec2D(0.0, 0.0), color)),
            (vertices[3], VertexAttributes(normal_1, Vec2D(1.0, 0.0), color))
        ], 1),
        
        Face([
            (vertices[0], VertexAttributes(normal_2, Vec2D(0.5, 1.0), color)),
            (vertices[3], VertexAttributes(normal_2, Vec2D(0.0, 0.0), color)),
            (vertices[2], VertexAttributes(normal_2, Vec2D(1.0, 0.0), color))
        ], 2),
        
        Face([
            (vertices[1], VertexAttributes(normal_3, Vec2D(0.0, 1.0), color)),
            (vertices[2], VertexAttributes(normal_3, Vec2D(1.0, 1.0), color)),
            (vertices[3], VertexAttributes(normal_3, Vec2D(0.5, 0.0), color))
        ], 3)
    ]

    return vertices, faces

def create_tetrahedron_object(shader:Shader, name:str="Tetrahedron", size:float=1) -> Object3D:
    vertices, faces = _create_tetrahedron_geometry(size)
    edges = edge_extractor(vertices, faces)
    mesh = Mesh(name, vertices, edges, faces)
    obj = Object3D(shader, name, mesh)

    return obj
