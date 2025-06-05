# CENG 487 Assignment4 by
# Bugrahan Imal
# StudentId: 280201012
# May 2025
from .base_mode import BaseMode
from object3d import Object3D
from generators import create_box_object, create_cylinder_object, create_pyramid_object, create_sphere_object, create_torus_object, create_tetrahedron_object
from parser import parse_file
from math3d import Vec3D



class SceneMode:
    base_mode:BaseMode


    def __init__(self, base_mode:BaseMode) -> None:
        self.base_mode = base_mode

    def handle_key_press(self, key:bytes) -> bool:
        if key in [b'1', b'\x00', b'\x1b', b'\x1c', b'\x1d', b'\x1e']:
            if not self.base_mode.ctrl_key_pressed:
                return False
            return self.__add_object(key)
        elif key == b'\x0f':
            if not self.base_mode.ctrl_key_pressed:
                return False
            return self.__load_object()
        elif key == b'0':
            if not self.base_mode.ctrl_key_pressed:
                return False
            return self.__toggle_grid()
        elif key == b'\x7f':
            return self.__remove_object()
        elif key == b'x':
            return self.__loop_active_object()  
        
        return self.base_mode.handle_key_press(key)
    
    def handle_special_key_press(self, key:int) -> bool:
        return self.base_mode.handle_special_key_press(key)

    def handle_special_key_release(self, key:int) -> None:
        self.base_mode.handle_special_key_release(key)

    def handle_mouse_wheel(self, direction:int) -> bool:
        return False

    def handle_mouse_button(self, button:int, is_pressed:bool, x:int, y:int) -> bool:
        return False

    def handle_mouse_drag(self, x:int, y:int) -> bool:
        return False

    def __add_object(self, obj_id:bytes) -> bool:
        shader = self.base_mode.scene.shader
        obj = Object3D(shader)
        if obj_id == b'1':
            obj = create_box_object(shader, "Box", 10, 10, 10)
        elif obj_id == b'\x00':
            obj = create_cylinder_object(shader, "Cylinder", 5, 10, 32)
        elif obj_id == b'\x1b':
            obj = create_pyramid_object(shader, "Pyramid", 10, 10, 15)
        elif obj_id == b'\x1c':
            obj = create_sphere_object(shader, "Sphere", 5, 32, 16)
        elif obj_id == b'\x1d':
            obj = create_torus_object(shader, "Torus", 5, 2.5, 32, 16)
        elif obj_id == b'\x1e':
            obj = create_tetrahedron_object(shader, "Tetrahedron", 5)
  
        self.base_mode.scene.add_object(obj)
        self.base_mode.scene.set_active_object(obj)
        return True
    
    def __remove_object(self) -> bool:
        active_obj = self.base_mode.scene.get_active_object()
        if active_obj is None:
            return False
        
        self.base_mode.scene.remove_object(active_obj)
        self.base_mode.scene.set_active_object(self.base_mode.scene.get_latest_object())
        return True
    
    def __load_object(self) -> bool:
        active_obj = self.base_mode.scene.get_active_object()
        if active_obj is not None:
            return False

        filepath = input("Please Provide path of .obj file:")
        obj = parse_file(filepath, Vec3D(0, 1, 0, 0), Vec3D(0, 0, -1, 0))
        if obj is None:
            return False

        self.base_mode.scene.add_object(obj)
        self.base_mode.scene.set_active_object(obj)
        return True

    def __toggle_grid(self) -> bool:
        self.base_mode.scene.change_grid_visibility()
        return True
    
    def __loop_active_object(self) -> bool:
        active_obj = self.base_mode.scene.get_active_object()
        if active_obj is None:
            return False

        obj = self.base_mode.scene.get_next_object(active_obj)
        if obj is None:
            return False
        self.base_mode.scene.set_active_object(obj)
        return True
