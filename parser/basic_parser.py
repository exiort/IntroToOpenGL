# CENG 487 Assignment3 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025
from math3d import Vec3D, Vec2D, Vec4D
from geometry import Vertex, VertexAttributes, Face, Mesh, edge_extractor
from shaders import Shader
from object3d import Object3D
from .utils import reorient_object

def parse_file(filepath:str, shader: Shader, source_up:Vec3D, source_fwd:Vec3D) -> Object3D | None:
    if not filepath.endswith(".obj"):
        print(f"Error: Invalid file format: {filepath[-4:]}")
        return None
    
    file_vertices: list[Vec3D] = []
    file_uvs: list[Vec2D] = []
    file_normals: list[Vec3D] = []

    mesh_faces: list[Face] = []
    
    vertex_cache: dict[str, tuple[Vertex, VertexAttributes]] = {}

    object_name = ""
    try:
        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith('#'):
                    continue

                parts = line.split()
                command = parts[0]

                if command == "o":
                    object_name = parts[1]
                elif command == "v":
                    file_vertices.append(Vec3D(float(parts[1]), float(parts[2]), float(parts[3])))
                elif command == "vt":
                    file_uvs.append(Vec2D(float(parts[1]), float(parts[2])))
                elif command == "vn":
                    file_normals.append(Vec3D(float(parts[1]), float(parts[2]), float(parts[3]), w=0))
                elif command == "f":
                    face_vertex_tuples: list[tuple[Vertex, VertexAttributes]] = []
                    for v_def in parts[1:]:
                        if v_def in vertex_cache:
                            face_vertex_tuples.append(vertex_cache[v_def])
                        else:
                            v_indices = v_def.split('/')
                            pos_idx = int(v_indices[0]) - 1
                            uv_idx = int(v_indices[1]) - 1
                            norm_idx = int(v_indices[2]) - 1

                            vertex_pos = file_vertices[pos_idx]
                            vertex_uv = file_uvs[uv_idx]
                            vertex_normal = file_normals[norm_idx]
                            
                            vertex_obj = Vertex(vertex_pos)
                            attrib_obj = VertexAttributes(vertex_normal, vertex_uv, Vec4D(1.0, 1.0, 1.0, 1.0))
                            
                            new_tuple = (vertex_obj, attrib_obj)
                            vertex_cache[v_def] = new_tuple
                            face_vertex_tuples.append(new_tuple)
                    
                    if len(face_vertex_tuples) >= 3:
                        mesh_faces.append(Face(face_vertex_tuples, len(mesh_faces)))
                        
    except Exception as e:
        print(f"Error parsing file: {e}")
        return None

    all_used_vertices = list(set([vt[0] for vt in vertex_cache.values()]))
    edges = edge_extractor(all_used_vertices, mesh_faces) 
    
    mesh = Mesh(object_name, vertices=all_used_vertices, edges=edges, faces=mesh_faces)
    obj = Object3D(shader, object_name, mesh)

    reorient_object(obj, source_up, source_fwd)
    return obj
