# CENG 487 Assignment5 by
# Bugrahan Imal
# StudentId: 280201012
# June 2025
from __future__ import annotations
from typing import Any



class Vec4D:
    r: float
    g: float
    b: float
    a: float

    def __init__(self, r: float = 0.0, g: float = 0.0, b: float = 0.0, a: float = 1.0) -> None:
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __repr__(self) -> str:
        return f"Vec4D(r={self.r:.3f}, g={self.g:.3f}, b={self.b:.3f}, a={self.a:.3f})"

    def copy(self) -> Vec4D:
        return Vec4D(self.r, self.g, self.b, self.a)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Vec4D):
            return NotImplemented
        return self.r == other.r and self.g == other.g and self.b == other.b and self.a == other.a

    def __hash__(self) -> int:
        return hash((self.r, self.g, self.b, self.a))

    def flatten(self) -> list[float]:
        return [self.r, self.g, self.b, self.a]

    def __add__(self, other: Vec4D) -> Vec4D:
        return Vec4D(self.r + other.r, self.g + other.g, self.b + other.b, self.a + other.a)

    def __sub__(self, other: Vec4D) -> Vec4D:
        return Vec4D(self.r - other.r, self.g - other.g, self.b - other.b, self.a - other.a)

    def __mul__(self, scalar: float) -> Vec4D:
        return Vec4D(self.r * scalar, self.g * scalar, self.b * scalar, self.a)

