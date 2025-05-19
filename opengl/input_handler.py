# CENG 487 Assignment2 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025
from input_modes import BaseMode, CameraMode, ObjectMode, SceneMode
from scene import Scene


class InputHandler:
    modes:list[CameraMode|ObjectMode|SceneMode]
    active_mode:int
    active_mode_names:list[str] = ["CameraMode", "ObjectMode", "SceneMode"]
    
    def __init__(self, scene:Scene, orbit_sensitivity:float=0.01, pan_sensitivity:float=0.01, dolly_sensitivity:float=0.75, object_sensitivity:float=0.01) -> None:
        base_mode = BaseMode(scene, orbit_sensitivity, pan_sensitivity, dolly_sensitivity, object_sensitivity)
        self.modes = []
        self.modes.append(CameraMode(base_mode))
        self.modes.append(ObjectMode(base_mode))
        self.modes.append(SceneMode(base_mode))
        self.active_mode = 0

    def handle_key_press(self, key:bytes) -> bool:
        print(f"key presss: key_char={key}")
        if key.lower() == b'm':
            self.active_mode = (self.active_mode + 1) % len(self.modes)
            print(f"activemode:{self.active_mode}")
            return False
        
        return self.modes[self.active_mode].handle_key_press(key)

    def handle_special_key_press(self, key:int) -> bool:
        print(f"special press: key={key}")
        return self.modes[self.active_mode].handle_special_key_press(key)

    def handle_special_key_release(self, key:int) -> None:
        print(f"special release: key={key}")
        self.modes[self.active_mode].handle_special_key_release(key)

    def handle_mouse_wheel(self, direction:int) -> bool:
        print(f"wheel: direction={direction}")
        return self.modes[self.active_mode].handle_mouse_wheel(direction)

    def handle_mouse_button(self, button:int, is_pressed:bool, x:int, y:int) -> bool:
        print(f"button: button={button}, is_pressed={is_pressed}, x={x}, y={y}")
        return self.modes[self.active_mode].handle_mouse_button(button, is_pressed, x, y)

    def handle_mouse_drag(self, x:int, y:int) -> bool:
        print(f"drag:x={x}, y={y}")
        return self.modes[self.active_mode].handle_mouse_drag(x, y)
    
