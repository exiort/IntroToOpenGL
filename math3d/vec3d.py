# CENG 487 Assignment1 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from __future__ import annotations
import math



class Vec3D:
    x:float
    y:float
    z:float
    w:float

    def __init__(self, x:float=0, y:float=0, z:float=0, w:float=1) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __add__(self, other:Vec3D) -> Vec3D:
        return Vec3D(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )

    def __sub__(self, other:Vec3D) -> Vec3D:
        return Vec3D(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    def __mul__(self, scalar:float) -> Vec3D:
        return Vec3D(
            self.x * scalar,
            self.y * scalar,
            self.z * scalar
        )

    def __rmul__(self, scalar:float) -> Vec3D:
        return self * scalar
    
    def __repr__(self) -> str:
        return f"Vec3D Object with : x={self.x}, y={self.y}, z={self.z}, w={self.w}"

    def copy(self) -> Vec3D:
        return Vec3D(self.x, self.y, self.z, self.w)
    
    def dot(self, other:Vec3D) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other:Vec3D) -> Vec3D:
        return Vec3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self) -> Vec3D:
        l = self.magnitude()
        if l == 1:
            return self
        return Vec3D(
            self.x / l,
            self.y / l,
            self.z / l
        )

    def flatten(self) -> list[float]:
        return [self.x, self.y, self.z, self.w]

