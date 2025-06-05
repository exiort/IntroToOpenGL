# CENG 487 Assignment5 by
# Bugrahan Imal
# StudentId: 280201012
# June 2025

from OpenGL.GL import (
    glGenVertexArrays, glBindVertexArray, glDeleteVertexArrays,
    glGenBuffers, glBindBuffer, glBufferData,
    glVertexAttribPointer, glEnableVertexAttribArray, glDeleteBuffers,
    GL_FLOAT, GL_FALSE, GL_STATIC_DRAW, GL_ARRAY_BUFFER, GL_TRIANGLES, GL_LINES, GL_POINTS
)
import numpy as np
import ctypes



class RenderableMesh:
    vao_id:int
    vbo_ids:dict[str, int]
    num_render_vertices:int
    render_mode:int

    def __init__(self) -> None:
        self.vao_id = -1
        self.vbo_ids = {}
        self.num_render_vertices = 0
        self.render_mode = 0

    def update_buffers(self, mode:int, positions:np.ndarray, normals:np.ndarray, uvs:np.ndarray, colors:np.ndarray, num_vertices:int) -> None:
        self.render_mode = mode
        self.num_render_vertices = num_vertices

        if self.num_render_vertices == 0 or self.render_mode == 0:
            self.release_buffers()
            return

        try: 
            self.vao_id = glGenVertexArrays(1)
            glBindVertexArray(self.vao_id)

            if positions.size > 0:
                pos_vbo_id = glGenBuffers(1)
                self.vbo_ids["positions"] = pos_vbo_id
                glBindBuffer(GL_ARRAY_BUFFER, pos_vbo_id)
                glBufferData(GL_ARRAY_BUFFER, positions.nbytes, positions, GL_STATIC_DRAW)
                glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
                glEnableVertexAttribArray(0)
        
            if uvs.size > 0:
                uv_vbo_id = glGenBuffers(1)
                self.vbo_ids["uvs"] = uv_vbo_id
                glBindBuffer(GL_ARRAY_BUFFER, uv_vbo_id)
                glBufferData(GL_ARRAY_BUFFER, uvs.nbytes, uvs, GL_STATIC_DRAW)
                glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
                glEnableVertexAttribArray(1)
                

            if normals.size > 0:
                norm_vbo_id = glGenBuffers(1)        
                self.vbo_ids["normals"] = norm_vbo_id
                glBindBuffer(GL_ARRAY_BUFFER, norm_vbo_id)
                glBufferData(GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)
                glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
                glEnableVertexAttribArray(2)

            if colors.size > 0: 
                color_vbo_id = glGenBuffers(1)
                self.vbo_ids["colors"] = color_vbo_id
                glBindBuffer(GL_ARRAY_BUFFER, color_vbo_id)
                glBufferData(GL_ARRAY_BUFFER, colors.nbytes, colors, GL_STATIC_DRAW)
                glVertexAttribPointer(3, 4, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
                glEnableVertexAttribArray(3)

        except Exception as e:
            print(f"RenderableMesh: Error during buffer update: {e}")
            self.release_buffers()
            
        finally:
            glBindBuffer(GL_ARRAY_BUFFER, 0) 
            glBindVertexArray(0)

    def release_buffers(self) -> None:
        if self.vao_id != -1 and self.vao_id != 0:
            if self.vbo_ids:
                ids_to_delete = list(self.vbo_ids.values())
                glDeleteBuffers(len(ids_to_delete), ids_to_delete)
            glDeleteVertexArrays(1, [self.vao_id])

        self.vao_id = -1
        self.vbo_ids = {}
        self.num_render_vertices = 0
        self.render_mode = 0

    def bind(self) -> None:
        if self.vao_id != -1 and self.vao_id != 0:
            glBindVertexArray(self.vao_id)

    def unbind(self) -> None:
        glBindVertexArray(0)

    def get_gl_draw_mode(self) -> int|None:
        if self.render_mode == 1:
            return GL_TRIANGLES
        elif self.render_mode == 2:
            return GL_LINES
        elif self.render_mode == 3:
            return GL_POINTS
        return None
        
