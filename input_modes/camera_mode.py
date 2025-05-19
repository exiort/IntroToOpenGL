# CENG 487 Assignment4 by
# Bugrahan Imal
# StudentId: 280201012
# May 2025
from .base_mode import BaseMode
from camera import Camera
from math3d import Mat3D


class CameraMode:
    base_mode:BaseMode


    def __init__(self, base_mode:BaseMode) -> None:
        self.base_mode = base_mode

    def handle_key_press(self, key:bytes) -> bool:
        if key == b'f':
            return self.__reset_camera()
        
        return self.base_mode.handle_key_press(key)
    
    def handle_special_key_press(self, key:int) -> bool:
        return self.base_mode.handle_special_key_press(key)

    def handle_special_key_release(self, key:int) -> None:
        self.base_mode.handle_special_key_release(key)

    def handle_mouse_wheel(self, direction:int) -> bool:
        return self.__handle_dolly(direction)

    def handle_mouse_button(self, button:int, is_pressed:bool, x:int, y:int) -> bool:
        if is_pressed:
            self.base_mode.last_mouse_position["x"] = x
            self.base_mode.last_mouse_position["y"] = y

            if button == 0: self.base_mode.mouse_state["l"] = True
            elif button == 1: self.base_mode.mouse_state["r"] = True
            elif button == 2: self.base_mode.mouse_state["m"] = True

        else:
            if button == 0: self.base_mode.mouse_state["l"] = False
            elif button == 1: self.base_mode.mouse_state["r"] = False
            elif button == 2: self.base_mode.mouse_state["m"] = False

        return False
    
    def handle_mouse_drag(self, x:int, y:int) -> bool:
        if not self.base_mode.alt_key_pressed:
            return False

        redraw_needed = False
        dx = self.base_mode.last_mouse_position["x"] - x
        dy = self.base_mode.last_mouse_position["y"] - y

        if self.base_mode.mouse_state["l"]:
            redraw_needed = self.__handle_orbit(dx, dy)
        elif self.base_mode.mouse_state["r"]:
            pass
        elif self.base_mode.mouse_state["m"]:
            redraw_needed = self.__handle_pan(dx, dy)

        self.base_mode.last_mouse_position["x"] = x
        self.base_mode.last_mouse_position["y"] = y
        
        return redraw_needed
        
    def __reset_camera(self) -> bool:
        cam_obj = self.base_mode.scene.get_active_camera()
        cam = cam_obj.data
        if not isinstance(cam, Camera):
            return False
        
        cam.set_target(self.base_mode.scene.default_camera_target)
        cam.set_position(self.base_mode.scene.default_camera_position)
        cam.set_up(self.base_mode.scene.default_camera_up)
        return True
    
    def __handle_orbit(self, dx:int, dy:int) -> bool:
        cam_obj = self.base_mode.scene.get_active_camera()
        cam = cam_obj.data
        if not isinstance(cam, Camera):
            return False
        
        position = cam.position
        target = cam.target
        up = cam.up
        
        offset_vec = position - target      
        right_vec = offset_vec.normalize().cross(up).normalize()
        corrected_up_vec = right_vec.cross(offset_vec.normalize()).normalize()

        angle_yaw = dx * self.base_mode.orbit_sensitivity
        angle_pitch = -dy * self.base_mode.orbit_sensitivity
        
        yaw_mat = Mat3D.rotation_around_axis(corrected_up_vec, angle_yaw)
        pitch_mat = Mat3D.rotation_around_axis(right_vec, angle_pitch)

        rot_mat = pitch_mat @ yaw_mat
        rotated_offset_vec = rot_mat * offset_vec
   
        cam.set_position(target + rotated_offset_vec)
        
        return True

    def __handle_pan(self, dx:int, dy:int) -> bool:
        cam_obj = self.base_mode.scene.get_active_camera()
        cam = cam_obj.data
        if not isinstance(cam, Camera):
            return False

        position = cam.position
        target = cam.target
        up = cam.up

        offset_vec = (position - target).normalize()
        right_vec = offset_vec.cross(up).normalize()
        corrected_up = right_vec.cross(offset_vec).normalize()

        move_x = -dx * self.base_mode.pan_sensitivity
        move_y = -dy * self.base_mode.pan_sensitivity

        pan_vec = (right_vec * move_x) + (corrected_up * move_y)

        cam.set_position(position + pan_vec)
        cam.set_target(target + pan_vec)

        return True

    def __handle_dolly(self, direction:int) -> bool:
        cam_obj = self.base_mode.scene.get_active_camera()
        cam = cam_obj.data
        if not isinstance(cam, Camera):
            return False

        position = cam.position
        target = cam.target

        if (target-position).magnitude() <= 0.1:
            return False
        
        forward = (target-position).normalize()

        dolly_step = direction * self.base_mode.dolly_sensitivity
        cam.set_position(position + forward * dolly_step)
        
        return True
