# CENG 487 Assignment3 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from math3d import Vec3D
from geometry import Vertex, Face, Mesh, edge_extractor
from object3d import Object3D
from .utils import reorient_object



def parse_file(filepath:str, source_up:Vec3D, source_fwd:Vec3D) -> Object3D|None:
    if filepath[-4:] != ".obj":
        print(f"Error: Invalid file format:{filepath[-4:]}")
        return
    
    vertices:list[Vertex] = []
    faces:list[Face] = []

    face_idx = 0
    object_name = ""
    try:
        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith('#'):
                    continue

                splitted_line = line.split()
                command = splitted_line[0]

                if command == "o":
                    object_name = splitted_line[1]
                    
                if command == "v":
                    try:
                        position = Vec3D(float(splitted_line[1]), float(splitted_line[2]), float(splitted_line[3]))
                        vertices.append(Vertex(position))
                    except:
                        print(f"Warning: Could not parse vertex line:{line}")
                    
                elif command == "f":
                    try:
                        face_vertices:list[Vertex] = []

                        for v_idx in splitted_line[1:]:
                            face_vertices.append(vertices[int(v_idx) - 1])

                        if len(face_vertices) >= 3:
                            faces.append(Face(face_vertices, face_idx))
                            face_idx += 1
                        else:
                            print(f"Warning: Face with less than 3 vertices found:{line}")
                            
                    except:
                        print(f"Warning: Could not parse face line:{line}")
                        
    except:
        print("Error: Could not open file.")
        return 

    edges = edge_extractor(vertices, faces) 
    
    mesh = Mesh(object_name, vertices=vertices, edges=edges, faces=faces)
    obj =  Object3D(object_name, mesh)
    
    reorient_object(obj, source_up, source_fwd)
    return obj
