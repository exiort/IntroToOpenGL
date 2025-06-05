# CENG 487 Assignment5 by
# Bugrahan Imal
# StudentId: 280201012
# June 2025
from __future__ import annotations
from math3d import Vec2D, Vec3D, Vec4D



class VertexAttributes:
    normal:Vec3D
    uv:Vec2D
    color:Vec4D

    def __init__(self, normal:Vec3D, uv:Vec2D, color:Vec4D) -> None:
        if normal.w != 0:
            raise Exception("Normal must be vector.")

        self.normal = normal
        self.uv = uv
        self.color = color

    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, VertexAttributes):
            return NotImplemented
        return self.uv == value.uv and self.normal == value.normal and self.color == value.color

    def __hash__(self) -> int:
        return hash((self.uv, self.normal, self.color))
        
    def __repr__(self) -> str:
        return f"VertexAttributes(UV: {self.uv}, Normal: {self.normal}), Color: {self.color}"    

    def copy(self) -> VertexAttributes:
        return VertexAttributes(self.normal.copy(), self.uv.copy(), self.color.copy())

    
    
