# CENG 487 Assignment4 by
# Bugrahan Imal
# StudentId: 280201012
# May 2025
class UIManager:
    help_pages_content:list[dict[str, str|list[str]]] = [
        {
            "title":"HELP FOR INTERACTION MODES",
            "lines": [
                "This application uses different interaction modes for various tasks.",
                "Press 'M' to cycle through modes.",
                "The current active mode/active object/subdivision level is shown in the OSD."
                "",
                "GLOBAL CONTROLS (Always Available)",
                " H: Toggle Help Menu / Cycle Help Pages",
                " Q: Quit Application",
                " Ctrl + Z: Undo last object transformation (if an object is active)",
                " CTRL + SHIFT + Z: Redo last object transformation (if an object is active)"
            ]
        },
        {
            "title": "CAMERA MODE CONTROLS",
            "lines": [
                "Alt + Left Mouse Button Drag: Orbit Camera (Rotate Around Target)",
                "Alt + Middle Mouse Button Drag: Pan Camera",
                "Mouse Wheel: Dolly Camera (Zoom In/Out)",
                "F: Reset Camera to Default Position"
            ]
        },
        {
            "title": "OBJECT MODE CONTROLS",
            "lines": [
                "'+': Increase Subdivision Level of Active Mesh",
                "'-': Decrease Subdivision Level of Active Mesh",
                "Ctrl + LMB/RMB/MMB Drag: Translate Active Object (X/Y/Z)",
                "Alt + LMB/RMB/MMB Drag: Rotate Active Object (X/Y/Z)",
                "SHIFT + LMB/RMB/MMB Drag: Scale Active Object (X/Y/Z)" 
            ]
        },
        {
            "title": "SCENE MODE CONTROLS",
            "lines": [
                "Ctrl + 1: Add Predefined Box Object (if no object is active)",
                "Ctrl + 2: Add Predefined Cylinder Object (if no object is active)",
                "Ctrl + 3: Add Predefined Pyramid Object (if no object is active)",
                "Ctrl + 4: Add Predefined Sphere Object (if no object is active)",
                "Ctrl + 5: Add Predefined Torus Object (if no object is active)",
                "Ctrl + 6: Add Predefined Tetrahedron Object (if no object is active)",
                "Ctrl + O: Load an .obj file (if no object is active)",
                "Delete: Delete Active Object (if an object is active)",
                "Ctrl + 0: Toggle Grid Visibility"
            ]
        }
    ]
    
    is_help_visible:bool
    current_help_page_idx:int
    
    help_text_color:tuple[float, float, float, float]
    help_title_color:tuple[float, float, float, float]
    help_panel_bg_color:tuple[float, float, float, float]
    help_panel_border_color:tuple[float, float, float, float]
    
    osd_active_mode_name:str
    osd_active_object_name:str
    osd_active_object_subdivision:str

    osd_text_color:tuple[float, float, float, float]
    osd_title_color:tuple[float, float, float, float]
    osd_box_bg_color:tuple[float, float, float, float]
    osd_box_border_color:tuple[float, float, float, float]
    
    norm_padding:float = 0.015       
    norm_line_height:float = 0.03    
    norm_title_height:float = 0.04
    
    def __init__(self) -> None:
        self.is_help_visible = False
        self.current_help_page_idx = 0

        self.help_text_color = (0.9, 0.9, 0.9, 1)
        self.help_title_color = (1, 0.85, 0, 1)
        self.help_panel_bg_color = (0.1, 0.1, 0.12, 0.92)
        self.help_panel_border_color = (0.5, 0.5, 0.55, 1.0)

        self.osd_active_mode_name = "CAMERA MODE"
        self.osd_active_object_name = "None"
        self.osd_active_object_subdivision = "N/A"
        
        self.osd_text_color = (0.9, 0.9, 0.9, 1)
        self.osd_title_color = (1, 0.85, 0, 1)
        self.osd_box_bg_color = (0.15, 0.15, 0.15, 0.75)
        self.osd_box_border_color = (0.4, 0.4, 0.4, 1)

        self.norm_padding = 0.015       
        self.norm_line_height = 0.03    
        self.norm_title_height = 0.04   

    def handle_help_action(self, activate:bool) -> bool:
        if activate:
            if not self.is_help_visible:
                self.is_help_visible = True
                self.current_help_page_idx = 0
            else:
                self.current_help_page_idx = (self.current_help_page_idx + 1) % len(self.help_pages_content)
                
        else:
            self.is_help_visible = False
            self.current_help_page_idx = 0

        return True    

    def update_osd_data(self, active_mode_name:str|None=None, active_object_name:str|None=None, active_object_subdivision:str|None=None) -> bool:
        redraw_needed = False
        if active_mode_name is not None:
            self.osd_active_mode_name = active_mode_name
            redraw_needed = True

        if active_object_name is not None:
            self.osd_active_object_name = active_object_name
            redraw_needed = True
            
        if active_object_subdivision is not None:
            self.osd_active_object_subdivision = active_object_subdivision
            redraw_needed = True
            
        return redraw_needed
        
    def get_draw_commands(self) -> list[tuple]:
        commands:list[tuple] = []

        if self.is_help_visible:
            commands.extend(self.__prepare_help_menu_commands())
        else:
            commands.extend(self.__prepare_osd_commands())

        return commands
        
    def __prepare_osd_commands(self) -> list[tuple]:
        commands:list[tuple] = []

        osd_lines = [
            f"Active Mode: {self.osd_active_mode_name}",
            f"Active Object: {self.osd_active_object_name}",
            f"Subdivision Level: {self.osd_active_object_subdivision}",
            f"Help: h"
        ]

        box_w_norm = 0.25
        line_h_norm = self.norm_line_height
        pad_norm = self.norm_padding

        box_h_norm = (len(osd_lines) * line_h_norm) + (pad_norm * 2)
        box_x_norm = 1 - box_w_norm - pad_norm
        box_y_norm = pad_norm

        commands.append(
            ("RECT", box_x_norm, box_y_norm, box_w_norm, box_h_norm, self.osd_box_bg_color, self.osd_box_border_color, 1)
        )

        text_x_norm = box_x_norm + (pad_norm / 2)
        current_y_norm = box_y_norm + (pad_norm / 2) + line_h_norm * 0.8

        for line in osd_lines:
            commands.append(
                ("TEXT", line, text_x_norm, current_y_norm, self.osd_text_color)
            )
            current_y_norm += line_h_norm
        
        return commands

    def __prepare_help_menu_commands(self) -> list[tuple]:
        commands:list[tuple] = []

        page_data = self.help_pages_content[self.current_help_page_idx]
        title = page_data["title"]
        content_lines = page_data["lines"]

        margin_norm = 0.05
        panel_x_norm = margin_norm
        panel_y_norm = margin_norm
        panel_w_norm = 1 - (2 * margin_norm)
        panel_h_norm = 1 - (2 * margin_norm)

        text_pad_norm = self.norm_padding * 2
        line_h_norm = self.norm_line_height
        title_h_norm = self.norm_title_height

        commands.append(
            ("RECT", panel_x_norm, panel_y_norm, panel_w_norm, panel_h_norm, self.help_panel_bg_color, self.help_panel_border_color, 1)
        )

        current_y_norm = panel_y_norm + text_pad_norm + title_h_norm * 0.8
        text_x_norm = panel_x_norm + text_pad_norm

        commands.append(
            ("TEXT", title, text_x_norm, current_y_norm, self.help_title_color)
        )

        current_y_norm += line_h_norm * 1.5
        for line in content_lines:
            if current_y_norm + line_h_norm > panel_y_norm + panel_h_norm - text_pad_norm:
                commands.append(("TEXT", "...", text_x_norm, current_y_norm, self.help_text_color))
                break 
            commands.append(("TEXT", line, text_x_norm, current_y_norm, self.help_text_color))
            current_y_norm += line_h_norm
        
        return commands
