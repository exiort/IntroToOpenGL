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

    def transpose(self) -> Mat3D:
        rows = len(self.matrix)
        columns = len(self.matrix[0])

        new_matrix_values:list[list[float]] = [[0 for _ in range(rows)] for _ in range(columns)]

        for i in range(rows):
            for j in range(columns):
                new_matrix_values[j][i] = self.matrix[i][j]

        return Mat3D(new_matrix_values)
                
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

    @staticmethod
    def look_at(eye:Vec3D, center:Vec3D, up:Vec3D) -> Mat3D:
        f = (center - eye).normalize()
        s = f.cross(up).normalize()
        u = s.cross(f)
        
        tx = -s.dot(eye.vectorize())
        ty = -u.dot(eye.vectorize())
        tz = f.dot(eye.vectorize())
        return Mat3D([
            [s.x, s.y, s.z, tx],
            [u.x, u.y, u.z, ty],
            [-f.x, -f.y, -f.z, tz],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def perspective(fov:float, aspect_ratio:float, near:float, far:float) -> Mat3D:
        f = 1 / math.tan(math.radians(fov) / 2)
        nf = 1 / (near - far)

        return Mat3D([
            [f/aspect_ratio, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (far+near)*nf, (2*far*near)*nf],
            [0, 0, -1, 0]
        ])

    @staticmethod
    def orthographic(left:float, right:float, bottom:float, top:float, near:float, far:float) -> Mat3D:
        rl = 1.0 / (right - left)
        tb = 1.0 / (top - bottom)
        fn = 1.0 / (far - near)

        sx = 2.0 * rl
        sy = 2.0 * tb
        sz = -2.0 * fn
        
        tx = -(right + left) * rl
        ty = -(top + bottom) * tb
        tz = -(far + near) * fn

        return Mat3D([
            [sx,  0.0, 0.0, tx ],
            [0.0, sy,  0.0, ty ],
            [0.0, 0.0, sz,  tz ],
            [0.0, 0.0, 0.0, 1.0]
        ])
    
    @staticmethod
    def rotation_around_axis(axis:Vec3D, angle_rad:float) -> Mat3D:
        norm_axis = axis.normalize()
        x, y, z, _ = norm_axis.flatten()
        
        cos = math.cos(angle_rad)
        sin = math.sin(angle_rad)
        omc = 1-cos
        
        r00 = x**2 * omc + cos
        r01 = x * y * omc - z * sin
        r02 = x * z * omc + y * sin

        r10 = y * x * omc + z * sin
        r11 = y**2 * omc + cos
        r12 = y * z * omc - x * sin

        r20 = z * x * omc - y * sin
        r21 = z * y * omc + x * sin
        r22 = z**2 * omc + cos

        return Mat3D([
            [r00, r01, r02, 0],
            [r10, r11, r12, 0],
            [r20, r21, r22, 0],
            [0, 0, 0, 1]
        ])
