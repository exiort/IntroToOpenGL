# CENG 487 Assignment5 by
# Bugrahan Imal
# StudentId: 280201012
# June 2025

from __future__ import annotations
import math



class Vec2D:
    u: float
    v: float

    def __init__(self, u: float = 0.0, v: float = 0.0) -> None:
        self.u = u
        self.v = v

    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, Vec2D):
            return NotImplemented
        return self.u == value.u and self.v == value.v

    def __hash__(self) -> int:
        return hash((self.u, self.v))
        
    def __add__(self, other: Vec2D) -> Vec2D:
        return Vec2D(
            self.u + other.u,
            self.v + other.v
        )

    def __sub__(self, other: Vec2D) -> Vec2D:
        return Vec2D(
            self.u - other.u,
            self.v - other.v
        )

    def __mul__(self, scalar: float) -> Vec2D:
        return Vec2D(
            self.u * scalar,
            self.v * scalar
        )

    def __rmul__(self, scalar: float) -> Vec2D:
        return self.__mul__(scalar)
    
    def __repr__(self) -> str:
        return f"Vec2D(u={self.u}, v={self.v})"
 
    def copy(self) -> Vec2D:
        return Vec2D(self.u, self.v)
    
    def magnitude_sq(self) -> float:
        return self.u**2 + self.v**2

    def magnitude(self) -> float:
        return math.sqrt(self.magnitude_sq())

    def normalize(self) -> Vec2D:
        l = self.magnitude()
        if l == 0:
            return Vec2D(0, 0)
        if l == 1:
            return self.copy()
        return Vec2D(
            self.u / l,
            self.v / l
        )

    def dot(self, other: Vec2D) -> float:
        return self.u * other.u + self.v * other.v

    def flatten(self) -> list[float]:
        return [self.u, self.v]

    @staticmethod
    def lerp(v1: Vec2D, v2: Vec2D, t: float) -> Vec2D:
        t_clamped = max(0.0, min(1.0, t))
        return Vec2D(
            v1.u + (v2.u - v1.u) * t_clamped,
            v1.v + (v2.v - v1.v) * t_clamped
        )
