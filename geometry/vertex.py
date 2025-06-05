# CENG 487 Assignment1 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from __future__ import annotations
from math3d import Vec3D



class Vertex:
    position: Vec3D

    
    def __init__(self, position:Vec3D) -> None:
        if position.w != 1:
            raise Exception("Position must be point")
        self.position = position

    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, Vertex):
            return NotImplemented

        return self.position == value.position

    def __hash__(self) -> int:
        return hash(self.position)
    
    def __repr__(self) -> str:
        return f"Vertex with: {self.position}"

    def copy(self) -> Vertex:
        new_position = self.position.copy()
        return Vertex(new_position)
        
    #def transform(self, matrix:Mat3D) -> None:
    #    self.position = matrix * self.position

