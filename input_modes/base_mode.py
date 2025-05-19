from scene import Scene



class BaseMode:
    scene:Scene

    orbit_sensitivity:float
    pan_sensitivity:float
    dolly_sensitivity:float
    object_sensitivity:float

    mouse_state:dict[str, bool]
    last_mouse_position:dict[str, int]
    shift_key_pressed:bool
    ctrl_key_pressed:bool
    alt_key_pressed:bool

    
    def __init__(self, scene:Scene, orbit_sensitivity:float=0.008, pan_sensitivity:float=0.008, dolly_sensitivity:float=0.75, object_sensitivity:float=0.008) -> None:
        self.scene = scene
        self.orbit_sensitivity = orbit_sensitivity
        self.pan_sensitivity = pan_sensitivity
        self.dolly_sensitivity = dolly_sensitivity
        self.object_sensitivity = object_sensitivity

        self.shift_key_pressed = False
        self.ctrl_key_pressed = False
        self.alt_key_pressed = False
        self.mouse_state = {"l":False, "r":False, "m":False}
        self.last_mouse_position = {"x":0, "y":0}

    def handle_key_press(self, key:bytes) -> bool:
        if key == b'\x1a':
            if not self.ctrl_key_pressed:
                return False
            if self.shift_key_pressed:
                return self.__redo()
            return self.__undo()

        return False
        
    def handle_special_key_press(self, key:int) -> bool:
        if key == 112: #Shift
            self.shift_key_pressed = True
        elif key == 114: #Ctrl
            self.ctrl_key_pressed = True
        elif key == 116: #Alt
            self.alt_key_pressed = True
        return False
            
    def handle_special_key_release(self, key:int) -> None:
        if key == 112: #Shift
            self.shift_key_pressed = False
        elif key == 114: #Ctrl
            self.ctrl_key_pressed = False
        elif key == 116: #Alt
            self.alt_key_pressed = False
    
    def __undo(self) -> bool:
        active_object = self.scene.get_active_object()
        if active_object is None:
            return False

        active_object.undo_transform()
        return True

    def __redo(self) -> bool:
        active_object = self.scene.get_active_object()
        if active_object is None:
            return False

        active_object.redo_transform()
        return True
