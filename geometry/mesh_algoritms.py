# CENG 487 Assignment4 by
# Bugrahan Imal
# StudentId: 280201012
# May 2025
from .vertex import Vertex
from .edge import Edge
from .face import Face
from math3d import Vec3D



class MeshAlgorithms:
    @staticmethod
    def split_geometry(vertices:list[Vertex], edges:list[Edge], faces:list[Face]) -> tuple[list[Vertex], list[Edge], list[Face]]:
        new_vertices:list[Vertex] = []
        new_edges_set:set[tuple[int, ...]] = set()
        new_faces:list[Face] = []

        vertex_map:dict[Vertex, Vertex] = {}
        edge_midpoint_map:dict[tuple[int, ...], Vertex] = {}
        face_centroid_map:dict[Face, Vertex] = {}

        for v_orig in vertices:
            v_copy = v_orig.copy()
            new_vertices.append(v_copy)
            vertex_map[v_orig] = v_copy
        
        for edge in edges:
            v1_orig, v2_orig = edge.v1, edge.v2
            edge_key = tuple(sorted((id(v1_orig), id(v2_orig))))
            if edge_key not in edge_midpoint_map:
                 v1_copy = vertex_map[v1_orig]
                 v2_copy = vertex_map[v2_orig]
                 mid_pos = Vec3D.middle_point(v1_copy.position, v2_copy.position)
                 mid_vertex = Vertex(mid_pos)
                 new_vertices.append(mid_vertex)
                 edge_midpoint_map[edge_key] = mid_vertex

        for face_orig in faces:
            center_pos_sum = Vec3D(0, 0, 0, 0)
            num_face_verts = len(face_orig.vertices)
            if num_face_verts > 0:
                for v_orig in face_orig.vertices:
                    v_copy = vertex_map[v_orig]
                    center_pos_sum += v_copy.position.vectorize()
                center_pos_sum = center_pos_sum * (1.0 / num_face_verts)
                center_pos = center_pos_sum.pointize()
            else:
                center_pos = Vec3D(0,0,0)
            center_vertex = Vertex(center_pos)
            new_vertices.append(center_vertex)
            face_centroid_map[face_orig] = center_vertex         
                 
        for face_orig in faces:
            orig_verts = face_orig.vertices
            num_orig_verts = len(orig_verts)
            sid = face_orig.surface_id
            copied_orig_verts = [vertex_map[v] for v in orig_verts]
            center_vert = face_centroid_map[face_orig]

            if num_orig_verts == 4:
                v0, v1, v2, v3 = copied_orig_verts
                m01 = edge_midpoint_map[tuple(sorted((id(orig_verts[0]), id(orig_verts[1]))))]
                m12 = edge_midpoint_map[tuple(sorted((id(orig_verts[1]), id(orig_verts[2]))))]
                m23 = edge_midpoint_map[tuple(sorted((id(orig_verts[2]), id(orig_verts[3]))))]
                m30 = edge_midpoint_map[tuple(sorted((id(orig_verts[3]), id(orig_verts[0]))))]
                f1 = Face([v0, m01, center_vert, m30], sid)
                f2 = Face([v1, m12, center_vert, m01], sid)
                f3 = Face([v2, m23, center_vert, m12], sid)
                f4 = Face([v3, m30, center_vert, m23], sid)
                new_faces.extend([f1, f2, f3, f4])
                edges_to_add = [(v0, m01), (m01, center_vert), (center_vert, m30), (m30, v0), (v1, m12), (m12, center_vert), (center_vert, m01), (m01, v1), (v2, m23), (m23, center_vert), (center_vert, m12), (m12, v2), (v3, m30), (m30, center_vert), (center_vert, m23), (m23, v3)]
                for v_a, v_b in edges_to_add: new_edges_set.add(tuple(sorted((id(v_a), id(v_b)))))

            elif num_orig_verts == 3:
                v0, v1, v2 = copied_orig_verts
                m01 = edge_midpoint_map[tuple(sorted((id(orig_verts[0]), id(orig_verts[1]))))]
                m12 = edge_midpoint_map[tuple(sorted((id(orig_verts[1]), id(orig_verts[2]))))]
                m20 = edge_midpoint_map[tuple(sorted((id(orig_verts[2]), id(orig_verts[0]))))]
                f1 = Face([v0, m01, m20], sid)
                f2 = Face([v1, m12, m01], sid)
                f3 = Face([v2, m20, m12], sid)
                f4 = Face([m01, m12, m20], sid)
                new_faces.extend([f1, f2, f3, f4])
                edges_to_add = [(v0, m01), (m01, m20), (m20, v0), (v1, m12), (m12, m01), (m01, v1), (v2, m20), (m20, m12), (m12, v2), (m01, m12), (m12, m20), (m20, m01)]
                for v_a, v_b in edges_to_add: new_edges_set.add(tuple(sorted((id(v_a), id(v_b)))))

        vertex_id_map = {id(v): v for v in new_vertices}
        new_edges = []
        for id1, id2 in new_edges_set:
            if id1 in vertex_id_map and id2 in vertex_id_map:
                new_edges.append(Edge(vertex_id_map[id1], vertex_id_map[id2]))

        return new_vertices, new_edges, new_faces      

    @staticmethod
    def calculate_catmull_clark(vertices: list[Vertex], edges: list[Edge], faces: list[Face]) -> tuple[list[Vertex], list[Edge], list[Face]]:
        vertex_adj_faces: dict[Vertex, list[Face]] = {}
        vertex_adj_edges: dict[Vertex, list[Edge]] = {}
        edge_key_to_edge_obj: dict[tuple[int,...], Edge] = {}
        edge_key_to_adj_faces: dict[tuple[int,...], list[Face]] = {}

        for v in vertices:
            vertex_adj_faces[v] = []
            vertex_adj_edges[v] = []

        for edge_obj in edges:
            key = tuple(sorted((id(edge_obj.v1), id(edge_obj.v2))))
            edge_key_to_edge_obj[key] = edge_obj
            edge_key_to_adj_faces[key] = []
            if edge_obj not in vertex_adj_edges[edge_obj.v1]:
                 vertex_adj_edges[edge_obj.v1].append(edge_obj)
            if edge_obj not in vertex_adj_edges[edge_obj.v2]:
                 vertex_adj_edges[edge_obj.v2].append(edge_obj)

        for face in faces:
            for v_idx in range(len(face.vertices)):
                v_orig = face.vertices[v_idx]
                if face not in vertex_adj_faces[v_orig]:
                    vertex_adj_faces[v_orig].append(face)

                v_next_orig = face.vertices[(v_idx + 1) % len(face.vertices)]
                edge_v_ids = tuple(sorted((id(v_orig), id(v_next_orig))))
                if edge_v_ids in edge_key_to_adj_faces:
                    if face not in edge_key_to_adj_faces[edge_v_ids]:
                        edge_key_to_adj_faces[edge_v_ids].append(face)

        new_mesh_vertices_list: list[Vertex] = []
        face_to_fp_vertex: dict[Face, Vertex] = {}

        for face_orig in faces:
            if not face_orig.vertices:
                continue
            
            center_pos_vec_sum = Vec3D(0,0,0,0) 
            for v_in_face in face_orig.vertices:
                center_pos_vec_sum += v_in_face.position.vectorize() 
            
            if len(face_orig.vertices) > 0:
                center_pos_vec_sum = center_pos_vec_sum * (1.0 / len(face_orig.vertices))
            
            fp_pos_point = center_pos_vec_sum.pointize() 
            fp_vertex = Vertex(fp_pos_point)
            new_mesh_vertices_list.append(fp_vertex)
            face_to_fp_vertex[face_orig] = fp_vertex

        edge_key_to_ep_vertex: dict[tuple[int,...], Vertex] = {}
        for edge_key, edge_obj in edge_key_to_edge_obj.items():
            v1_orig_pos = edge_obj.v1.position
            v2_orig_pos = edge_obj.v2.position
            
            adj_faces_for_this_edge = edge_key_to_adj_faces.get(edge_key, [])
            
            sum_ep_vec = Vec3D(0,0,0,0)
            sum_ep_vec += v1_orig_pos.vectorize()
            sum_ep_vec += v2_orig_pos.vectorize()
            num_terms = 2.0
            
            if len(adj_faces_for_this_edge) == 2:
                fp1 = face_to_fp_vertex[adj_faces_for_this_edge[0]]
                fp2 = face_to_fp_vertex[adj_faces_for_this_edge[1]]
                sum_ep_vec += fp1.position.vectorize()
                sum_ep_vec += fp2.position.vectorize()
                num_terms += 2.0
            elif len(adj_faces_for_this_edge) == 1:
                fp_adj = face_to_fp_vertex[adj_faces_for_this_edge[0]]
                sum_ep_vec += fp_adj.position.vectorize()
                num_terms += 1.0
            
            avg_ep_vec = sum_ep_vec * (1.0 / num_terms)
            ep_pos_point = avg_ep_vec.pointize()
            
            ep_vertex = Vertex(ep_pos_point) 
            new_mesh_vertices_list.append(ep_vertex)
            edge_key_to_ep_vertex[edge_key] = ep_vertex
            
        orig_vertex_to_mop_vertex: dict[Vertex, Vertex] = {}
        for v_orig in vertices:
            connected_faces = vertex_adj_faces.get(v_orig, [])
            connected_edges = vertex_adj_edges.get(v_orig, [])
            
            n_faces = float(len(connected_faces))
            p_orig_pos_point = v_orig.position # Bu bir nokta

            if n_faces < 1e-6: 
                mop_pos_point = p_orig_pos_point.copy()
            else:
                sum_fp_vec = Vec3D(0,0,0,0)
                for face_item in connected_faces:
                    sum_fp_vec += face_to_fp_vertex[face_item].position.vectorize()
                f_avg_vec = sum_fp_vec * (1.0 / n_faces)
                f_avg_point = f_avg_vec.pointize()

                sum_r_midpoints_vec = Vec3D(0,0,0,0)
                n_edges = float(len(connected_edges))
                if n_edges < 1e-6: 
                    r_avg_point = p_orig_pos_point.copy() 
                else:
                    for edge_item in connected_edges:
                        midpoint_as_point = Vec3D.middle_point(edge_item.v1.position, edge_item.v2.position)
                        sum_r_midpoints_vec += midpoint_as_point.vectorize()
                    r_avg_vec = sum_r_midpoints_vec * (1.0 / n_edges)
                    r_avg_point = r_avg_vec.pointize()
                
                weight_F = 1.0 / n_faces
                weight_R = 2.0 / n_faces
                weight_P = (n_faces - 3.0) / n_faces
                
                term_F_vec = f_avg_point.vectorize() * weight_F
                term_R_vec = r_avg_point.vectorize() * weight_R
                term_P_vec = p_orig_pos_point.vectorize() * weight_P
                
                mop_sum_vec = term_F_vec + term_R_vec + term_P_vec
                mop_pos_point = mop_sum_vec.pointize()

            mop_vertex = Vertex(mop_pos_point)
            new_mesh_vertices_list.append(mop_vertex)
            orig_vertex_to_mop_vertex[v_orig] = mop_vertex

        final_faces: list[Face] = []
        final_edges_set: set[tuple[int,...]] = set()

        for face_orig in faces:
            if not face_orig.vertices:
                continue
            
            fp_of_this_face = face_to_fp_vertex[face_orig]
            num_orig_verts_in_face = len(face_orig.vertices)

            for i in range(num_orig_verts_in_face):
                v_curr_orig = face_orig.vertices[i]
                v_next_orig = face_orig.vertices[(i + 1) % num_orig_verts_in_face]
                v_prev_orig = face_orig.vertices[(i - 1 + num_orig_verts_in_face) % num_orig_verts_in_face]

                mop_v_curr = orig_vertex_to_mop_vertex[v_curr_orig]
                
                edge_key_curr_next = tuple(sorted((id(v_curr_orig), id(v_next_orig))))
                ep_curr_next = edge_key_to_ep_vertex.get(edge_key_curr_next)
                
                edge_key_prev_curr = tuple(sorted((id(v_prev_orig), id(v_curr_orig))))
                ep_prev_curr = edge_key_to_ep_vertex.get(edge_key_prev_curr)

                if ep_curr_next is None or ep_prev_curr is None:
                    continue 
                
                new_quad_vertices = [
                    fp_of_this_face,
                    ep_curr_next,
                    mop_v_curr,
                    ep_prev_curr
                ]
                new_face = Face(new_quad_vertices, face_orig.surface_id)
                final_faces.append(new_face)

                for v_quad_idx in range(len(new_quad_vertices)):
                    vert1 = new_quad_vertices[v_quad_idx]
                    vert2 = new_quad_vertices[(v_quad_idx + 1) % len(new_quad_vertices)]
                    final_edges_set.add(tuple(sorted((id(vert1), id(vert2)))))
        
        final_edges: list[Edge] = []
        vertex_id_to_new_vertex_obj: dict[int, Vertex] = {id(v): v for v in new_mesh_vertices_list}
        
        for id1, id2 in final_edges_set:
            if id1 in vertex_id_to_new_vertex_obj and id2 in vertex_id_to_new_vertex_obj:
                 v_a = vertex_id_to_new_vertex_obj[id1]
                 v_b = vertex_id_to_new_vertex_obj[id2]
                 final_edges.append(Edge(v_a, v_b))

        return new_mesh_vertices_list, final_edges, final_faces
