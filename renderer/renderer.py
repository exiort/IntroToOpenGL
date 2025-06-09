# CENG 487 Assignment5 by
# Bugrahan Imal
# StudentId: 280201012
# June 2025

from OpenGL.GL import glDrawArrays, glUseProgram, glActiveTexture, glBindTexture, GL_TEXTURE_2D, GL_TEXTURE0, GL_TEXTURE1
from math3d import Mat3D
from camera import Camera
from geometry import Mesh

import numpy as np



class Renderer:
    @staticmethod
    def __get_camera_matrices(scene) -> tuple[np.ndarray|None, np.ndarray|None]:
        active_camera_object = scene.get_active_camera()
        if not active_camera_object or not isinstance(active_camera_object.data, Camera):
            return None, None

        cam = active_camera_object.data
        view = Mat3D.convert_to_numpy(cam.get_view_matrix())
        proj = Mat3D.convert_to_numpy(cam.get_projection_matrix())

        return view, proj

    @staticmethod
    def __prepare_and_set_uniforms(obj, view_matrix:np.ndarray, projection_matrix:np.ndarray) -> bool:
        if obj.shader is None or obj.shader.program_id == -1 or obj.material is None:
            return False

        obj.shader.use()

        model_matrix = Mat3D.convert_to_numpy(obj.get_m2w_matrix())

        obj.shader.set_uniform_mat4d("model", model_matrix, True)
        obj.shader.set_uniform_mat4d("view", view_matrix, True)
        obj.shader.set_uniform_mat4d("projection", projection_matrix, True)

        material = obj.material
        obj.shader.set_uniform_1b("useRawColor", material.use_raw_color)

        if material.use_raw_color:
            raw_color = np.array(material.raw_color.flatten(), dtype=np.float32)
            obj.shader.set_uniform_vec4d("rawColor", raw_color)
        else:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, material.texture_id1)
            obj.shader.set_uniform_1i("texture1", 0)
        
            glActiveTexture(GL_TEXTURE1)
            glBindTexture(GL_TEXTURE_2D, material.texture_id2)
            obj.shader.set_uniform_1i("texture2", 1) 
            obj.shader.set_uniform_1f("blendFactor", material.blend_factor)
        
        return True

    @staticmethod
    def __draw_object(obj) -> None:
        if obj.renderable_data is None or obj.renderable_data.vao_id == -1 or obj.renderable_data.num_render_vertices == 0:
            return

        obj.renderable_data.bind()
        gl_draw_mode = obj.renderable_data.get_gl_draw_mode()
        if gl_draw_mode is not None:
            glDrawArrays(gl_draw_mode, 0, obj.renderable_data.num_render_vertices)
        obj.renderable_data.unbind()
 
    @staticmethod
    def render_scene(scene) -> None:
        view_matrix, projection_matrix = Renderer.__get_camera_matrices(scene)
        if view_matrix is None or projection_matrix is None:
            return
        
        for obj in scene.get_visible_objects():
            if not isinstance(obj.data, Mesh) or obj.material is None:
                continue

            obj.sync_gpu_representation()
            if not Renderer.__prepare_and_set_uniforms(obj, view_matrix, projection_matrix):
                continue

            Renderer.__draw_object(obj)

        glUseProgram(0)
