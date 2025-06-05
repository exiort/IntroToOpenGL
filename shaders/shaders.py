# CENG 487 Assignment5 by
# Bugrahan Imal
# StudentId: 280201012
# June 2025

from OpenGL.GL import GL_COMPILE_STATUS, GL_FALSE, GL_LINK_STATUS, glAttachShader, glCompileShader, glCreateProgram, glCreateShader, glDeleteProgram, glDeleteShader, glDetachShader, glGetProgramInfoLog, glGetProgramiv, glGetShaderInfoLog, glGetShaderiv, glGetUniformLocation, glLinkProgram, glShaderSource, glUniform1f, glUniform3fv, glUniformMatrix4fv, glUseProgram, GL_TRUE

import numpy as np

class Shader:
    program_id:int
    uniform_cache:dict[str, int]

    def __init__(self, shader_info:list[tuple[str, int]]) -> None:
        self.program_id = -1
        self.uniform_cache = {}

        if not shader_info: return

        compiled_shader_ids:list[int] = []
        for filepath, shader_type in shader_info:
            source = self.__load_shader_source(filepath)
            if source is None: continue

            shader_id = self.__compile_shader(source, shader_type)
            if shader_id == 0: continue

            compiled_shader_ids.append(shader_id)

        if len(compiled_shader_ids) == 0:
            raise Exception("__init__:No Shader can compiled!")

        self.program_id = self.__link_program(compiled_shader_ids)
            
    def delete(self) -> None:
        if self.program_id == -1: return

        glDeleteProgram(self.program_id)
        self.program_id = -1
        self.uniform_cache.clear()
        
    def __load_shader_source(self, filepath:str) -> str|None:
        try:
            with open(filepath, 'r') as f:
                return f.read()
        except Exception as e:
            print(f"__load_shader_source:{e}")
            return None
        
    def __compile_shader(self, source:str, shader_type:int) -> int:
        shader_id = glCreateShader(shader_type)
        if shader_id == 0:
            return 0

        glShaderSource(shader_id, source)
        glCompileShader(shader_id)

        compile_status = glGetShaderiv(shader_id, GL_COMPILE_STATUS)
        if compile_status == GL_FALSE:
            info_log = glGetShaderInfoLog(shader_id)
            
            if isinstance(info_log, bytes):
                info_log = info_log.decode('utf-8')

            print(f"__compile_shader: {info_log}")
            
            glDeleteShader(shader_id)
            return 0
        
        return shader_id#type:ignore

    def __link_program(self, compiled_shader_ids:list[int]) -> int:
        program_id = glCreateProgram()
        if program_id == 0:
            for shader_id in compiled_shader_ids:
                glDeleteShader(shader_id)

            raise Exception("Failed to create shader program object.")
        for shader_id in compiled_shader_ids:
            glAttachShader(program_id, shader_id)

        glLinkProgram(program_id)

        link_status = glGetProgramiv(program_id, GL_LINK_STATUS)
        if link_status == GL_FALSE:
            info_log = glGetProgramInfoLog(program_id)
            if isinstance(info_log, bytes):
                info_log = info_log.decode('utf-8')

            glDeleteProgram(program_id)
            for shader_id in compiled_shader_ids:
                glDeleteShader(shader_id)

            raise Exception(f"Error linking shader program: {info_log}")

        for shader_id in compiled_shader_ids:
            glDetachShader(program_id, shader_id)
            glDeleteShader(shader_id)

        return program_id#type:ignore

    def use(self) -> None:
        if self.program_id != -1:
            glUseProgram(self.program_id)
        else:
            pass
        
    def unuse(self) -> None:
        glUseProgram(0)

    def get_uniform_location(self, name:str) -> int:
        if self.program_id == -1:
            return -1
        if name in self.uniform_cache:
            return self.uniform_cache[name]

        location = glGetUniformLocation(self.program_id, name)
        self.uniform_cache[name] = location
        return location
        
    def set_uniform_mat4d(self, name:str, matrix:np.ndarray, transpose:bool=False) -> None:
        if self.program_id == -1: return
        loc = self.get_uniform_location(name)
        if loc == -1: return

        gl_transpose = GL_TRUE if transpose else GL_FALSE
        glUniformMatrix4fv(loc, 1, gl_transpose, matrix)

    def set_uniform_1f(self, name:str, value:float) -> None:
        if self.program_id == -1: return
        loc = self.get_uniform_location(name)
        if loc == -1: return

        glUniform1f(loc, value)

    def set_uniform_vec3d(self, name:str, vector_data:np.ndarray) -> None:
        if self.program_id == -1: return
        loc = self.get_uniform_location(name)
        if loc == -1: return

        glUniform3fv(loc, 1, vector_data)

    
