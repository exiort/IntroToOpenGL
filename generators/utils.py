# CENG 487 Assignment2 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from geometry import Vertex, Edge, Face
import math



def merge_geometry_parts(geometry_parts:list[tuple[list[Vertex], list[Face]]], tolerance:float = 1e-6) -> tuple[list[Vertex], list[Edge], list[Face]]:
    final_vertices:list[Vertex] = []
    final_edges_set:set[tuple[int, ...]] = set()
    final_faces:list[Face] = []

    merged_vertices_map: dict[tuple[float, float, float], Vertex] = {}

    old_to_new_vertex_map: dict[int, Vertex] = {}

    ndigits = int(-math.log10(tolerance))
    for vertices, _ in geometry_parts:
        for v_old in vertices:
            pos = v_old.position
            pos_key = (
                round(pos.x, ndigits),
                round(pos.y, ndigits),
                round(pos.z, ndigits)
            )

            if pos_key not in merged_vertices_map:
                v_new = Vertex(pos.copy())
                final_vertices.append(v_new)
                merged_vertices_map[pos_key] = v_new
                old_to_new_vertex_map[id(v_old)] = v_new
            else:
                v_new = merged_vertices_map[pos_key]
                old_to_new_vertex_map[id(v_old)] = v_new

    for _, faces in geometry_parts:
        for f_old in faces:
            new_face_vertices = []
            is_valid_face = True
            for v_old in f_old.vertices:
                if id(v_old) in old_to_new_vertex_map:
                    v_new = old_to_new_vertex_map[id(v_old)]
                    new_face_vertices.append(v_new)
                else:
                    is_valid_face = False
                    break

            if is_valid_face and len(new_face_vertices) >= 3:
                new_face = Face(new_face_vertices, f_old.surface_id)
                final_faces.append(new_face)

                num_vertices = len(new_face_vertices)
                for i in range(num_vertices):
                    v1 = new_face_vertices[i]
                    v2 = new_face_vertices[(i + 1) % num_vertices]
                    edge_key = tuple(sorted((id(v1), id(v2))))
                    final_edges_set.add(edge_key)

    vertex_id_map = {id(v): v for v in final_vertices}
    final_edges:list[Edge] = []
    for id1, id2 in final_edges_set:
        if id1 in vertex_id_map and id2 in vertex_id_map:
            final_edges.append(Edge(vertex_id_map[id1], vertex_id_map[id2]))

    return final_vertices, final_edges, final_faces
