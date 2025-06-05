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

    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, Vec3D):
            return NotImplemented
        return self.x == value.x and self.y == value.y and self.z == value.z and self.w == value.w 

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z, self.w))

    def __add__(self, other:Vec3D) -> Vec3D:
        if self.w == 1 and other.w == 1:
            raise Exception("Point+Point invalid")
        if self.w == 0 and other.w == 1:
            raise Exception("Vector+Point invalid")
        
        return Vec3D(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
            self.w + other.w
        )

    def __sub__(self, other:Vec3D) -> Vec3D:
        if self.w == 0 and other.w == 1:
            raise Exception("Vector-Point invalid")
        
        return Vec3D(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
            self.w - other.w
        )

    def __mul__(self, scalar:float) -> Vec3D:
        if self.w == 1:
            raise Exception("Cannot scale a point")
        return Vec3D(
            self.x * scalar,
            self.y * scalar,
            self.z * scalar,
            self.w
        )

    def __rmul__(self, scalar:float) -> Vec3D:
        return self * scalar
    
    def __repr__(self) -> str:
        return f"Vec3D Object with : x={self.x}, y={self.y}, z={self.z}, w={self.w}"

    def copy(self) -> Vec3D:
        return Vec3D(self.x, self.y, self.z, self.w)
    
    def dot(self, other:Vec3D) -> float:
        if self.w == 1 or other.w == 1:
            raise Exception("Only Vector.Vector valid")
        
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other:Vec3D) -> Vec3D:
        if self.w == 1 or other.w == 1:
            raise Exception("Only VectorxVector valid")

        return Vec3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
            0
        )

    def magnitude(self) -> float:
        if self.w == 1:
            raise Exception("Point magniute invalid")
        
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self) -> Vec3D:
        l = self.magnitude()
        if l == 0:
            return Vec3D(0, 0, 0, 0)
        if l == 1:
            return self.copy()
        return Vec3D(
            self.x / l,
            self.y / l,
            self.z / l,
            0
        )

    def flatten(self) -> list[float]:
        return [self.x, self.y, self.z, self.w]

    def vectorize(self) -> Vec3D:
        return Vec3D(self.x, self.y, self.z, 0)

    def pointize(self) -> Vec3D:
        return Vec3D(self.x, self.y, self.z, 1)
    
    @staticmethod
    def middle_point(first:Vec3D, second:Vec3D) -> Vec3D:
        if first.w == 0 or second.w == 0:
            raise Exception("Only Point, Point valid")

        return Vec3D(
            (first.x + second.x) / 2,
            (first.y + second.y) / 2,
            (first.z + second.z) / 2,
            1
        )
