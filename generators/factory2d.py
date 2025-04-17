# CENG 487 Assignment1 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from .basefactory2d import create_base_square, create_base_triangle
from object3d.object3d import Object3D
from math3d import Mat3D, Vec3D
from geometry import Vertex, Edge, Face
import math



def create_triangle(
        name:str="Triangle",
        sx:float=1, sy:float=1, sz:float=1,
) -> Object3D:
    base_triangle = create_base_triangle(name)
    base_triangle.do_transform(Mat3D.scaling(sx, sy, sz))
    base_triangle.apply_transform()
    return base_triangle

def create_square(
        name:str="Square",
        sx:float=1, sy:float=1, sz:float=1
)-> Object3D:
    base_square = create_base_square(name)
    base_square.do_transform(Mat3D.scaling(sx, sy, sz))
    base_square.apply_transform()
    return base_square


def __create_oriented_quad(width:float, height:float, center:Vec3D, normal:Vec3D, up:Vec3D, surface_id:int) -> tuple[list[Vertex], list[Face]]:
    norm = normal.normalize()
    up_norm = up.normalize()

    #Gram-Schmidt
    right_norm = up_norm.cross(norm).normalize()
    up_norm = norm.cross(right_norm).normalize()

    hw = width / 2
    hh = height / 2

    right_vec = right_norm * hw
    up_vec = up_norm * hh
    
    position0 = center - right_vec - up_vec
    position1 = center +  right_vec - up_vec
    position2 = center + right_vec + up_vec
    position3 = center - right_vec + up_vec

    v0 = Vertex(position0)
    v1 = Vertex(position1)
    v2 = Vertex(position2)
    v3 = Vertex(position3)
    vertices = [v0, v1, v2, v3]

    face = Face(vertices, surface_id)

    return vertices, [face]

def __create_polygon_disk(radius:float, segments:int, center:Vec3D, normal:Vec3D, up:Vec3D, surface_id:int) -> tuple[list[Vertex], list[Face]]:

    disk_vertices:list[Vertex] = []
    disk_faces:list[Face] = []

    v_center = Vertex(center.copy())
    disk_vertices.append(v_center)

    norm = normal.normalize()
    up_norm = up.normalize()
    
    right_norm = up_norm.cross(norm).normalize()
    up_norm = norm.cross(right_norm).normalize()

    circle_vertices:list[Vertex] = []
    for i in range(segments):
        angle = (i / segments) * 2 * math.pi
        local_x = math.cos(angle) * radius
        local_y = math.sin(angle) * radius

        pos = center + (right_norm * local_x) + (up_norm * local_y)
        circle_vertices.append(Vertex(pos))

    disk_vertices.extend(circle_vertices)
    
    for i in range(segments):
        v_crr = circle_vertices[i]
        v_next = circle_vertices[(i + 1) % segments]

        face = Face([v_center, v_crr, v_next], surface_id)
        disk_faces.append(face)

    return disk_vertices, disk_faces
