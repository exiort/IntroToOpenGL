# CENG 487 Assignment 6 by
# Bugrahan Imal
# StudentId: 280201012
# June 2025
from __future__ import annotations
from math3d import Vec4D



class Material:
    texture_id1: int
    texture_id2: int
    blend_factor: float

    use_raw_color:bool
    raw_color:Vec4D
    
    def __init__(self) -> None:
        self.texture_id1 = -1
        self.texture_id2 = -1
        self.blend_factor = 0.0

        self.use_raw_color = False
        self.raw_color = Vec4D()
        
    def set_textures(self, tex_id1: int, tex_id2: int) -> None:
        self.texture_id1 = tex_id1
        self.texture_id2 = tex_id2

    def copy(self) -> Material:
        new_material = Material()
        new_material.texture_id1 = self.texture_id1
        new_material.texture_id2 = self.texture_id2
        new_material.blend_factor = self.blend_factor
        new_material.use_raw_color = self.use_raw_color
        new_material.raw_color = self.raw_color
        return new_material
