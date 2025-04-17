# CENG 487 Assignment2 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from .utils import merge_geometry_parts
from .factory2d import __create_oriented_quad, __create_polygon_disk
from math3d import Vec3D
from geometry import Vertex, Face, Mesh
from object3d import Object3D



def create_box(name:str="Box", size_x:float=1, size_y:float=1, size_z:float=1) -> Object3D:
    hx = size_x / 2
    hy = size_y / 2
    hz = size_z / 2

    box_center_z = hz

    face_params = [
        {"width": size_x, "height": size_y, "center": Vec3D(0, 0, 0), "normal": Vec3D(0, 0, -1), "up": Vec3D(0, 1, 0), "surface_id": 0},
        {"width": size_x, "height": size_y, "center": Vec3D(0, 0, size_z), "normal": Vec3D(0, 0, 1), "up": Vec3D(0, 1, 0), "surface_id": 1},
        {"width": size_x, "height": size_z, "center": Vec3D(0, hy, box_center_z), "normal": Vec3D(0, 1, 0), "up": Vec3D(0, 0, 1), "surface_id": 2},
        {"width": size_x, "height": size_z, "center": Vec3D(0, -hy, box_center_z), "normal": Vec3D(0, -1, 0),"up": Vec3D(0, 0, 1), "surface_id": 3},
        {"width": size_y, "height": size_z, "center": Vec3D(-hx, 0, box_center_z), "normal": Vec3D(-1, 0, 0), "up": Vec3D(0, 0, 1), "surface_id": 4},
        {"width": size_y, "height": size_z, "center": Vec3D(hx, 0, box_center_z), "normal": Vec3D(1, 0, 0), "up": Vec3D(0, 0, 1), "surface_id": 5},
    ]
    geometry_parts_to_merge:list[tuple[list[Vertex], list[Face]]] = []

    for params in face_params:
        vertices, faces = __create_oriented_quad(
            params["width"], params["height"], params["center"], params["normal"], params["up"], params["surface_id"]
        )
        geometry_parts_to_merge.append((vertices, faces))

    final_vertices, final_edges, final_faces = merge_geometry_parts(geometry_parts_to_merge)
    mesh = Mesh(name, final_vertices, final_edges, final_faces)
    obj = Object3D(name, mesh)
    return obj
    

def create_cylinder(name:str="Cylinder", radius:float=0.5, height:float=1, segments:int=16) -> Object3D:
    geometry_parts_to_merge:list[tuple[list[Vertex], list[Face]]] = []

    up_for_caps = Vec3D(0, 1, 0)

    vertices_bot, faces_bot = __create_polygon_disk(radius, segments, Vec3D(0, 0, 0), Vec3D(0, 0, -1), up_for_caps, 0)
    geometry_parts_to_merge.append((vertices_bot, faces_bot))

    vertices_top, faces_top = __create_polygon_disk(radius, segments, Vec3D(0, 0, height), Vec3D(0, 0, 1), up_for_caps, 1)
    geometry_parts_to_merge.append((vertices_top, faces_top))

    bottom_circle_vertices = vertices_bot[1:]
    top_circle_vertices = vertices_top[1:]

    for i in range(segments):
        vb_curr = bottom_circle_vertices[i]
        vb_next = bottom_circle_vertices[(i + 1) % segments]
        vt_curr = top_circle_vertices[i]
        vt_next = top_circle_vertices[(i + 1) % segments]

        face = Face([vb_curr, vb_next, vt_next, vt_curr], 2)
        current_side_quad_vertices = [vb_curr, vb_next, vt_next, vt_curr]
        geometry_parts_to_merge.append((current_side_quad_vertices, [face]))
    
    final_vertices, final_edges, final_faces = merge_geometry_parts(geometry_parts_to_merge)
    
    print(geometry_parts_to_merge)
    mesh = Mesh(name, final_vertices, final_edges, final_faces)
    obj = Object3D(name, mesh)
    return obj
