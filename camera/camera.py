# CENG 487 Assignment2 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from __future__ import annotations
from math3d import Vec3D, Mat3D



class Camera:
    name:str
    position:Vec3D
    target:Vec3D
    up: Vec3D

    fov:float
    aspect_ratio:float
    near:float
    far:float

    ortho_scale:float
    projection_type:str

    view_matrix:Mat3D
    projection_matrix:Mat3D

    is_view_dirty:bool
    is_proj_dirty:bool
    
    def __init__(
            self, name:str, position:Vec3D, target:Vec3D, up_hint:Vec3D,
            fov:float=60, aspect_ratio:float=1, near:float=0.1, far:float=100,
            projection_type:str="perspective", ortho_scale:float=5
    ) -> None:
        if position.w != 1 or target.w != 1:
            raise Exception("Poisition and Target must be point")
        if up_hint.w != 0:
            raise Exception("Up_hint must be vector")
        
        self.name = name
        
        self.position = position
        self.target = target
        self.up = up_hint
        
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        self.near = near
        self.far = far
        self.projection_type = projection_type
        self.ortho_scale = ortho_scale

        self.view_matrix = Mat3D.identity()
        self.projection_matrix = Mat3D.identity()

        self.is_view_dirty = True 
        self.is_proj_dirty = True

#    def apply_transform(self, transform: Mat3D) -> None:
#        self.position = transform * self.position
#        self.target = transform * self.target
#        self.up = (transform * self.up).normalize()
#        self.is_view_dirty = True

    def copy(self) -> Camera:
        new_camera = Camera(
            self.name,
            position=self.position.copy(),
            target=self.target.copy(),
            up_hint=self.up.copy(),
            fov=self.fov,
            aspect_ratio=self.aspect_ratio,
            near=self.near,
            far=self.far,
            projection_type=self.projection_type,
            ortho_scale=self.ortho_scale
        )
    
        new_camera.view_matrix = self.view_matrix.copy()
        new_camera.projection_matrix = self.projection_matrix.copy()
        new_camera.is_view_dirty = self.is_view_dirty
        new_camera.is_proj_dirty = self.is_proj_dirty
        return new_camera

    def set_projection_perspective(
            self,
            fov:float|None=None,
            aspect_ratio:float|None=None,
            near:float|None=None,
            far:float|None=None
    ) -> None:
        if fov is not None:
            self.fov = fov
        if aspect_ratio is not None:
            self.aspect_ratio = aspect_ratio
        if near is not None:
            self.near = near
        if far is not None:
            self.far = far

        self.projection_type = "perspective"
        self.is_proj_dirty = True

    def set_projection_orthographic(
            self,
            ortho_scale:float|None=None,
            aspect_ratio:float|None=None,
            near:float|None=None,
            far:float|None=None
    ) -> None:
        if ortho_scale is not None:
            self.ortho_scale = ortho_scale
        if aspect_ratio is not None:
            self.aspect_ratio = aspect_ratio
        if near is not None:
            self.near = near
        if far is not None:
            self.far = far

        self.projection_type = "orthographic"
        self.is_proj_dirty = True

    def set_position(self, position:Vec3D) -> None:
        if position.w != 1:
            raise Exception("Position must be point")
        self.position = position
        self.is_view_dirty = True

    def set_target(self, target:Vec3D) -> None:
        if target.w != 1:
            raise Exception("Target must be point")
        self.target = target
        self.is_view_dirty = True

    def set_up(self, up:Vec3D) -> None:
        if up.w != 0:
            raise Exception("Up must be vector")
        self.up = up
        self.is_view_dirty = True
        
    def get_projection_matrix(self) -> Mat3D:
        if self.is_proj_dirty:
            if self.projection_type == "perspective":
                self.projection_matrix = Mat3D.perspective(
                    fov=self.fov,
                    aspect_ratio=self.aspect_ratio,
                    near=self.near,
                    far=self.far
                )
            elif self.projection_type == "orthographic":
                right = self.ortho_scale * self.aspect_ratio
                left = -right
                top = self.ortho_scale
                bottom = -top
            
                self.projection_matrix = Mat3D.orthographic(
                    left=left,
                    right=right,
                    bottom=bottom,
                    top=top,
                    near=self.near,
                    far=self.far
                )
            self.is_proj_dirty = False

        return self.projection_matrix

    def get_view_matrix(self) -> Mat3D:
        if self.is_view_dirty:
            self.view_matrix = Mat3D.look_at(self.position, self.target, self.up)
            self.is_view_dirty = False
            
        return self.view_matrix

    def get_w2c_matrix(self) -> Mat3D:
        return self.get_projection_matrix() @ self.get_view_matrix()
    
    def get_forward_vector(self) -> Vec3D:
        return (self.target - self.position).normalize()

    def get_right_vector(self) -> Vec3D:
        return self.get_forward_vector().cross(self.up).normalize()

    def get_up_vector(self) -> Vec3D:
        return self.get_right_vector().cross(self.get_forward_vector()).normalize()

