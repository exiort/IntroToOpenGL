# CENG 487 Assignment1 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from __future__ import annotations
import math
from .vec3d import Vec3D


class Mat3D:
    matrix:list[list[float]]

    def __init__(self, values:list[list[float]]|None = None) -> None: #Consider adding type and shape check for "values"
        if values:
            self.matrix = values
        else:
            self.matrix = [[0, 0, 0, 0] for _ in range(4)]

    def __mul__(self, other:Vec3D) -> Vec3D:
        res = [0.0, 0.0, 0.0, 0.0]
        v = other.flatten()
        for i in range(4):
            for j in range(4):
                res[i] += self.matrix[i][j] * v[j]
        return Vec3D(
            res[0],
            res[1],
            res[2],
            res[3]
        )

    def __matmul__(self, other:Mat3D) -> Mat3D:
        res = Mat3D()
        for i in range(4):
            for j in range(4):
                res.matrix[i][j] = sum(self.matrix[i][k] * other.matrix[k][j] for k in range(4))
        return res

    def __repr__(self) -> str:
        return f"Mat3D Object with : {self.matrix}"

    def copy(self) -> Mat3D:
        return Mat3D([row[:] for row in self.matrix])
    
    @staticmethod
    def identity():
        m = Mat3D()
        for i in range(4):
            m.matrix[i][i] = 1
        return m

    @staticmethod
    def __rotation_x(sin:float, cos:float) -> Mat3D:
        m = Mat3D.identity()
        m.matrix[1][1] = cos
        m.matrix[1][2] = -sin
        m.matrix[2][1] = sin
        m.matrix[2][2] = cos
        return m

    @staticmethod
    def __rotation_y(sin:float, cos:float) -> Mat3D:
        m = Mat3D.identity()
        m.matrix[0][0] = cos
        m.matrix[0][2] = sin
        m.matrix[2][0] = -sin
        m.matrix[2][2] = cos
        return m

    @staticmethod
    def __rotation_z(sin:float, cos:float) -> Mat3D:
        m = Mat3D.identity()
        m.matrix[0][0] = cos
        m.matrix[0][1] = -sin
        m.matrix[1][0] = sin
        m.matrix[1][1] = cos
        return m
    
    @staticmethod
    def rotation(axis:str, angle_rad:float) -> Mat3D:
        sin = math.sin(angle_rad)
        cos = math.cos(angle_rad)
        if axis == "x":
            return Mat3D.__rotation_x(sin, cos)
        if axis == "y":
            return Mat3D.__rotation_y(sin, cos)
        if axis == "z":
            return Mat3D.__rotation_z(sin, cos)
        return Mat3D.identity()

    @staticmethod
    def translation(tx:float, ty:float, tz:float) -> Mat3D:
        m = Mat3D.identity()
        m.matrix[0][3] = tx
        m.matrix[1][3] = ty
        m.matrix[2][3] = tz
        return m
    
    @staticmethod
    def scaling(sx:float, sy:float, sz:float) -> Mat3D:
        m = Mat3D.identity()
        m.matrix[0][0] = sx
        m.matrix[1][1] = sy
        m.matrix[2][2] = sz
        return m



