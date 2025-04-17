# CENG 487 Assignment2 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from OpenGL.GL import (
    GL_TRIANGLES, glBegin, glEnd, glVertex3f, glColor3f, GL_LINES, GL_POLYGON, GL_POINTS, glPointSize
)


from math3d import Mat3D
from camera import Camera
from geometry import Mesh
from scene import Scene



class Renderer:
    
    @staticmethod
    def bake_to_world_space(data:Mesh|Camera, m2w_matrix:Mat3D) -> None:
        data.apply_transform(m2w_matrix)

    @staticmethod
    def convert_to_ndc_camera(data:Camera) -> None:
        pass

    @staticmethod
    def convert_to_ndc_mesh(data:Mesh) -> None:
        for v in data.vertices:
            if abs(v.position.w) > 1e-6:
                v.position.x /= v.position.w
                v.position.y /= v.position.w
                v.position.z /= v.position.w
                v.position.w = 1
                
    @staticmethod
    def bake_to_clip_space(data:Mesh|Camera, w2c_matrix:Mat3D) -> None:
        data.apply_transform(w2c_matrix)
        if isinstance(data, Mesh):
            return Renderer.convert_to_ndc_mesh(data)
        if isinstance(data, Camera):
            return Renderer.convert_to_ndc_camera(data)
    
    @staticmethod
    def draw_camera(cam:Camera) -> None:
        pass

    @staticmethod
    def draw_mesh(mesh:Mesh) -> None:
        if mesh.faces:
            glColor3f(0, 0, 1)
            for face in mesh.faces:
                glBegin(GL_POLYGON)
                for v in face.vertices:
                    glVertex3f(v.position.x, v.position.y, v.position.z)
                glEnd()

        if mesh.edges:
            glColor3f(0, 1, 0)
            glBegin(GL_LINES)
            for edge in mesh.edges:
                v1 = edge.v1
                v2 = edge.v2
                glVertex3f(v1.position.x, v1.position.y, v1.position.z)
                glVertex3f(v2.position.x, v2.position.y, v2.position.z)
            glEnd()

        if mesh.vertices:
            glColor3f(1, 0, 0)
            glPointSize(5.0)
            glBegin(GL_POINTS)
            for v in mesh.vertices:
                glVertex3f(v.position.x, v.position.y, v.position.z)
            glEnd()

    @staticmethod
    def draw(data:Mesh|Camera) -> None:
        if isinstance(data, Mesh):
            return Renderer.draw_mesh(data)
        if isinstance(data, Camera):
            return Renderer.draw_camera(data)

    @staticmethod
    def render_scene(scene:Scene) -> None:
        camera_object = scene.get_active_camera()
        if camera_object is None:
            return
        cam = camera_object.data.copy()
        Renderer.bake_to_world_space(cam, camera_object.get_m2w_matrix()) 
        if not isinstance(cam, Camera):
            return
        w2c_matrix = cam.get_w2c_matrix()

        for obj in scene.get_visible_objects():
            m2w_matrix = obj.get_m2w_matrix()
            data = obj.data.copy()
            Renderer.bake_to_world_space(data, m2w_matrix)
            Renderer.bake_to_clip_space(data, w2c_matrix)
            Renderer.draw(data)


