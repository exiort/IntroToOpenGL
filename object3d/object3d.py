# CENG 487 Assignment1 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from __future__ import annotations
from camera import Camera
from math3d import Mat3D
from geometry import Mesh



class Object3D:
    name:str
    do_stack:list[Mat3D]
    redo_stack:list[Mat3D]
    temporary_stack:list[Mat3D]
    crr_transform:Mat3D
    is_transform_changed:bool
    data:Mesh|Camera
    
    def __init__(self, name="Default", data:Mesh|Camera|None=None) -> None:
        self.name = name
        self.do_stack = []
        self.redo_stack = []
        self.temporary_stack = []
        self.crr_transform = Mat3D.identity()
        self.is_transform_changed = False
        if data is None:
            self.data = Mesh()
        else:
            self.data = data
            
    def __repr__(self) -> str:
        return f"Object3D(name={self.name}, transform_count={len(self.do_stack)})"

    def copy(self) -> Object3D:
        new_obj = Object3D(f"{self.name}_Copy", self.data.copy())
        new_obj.do_stack = self.do_stack.copy()
        new_obj.redo_stack = self.redo_stack.copy()
        new_obj.crr_transform = self.crr_transform.copy()
        new_obj.is_transform_changed = self.is_transform_changed
        return new_obj
    
    def do_transform(self, transform:Mat3D) -> None:
        self.redo_stack.clear()
        self.do_stack.append(transform)
        self.is_transform_changed = True

    def do_temporary(self, transform:Mat3D) -> None:
        self.temporary_stack.append(transform)
        self.is_transform_changed = True

    def finalize_temporary(self) -> None:
        res = Mat3D.identity()
        for matrix in self.temporary_stack:
            res = matrix @ res

        self.temporary_stack.clear()
        self.do_transform(res)
        
    def undo_transform(self) -> None:
        if len(self.do_stack) == 0:
            return
        matrix = self.do_stack.pop()
        self.redo_stack.append(matrix)
        self.is_transform_changed = True

    def redo_transform(self) -> None:
        if len(self.redo_stack) == 0:
            return
        matrix = self.redo_stack.pop()
        self.do_stack.append(matrix)
        self.is_transform_changed = True

    def clear_transform(self) -> None:
        if len(self.do_stack) == 0:
            return
        self.redo_stack += list(reversed(self.do_stack))
        self.do_stack.clear()
        self.is_transform_changed = True
        
    def compute_transformation(self) -> None:
        res = Mat3D.identity()
        for matrix in self.do_stack:
            res = matrix @ res
        for matrix in self.temporary_stack:
            res = matrix @ res
            
        self.crr_transform = res
        self.is_transform_changed = False

    def apply_transform(self) -> None:
        if self.is_transform_changed:
            self.compute_transformation()
        self.data.apply_transform(self.crr_transform)
        self.do_stack.clear()
        self.redo_stack.clear()
        self.temporary_stack.clear()
        self.crr_transform = Mat3D.identity()
        self.is_transform_changed = False

    def get_m2w_matrix(self) -> Mat3D:
        if self.is_transform_changed:
            self.compute_transformation()
        return self.crr_transform

