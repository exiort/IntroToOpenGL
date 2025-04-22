# CENG 487 Assignment2 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

import math
from generators import create_box
from geometry import Mesh
from math3d import Vec3D, Mat3D
from scene import Scene
from camera import Camera
from parser import parse_file



class InputHandler:
    scene:Scene
    
    __orbit_sentitivity:float
    __pan_sensitivity:float
    __dolly_sensitivity:float
    
    __mouse_state:dict[str, bool]
    __last_mouse_position:dict[str,int]
    __shift_key_pressed:bool
    __ctrl_key_pressed:bool
    __alt_key_pressed:bool
    __a_key_pressed:bool
        
    def __init__(self, scene:Scene, orbit_sensitivity:float=0.008, pan_sensitivity:float=0.008, dolly_sensitivity:float=0.75) -> None:
        self.scene = scene

        self.__mouse_state = {"left":False, "right":False, "middle":False}
        self.__last_mouse_position = {"x":0, "y":0}
        
        self.__orbit_sentitivity = orbit_sensitivity
        self.__pan_sensitivity = pan_sensitivity
        self.__dolly_sensitivity = dolly_sensitivity

        self.__shift_key_pressed = False
        self.__ctrl_key_pressed = False
        self.__alt_key_pressed = False
        self.__a_key_pressed = False        

    def get_current_sub_division_level(self) -> int:
        obj = self.scene.get_active_object()
        if obj is None:
            return -1
        elif not isinstance(obj.data, Mesh):
            return -1
        else:
            return obj.data.current_subdivision_level
        
    def handle_key_press(self, key_char:str) -> bool:
        if key_char == "a":
            self.__a_key_pressed = True
            return False
        elif key_char == "f":
            return self.__reset_camera()
        elif key_char == "0":
            if self.__a_key_pressed:
                return self.__load_object()
            
            self.scene.change_grid_visibility()
            return True
        elif key_char == "+":
            return self.__increase_subdivision()
        elif key_char == "-":
            return self.__decrease_subdivision()
        elif key_char == "1":
            if self.__a_key_pressed:
                return self.__add_object(1)
        elif key_char.encode() == b'\x7f':
            return self.__remove_object()
        elif key_char == "z":
            active_obj = self.scene.get_active_object()
            if active_obj is not None:
                active_obj.undo_transform()
                return True
        elif key_char == "r":
            active_obj = self.scene.get_active_object()
            if active_obj is not None:
                active_obj.redo_transform()
                return True
            
        return False

    def handle_key_release(self, key_char:str) -> None:
        if key_char == "a" or key_char == "A":
            self.__a_key_pressed = False

    def handle_special_key_press(self, key:int) -> bool:
        if key == 100: #left arrow
            if self.__shift_key_pressed:
                return self.__handle_camera_movement(False, -1)
            elif self.__alt_key_pressed:
                return self.__translate_active_object(0, -1, 0)
            else:
                return self.__rotate_active_object_verticaly(-1)
            
        elif key == 101: #up arrow
            if self.__shift_key_pressed:
                return self.__handle_camera_movement(True, 1)
            elif self.__alt_key_pressed:
                return self.__translate_active_object(1, 0, 0)
            elif self.__ctrl_key_pressed:
                return self.__scale_active_object(1.1)
            else:
                return self.__rotate_active_object_horizontaly(1)
            
        elif key == 102: #right arrow
            if self.__shift_key_pressed:
                return self.__handle_camera_movement(False, 1)
            elif self.__alt_key_pressed:
                return self.__translate_active_object(0, 1, 0)
            else:
                return self.__rotate_active_object_verticaly(1)
        
        elif key == 103: #down arrow
            if self.__shift_key_pressed:
                return self.__handle_camera_movement(True, -1)
            elif self.__alt_key_pressed:
                return self.__translate_active_object(-1, 0, 0)
            elif self.__ctrl_key_pressed:
                return self.__scale_active_object(0.9)
            else:
                return self.__rotate_active_object_horizontaly(-1)
            
        elif key == 112: #shift
            self.__shift_key_pressed = True
            return False
        elif key == 114: #ctrl
            self.__ctrl_key_pressed = True
            return False
        elif key == 116: #alt
            self.__alt_key_pressed = True
            return False
        
        return False

    def handle_special_key_release(self, key:int) -> None:
        if key == 112:
            self.__shift_key_pressed = False
        elif key == 114:
            self.__ctrl_key_pressed = False
        elif key == 116:
            self.__alt_key_pressed = False
    
    def handle_mouse_wheel(self, direction:int) -> bool:
        return self.__handle_dolly(direction)

    def handle_mouse_button(self, button:int, is_pressed:bool, x:int, y:int) -> bool:
        if is_pressed:
            self.__last_mouse_position["x"] = x
            self.__last_mouse_position["y"] = y
            if button == 0: self.__mouse_state["left"] = True
            elif button == 1: self.__mouse_state["right"] = True
            elif button == 2: self.__mouse_state["middle"] = True
            
        else:
            if button == 0: self.__mouse_state["left"] = False
            elif button == 1: self.__mouse_state["right"] = False
            elif button == 2: self.__mouse_state["middle"] = False

        return False
    
    def handle_mouse_drag(self, x:int, y:int) -> bool:
        if not self.__shift_key_pressed:
            return False
        redraw_needed = False
        left_pressed = self.__mouse_state["left"]
        right_pressed = self.__mouse_state["right"]
        dx = x - self.__last_mouse_position["x"]
        dy = y - self.__last_mouse_position["y"]
        
        if left_pressed:
            redraw_needed = self.__handle_orbit(dx, dy)
        elif right_pressed:
            redraw_needed = self.__handle_pan(dx, dy)

        self.__last_mouse_position["x"] = x
        self.__last_mouse_position["y"] = y

        return redraw_needed

    def __add_object(self, obj_id:int) -> bool:
        active_obj = self.scene.get_active_object()
        if active_obj is not None:
            return False

        if obj_id == 1:
            obj  = create_box("Box", 4, 4, 4)
            self.scene.add_object(obj)
            self.scene.set_active_object(obj)
            return True
        return False
    
    def __load_object(self) -> bool:
        active_obj = self.scene.get_active_object()
        if active_obj is not None:
            return False

        filepath = input("Please Provide path of .obj file:")
        obj = parse_file(filepath, Vec3D(0,1,0), Vec3D(0, 0, -1))
        if obj is None:
            return False

        self.scene.add_object(obj)
        self.scene.set_active_object(obj)
        return True
        
    def __remove_object(self) -> bool:
        active_obj = self.scene.get_active_object()
        if active_obj is None:
            return False
        self.scene.set_active_object(None)
        self.scene.remove_object(active_obj)
        return True

    def __rotate_active_object_verticaly(self, direction:int) -> bool:
        active_obj = self.scene.get_active_object()
        if active_obj is None:
            return False

        rotation = Mat3D.rotation("z", math.pi/36 * direction)
        active_obj.do_transform(rotation)
        return True

    def __rotate_active_object_horizontaly(self, direction:int) -> bool:
        active_obj = self.scene.get_active_object()
        if active_obj is None:
            return False
        rotation = Mat3D.rotation("x", math.pi/36 * direction)
        active_obj.do_transform(rotation)
        return True

    def __translate_active_object(self, tx:int, ty:int, tz:int) -> bool:
        active_obj = self.scene.get_active_object()
        if active_obj is None:
            return False
        translation = Mat3D.translation(tx, ty, tz)
        active_obj.do_transform(translation)
        return True

    def __scale_active_object(self, direction:float):
        active_obj = self.scene.get_active_object()
        if active_obj is None:
            return False
        
        scaling = Mat3D.scaling(direction, direction, direction)
        active_obj.do_transform(scaling)
        return True
        
    def __increase_subdivision(self) -> bool:
        active_obj = self.scene.get_active_object()
        if active_obj is None:
            return False
        mesh = active_obj.data
        if not isinstance(mesh, Mesh):
            return False

        mesh.increase_subdivision_level()
        mesh.apply_subdivision()
        return True
    
    def __decrease_subdivision(self) -> bool:
        active_obj = self.scene.get_active_object()
        if active_obj is None:
            return False
        mesh = active_obj.data
        if not isinstance(mesh, Mesh):
            return False
        mesh.decrease_subdivision_level()
        mesh.apply_subdivision()
        return True
    
    def __reset_camera(self) -> bool:
        cam_obj = self.scene.get_active_camera()
        if cam_obj is None:
            return False
        cam = cam_obj.data
        if not isinstance(cam, Camera):
            return False
        cam_obj.data = Camera(self.scene.default_camera_position, self.scene.default_camera_target, self.scene.default_camera_up)
        return True
        
    def __apply_yaw_pitch_rotation(self, relative_vec:Vec3D, yaw_axis:Vec3D, pitch_axis:Vec3D, angle_yaw:float, angle_pitch:float) -> Vec3D:
        rot_mat_yaw = Mat3D.rotation_around_axis(yaw_axis, angle_yaw)
        rot_pitch = Mat3D.rotation_around_axis(pitch_axis, angle_pitch)
        return (rot_pitch @ rot_mat_yaw) * relative_vec
        
    def __handle_orbit(self, dx:int, dy:int) -> bool:
        cam_obj = self.scene.get_active_camera()
        if cam_obj is None:
            return False
        cam = cam_obj.data
        if not isinstance(cam, Camera):
            return False

        position = cam.position
        target = cam.target
        world_up = Vec3D(0, 0, 1)

        rel_vec = position - target

        angle_yaw = -dx * self.__orbit_sentitivity
        angle_pitch = -dy * self.__orbit_sentitivity
        
        right_axis = rel_vec.normalize().cross(world_up).normalize()

        rotated_rel_vec = self.__apply_yaw_pitch_rotation(rel_vec, world_up, right_axis, angle_yaw, angle_pitch) 
        new_position = target + rotated_rel_vec
        cam.set_position(new_position)
        return True

    def __handle_pan(self, dx:int, dy:int) -> bool:
        cam_obj = self.scene.get_active_camera()
        if cam_obj is None:
            return False
        cam = cam_obj.data
        if not isinstance(cam, Camera):
            return False

        position = cam.position
        target = cam.target
        world_up = Vec3D(0, 0, 1)

        rel_vec = target - position

        angle_yaw = -dx * self.__pan_sensitivity
        angle_pitch = -dy * self.__pan_sensitivity

        fwd_vec = rel_vec.normalize()
        right_axis = fwd_vec.cross(world_up).normalize()
        cam_up = fwd_vec.cross(right_axis).normalize()
        
        rotated_rel_vec = self.__apply_yaw_pitch_rotation(rel_vec, cam_up, right_axis, angle_yaw, angle_pitch)

        new_target = position + rotated_rel_vec
        cam.set_target(new_target)
        
        return True

    def __handle_dolly(self, direction:int) -> bool:
        cam_obj = self.scene.get_active_camera()
        if cam_obj is None:
            return False
        cam = cam_obj.data
        if not isinstance(cam, Camera):
            return False

        position = cam.position
        target = cam.target
        
        rel_vec = target - position

        fwd = rel_vec.normalize()

        move_step = direction * self.__dolly_sensitivity
        
        new_position = position + fwd * move_step

        cam.set_position(new_position)
        return True


    def __handle_camera_movement(self, is_fwd:bool, direction:int) -> bool:
        cam_obj = self.scene.get_active_camera()
        if cam_obj is None:
            return False
        cam = cam_obj.data
        if not isinstance(cam, Camera):
            return False

        position = cam.position
        target = cam.target
        world_up = Vec3D(0, 0, 1)
        
        rel_vec = target - position

        fwd = rel_vec.normalize()
        if is_fwd:
            move_vec = fwd * direction
            cam.set_position(position + move_vec)
            cam.set_target(target + move_vec)
            return True
        
        right_vec = fwd.cross(world_up).normalize()

        move_vec = right_vec * direction
        cam.set_position(position + move_vec)
        cam.set_target(target + move_vec)
                
        return True
