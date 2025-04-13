# CENG 487 Assignment1 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from __future__ import annotations
from math3d import Vec3D, Mat3D



class Vertex:
    possition: Vec3D

    def __init__(self, position:Vec3D) -> None:
        self.possition = position

    def __repr__(self) -> str:
        return f"Vertex with: {self.possition}"

    def copy(self) -> Vertex:
        return Vertex(self.possition.copy())
        
    def transform(self, matrix:Mat3D):
        self.possition = matrix * self.possition

