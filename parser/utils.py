# CENG 487 Assignment3 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from math3d import Vec3D, Mat3D
from object3d import Object3D



def reorient_object(obj:Object3D, source_up:Vec3D, source_fwd:Vec3D) -> None:
    s_up = source_up.normalize()
    s_fwd = source_fwd.normalize()
    s_right = s_fwd.cross(s_up).normalize()

    t_up = Vec3D(0, 0, 1)
    t_fwd = Vec3D(0, 1, 0)
    t_right = Vec3D(1, 0, 0)

    M_source_inv = Mat3D([
        [s_right.x, s_up.x, s_fwd.x, 0],
        [s_right.y, s_up.y, s_fwd.y, 0],
        [s_right.z, s_up.z, s_fwd.z, 0],
        [0, 0, 0, 1]
    ])

    M_target = Mat3D([
        [t_right.x, t_up.x, t_fwd.x, 0.0],
        [t_right.y, t_up.y, t_fwd.y, 0.0],
        [t_right.z, t_up.z, t_fwd.z, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ])

    obj.do_transform(M_source_inv)
    obj.do_transform(M_target)
    obj.apply_transform()
