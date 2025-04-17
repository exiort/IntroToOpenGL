# CENG 487 Assignment2 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from generators import create_box
from geometry import Mesh
from math3d import Vec3D, Mat3D
from scene import Scene
from camera import Camera
from object3d import Object3D
import sys

class InputHandler:
    scene:Scene
    
    __orbit_sentitivity:float
    __pan_sensitivity:float
    __dolly_sensitivity:float
    
    __mouse_state:dict[str, bool]
    __last_mouse_position:dict[str,int]

    __active_object:Object3D|None
    
    def __init__(self, scene:Scene, orbit_sensitivity:float=0.008, pan_sensitivity:float=0.008, dolly_sensitivity:float=0.75) -> None:
        self.scene = scene

        self.__mouse_state = {"left":False, "right":False, "middle":False}
        self.__last_mouse_position = {"x":0, "y":0}
        
        self.__orbit_sentitivity = orbit_sensitivity
        self.__pan_sensitivity = pan_sensitivity
        self.__dolly_sensitivity = dolly_sensitivity

        self.__active_object = None
        
    def handle_key_press(self, key_char:str) -> bool:
        if key_char == "q" or key_char == "Q":
            sys.exit()
            
        elif key_char in ["w", "W", "a", "A", "s", "S", "d", "D"]:
            if key_char == "w" or key_char == "W":
                return self.__handle_movement(True, 1)
            elif key_char == "s" or key_char == "S":
                return self.__handle_movement(True, -1)
            elif key_char == "a" or key_char == "A":
                return self.__handle_movement(False, -1)
            elif key_char == "d" or key_char == "D":
                return self.__handle_movement(False, 1)
        elif key_char == "f" or key_char == "F":
            return self.__reset_camera()
        elif key_char == "0":
            self.scene.change_grid_visibility()
            return True
        elif key_char == "1":
            return self.__add_object()
        elif key_char == "2":
            return self.__remove_object()
        elif key_char == "+":
            return self.__increase_subdivision()
        elif key_char == "-":
            return self.__decrease_subdivision()
        
        return False
    
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

    def __add_object(self) -> bool:
        if self.__active_object is not None:
            return False
        
        self.__active_object = create_box("Box", 10, 10, 10)
        self.scene.add_object(self.__active_object)
        return True

    def __remove_object(self) -> bool:
        if self.__active_object is None:
            return False
        self.scene.remove_object(self.__active_object)
        self.__active_object = None
        return True

    def __increase_subdivision(self) -> bool:
        if self.__active_object is None:
            return False
        mesh = self.__active_object.data
        if not isinstance(mesh, Mesh):
            return False

        mesh.increase_subdivision_level()
        mesh.apply_subdivision()
        return True
    
    def __decrease_subdivision(self) -> bool:
        if self.__active_object is None:
            return False
        mesh = self.__active_object.data
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


    def __handle_movement(self, is_fwd:bool, direction:int) -> bool:
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
