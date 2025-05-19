from geometry.mesh import Mesh
from .base_mode import BaseMode
from math3d import Mat3D



class ObjectMode:
    base_mode:BaseMode
    
    def __init__(self, base_mode:BaseMode) -> None:
        self.base_mode = base_mode

        
    def handle_key_press(self, key:bytes) -> bool:
        if key == b'+':
            return self.__handle_subdivision(True)
        elif key == b'-':
            return self.__handle_subdivision(False)
        
        return self.base_mode.handle_key_press(key)
    
    def handle_special_key_press(self, key:int) -> bool:
        return self.base_mode.handle_special_key_press(key)

    def handle_special_key_release(self, key:int) -> None:
       self.base_mode.handle_special_key_release(key)

    def handle_mouse_wheel(self, direction:int) -> bool:
        return False

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
            elif button == 2:self.base_mode.mouse_state["m"] = False
            self.__finalize()
            
        return False
            
    def handle_mouse_drag(self, x:int, y:int) -> bool:        
        if not self.base_mode.alt_key_pressed and not self.base_mode.ctrl_key_pressed and not self.base_mode.shift_key_pressed:
            return False

        redraw_needed = False
        dx = (self.base_mode.last_mouse_position["x"] - x) * self.base_mode.object_sensitivity
        dy = (self.base_mode.last_mouse_position["y"] - y) * self.base_mode.object_sensitivity
        
        if self.base_mode.ctrl_key_pressed:
            if self.base_mode.mouse_state["l"]:
                redraw_needed = self.__handle_translation("x", dx)
            elif self.base_mode.mouse_state["r"]:
                redraw_needed = self.__handle_translation("y", dy)
            elif self.base_mode.mouse_state["m"]:
                redraw_needed = self.__handle_translation("z", dy)
            
        elif self.base_mode.alt_key_pressed:
            if self.base_mode.mouse_state["l"]:
                redraw_needed = self.__handle_rotation("x", dx)
            elif self.base_mode.mouse_state["r"]:
                redraw_needed = self.__handle_rotation("y", dy)
            elif self.base_mode.mouse_state["m"]:
               redraw_needed = self.__handle_rotation("z", dy)

        elif self.base_mode.shift_key_pressed:
            if self.base_mode.mouse_state["l"]:
                redraw_needed = self.__handle_scaling("x", dx)
            elif self.base_mode.mouse_state["r"]:
                redraw_needed = self.__handle_scaling("y", dy)
            elif self.base_mode.mouse_state["m"]:
                redraw_needed = self.__handle_scaling("z", dy)
        
        self.base_mode.last_mouse_position["x"] = x
        self.base_mode.last_mouse_position["y"] = y
        
        return redraw_needed

    def __handle_translation(self, axis:str, d:float) -> bool:
        active_obj = self.base_mode.scene.get_active_object()
        if active_obj is None:
            return False
        if axis not in ["x", "y", "z"]:
            return False

        translation_mat = Mat3D.identity()
        if axis == "x":
            translation_mat = Mat3D.translation(d, 0, 0)
        elif axis == "y":
            translation_mat = Mat3D.translation(0, d, 0)
        elif axis == "z":
            translation_mat = Mat3D.translation(0, 0, d)

        active_obj.do_temporary(translation_mat)
        return True
    
    def __handle_rotation(self, axis:str, d:float) -> bool:
        active_obj = self.base_mode.scene.get_active_object()
        if active_obj is None:
            return False
        if axis not in ["x", "y", "z"]:
            return False

        rotation_mat = Mat3D.rotation(axis, d)
        active_obj.do_temporary(rotation_mat)
        return True

    def __handle_scaling(self, axis:str, d:float) -> bool:
        active_obj = self.base_mode.scene.get_active_object()
        if active_obj is None:
            return False
        if axis not in ["x", "y", "z"]:
            return False
        
        scale_mat = Mat3D.identity()
        if axis == "x":
            scale_mat = Mat3D.scaling(max(0.05, 1 + d), 1, 1)
        elif axis == "y":
            scale_mat = Mat3D.scaling(1, max(0.05, 1 + d), 1)
        elif axis == "z":
            scale_mat = Mat3D.scaling(1, 1, max(0.05, 1 + d))

        active_obj.do_temporary(scale_mat)
        return True

    def __finalize(self) -> bool:
        active_obj = self.base_mode.scene.get_active_object()
        if active_obj is None:
            return False
        active_obj.finalize_temporary()
        return True
    
    def __handle_subdivision(self, increase:bool) -> bool:
        active_obj = self.base_mode.scene.get_active_object()
        if active_obj is None:
            return False
        mesh = active_obj.data
        if not isinstance(mesh, Mesh):
            return False

        if increase:
            mesh.increase_subdivision_level()
        else:
            mesh.decrease_subdivision_level()
            
        mesh.apply_subdivision()
        return True
        
