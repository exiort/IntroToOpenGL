# CENG 487 Assignment2 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from OpenGL.GL import (
    GL_LINE_LOOP, GL_QUADS, glBegin, glClear, glClearColor, glClearDepth, glColor3f, glColor4f, glDepthFunc,
    glDisable, glEnable, glEnd, glLineWidth, glLoadIdentity, glMatrixMode, glPopMatrix,
    glPushMatrix, glRasterPos2f, glShadeModel, glVertex2f, glViewport,
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST, GL_LESS,
    GL_MODELVIEW, GL_PROJECTION, GL_SMOOTH
)
from OpenGL.GLU import gluOrtho2D

from OpenGL.GLUT import (
    GLUT_DEPTH, GLUT_DOUBLE, GLUT_RGBA,
    GLUT_DOWN, GLUT_BITMAP_HELVETICA_18,# type: ignore
    GLUT_LEFT_BUTTON, GLUT_MIDDLE_BUTTON, GLUT_RIGHT_BUTTON, GLUT_SCREEN_HEIGHT, GLUT_SCREEN_WIDTH,
    glutBitmapCharacter,
    glutCreateWindow, glutDisplayFunc, glutFullScreen, glutGet, glutIdleFunc,
    glutInit, glutInitDisplayMode, glutInitWindowSize,
    glutKeyboardFunc, glutKeyboardUpFunc,
    glutLeaveMainLoop, glutMainLoop, glutMotionFunc, glutMouseFunc,
    glutMouseWheelFunc, glutPostRedisplay, glutReshapeFunc,
    glutSpecialFunc, glutSpecialUpFunc, glutSwapBuffers
)
from OpenGL.raw.GLUT import GLUT_DOWN

from camera.camera import Camera

GLUT_RGBA:int
GLUT_DOUBLE:int
GLUT_DEPTH:int
GL_COLOR_BUFFER_BIT:int
GL_DEPTH_BUFFER_BIT:int

from geometry.mesh import Mesh
from scene import Scene
from ui import UIManager
from .renderer import Renderer
from .timer import Timer
from .input_handler import InputHandler



class GLContext:
    width:int
    height:int
    title:str

    scene:Scene
    timer:Timer

    input_handler:InputHandler
    ui_manager:UIManager
    
    def __init__(self, scene:Scene, title:str="3D", width:int=640, height:int=480, FPS:int=30) -> None:
        self.scene = scene
        self.title = title
        self.width = width
        self.height = height
        self.timer = Timer(FPS)

        self.input_handler = InputHandler(self.scene)
        self.ui_manager = UIManager()

    def run(self) -> None:
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

        try:
            screen_w = glutGet(GLUT_SCREEN_WIDTH)
            screen_h = glutGet(GLUT_SCREEN_HEIGHT)

            self.width = screen_w
            self.height = screen_h
        except Exception as e:
            print(e)
            
        glutInitWindowSize(self.width, self.height)
        glutCreateWindow(self.title.encode())
        glutFullScreen()
        self.init_gl()
        
        glutDisplayFunc(self.display)
        glutIdleFunc(self.display)
        glutReshapeFunc(self.reshape)
        glutKeyboardFunc(self.__glut_keyboard_handler)
        glutSpecialFunc(self.__glut_special_key_handler)
        glutSpecialUpFunc(self.__glut_special_key_up_handler)
        glutMouseFunc(self.__glut_mouse_button_handler)
        glutMotionFunc(self.__glut_mouse_drag_handler)
        glutMouseWheelFunc(self.__glut_mouse_wheel_handler)
        glutMainLoop()

    def init_gl(self) -> None:
        glClearColor(0.1, 0.1, 0.1, 0.1)
        glClearDepth(1)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)

    def display(self) -> None:
        if not self.timer.is_next_frame():
            return
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Renderer.render_scene(self.scene)

        
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0.0, self.width, 0.0, self.height) # (0,0) sol alt
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glDisable(GL_DEPTH_TEST)         
        active_mode_name = self.input_handler.active_mode_names[self.input_handler.active_mode]
        active_obj = self.scene.get_active_object()
        obj_name = active_obj.name if active_obj else "None"
        subdiv_str = str(active_obj.data.current_subdivision_level) if active_obj and isinstance(active_obj.data, Mesh) else "N/A"
        self.ui_manager.update_osd_data(active_mode_name, obj_name, subdiv_str)
        draw_commands = self.ui_manager.get_draw_commands()

        text_commands = [cmd for cmd in draw_commands if cmd[0] == "TEXT"]
        rect_commands = [cmd for cmd in draw_commands if cmd[0] == "RECT"]

        for cmd_type, *args in rect_commands:
            self.__draw_ui_rect(*args)

        for cmd_type, *args in text_commands:
            self.__draw_ui_text(*args)

        glEnable(GL_DEPTH_TEST) # Derinlik testini geri etkinleştir
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glutSwapBuffers()
        

    def reshape(self, width:int, height:int) -> None:
        glViewport(0, 0, width, height)
        self.width = width
        self.height = height
        if self.scene and self.scene.active_camera:
            camera_object = self.scene.get_active_camera()
            if camera_object.data and isinstance(camera_object.data, Camera):
                camera = camera_object.data
                new_aspect_ratio = float(width) / float(height)
                camera.aspect_ratio = new_aspect_ratio
                camera.is_proj_dirty = True
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
    def set_scene(self, scene:Scene) -> None:
        self.scene = scene
        self.input_handler = InputHandler(self.scene)

    def __draw_ui_text(self, text:str, norm_x:float, norm_y:float, color:tuple[float, float, float, float]) -> None:
        pixel_x = norm_x * self.width
        pixel_y = (1 - norm_y) * self.height

        glColor4f(color[0], color[1], color[2], color[3])
        glRasterPos2f(pixel_x, pixel_y)

        font = GLUT_BITMAP_HELVETICA_18
        for char_code in text.encode('latin-1', 'replace'):
            glutBitmapCharacter(font, char_code)

    def __draw_ui_rect(self, norm_x:float, norm_y:float, norm_w:float, norm_h:float, bg_color:tuple[float, float, float, float], border_color:tuple[float, float, float, float], border_width:float) -> None:
        pixel_x = norm_x * self.width
        pixel_w = norm_w * self.width
        pixel_h = norm_h * self.height
        
        pixel_y_bottom = (1 - norm_y - norm_h) * self.height

        glColor4f(bg_color[0], bg_color[1], bg_color[2], bg_color[3])
        glBegin(GL_QUADS)
        glVertex2f(pixel_x, pixel_y_bottom)
        glVertex2f(pixel_x + pixel_w, pixel_y_bottom)
        glVertex2f(pixel_x + pixel_w, pixel_y_bottom + pixel_h)
        glVertex2f(pixel_x, pixel_y_bottom + pixel_h)
        glEnd()

        glColor4f(border_color[0], border_color[1], border_color[2], border_color[3] if len(border_color) > 3 else 1.0)
        glLineWidth(border_width)
        glBegin(GL_LINE_LOOP)
        glVertex2f(pixel_x, pixel_y_bottom)
        glVertex2f(pixel_x + pixel_w, pixel_y_bottom)
        glVertex2f(pixel_x + pixel_w, pixel_y_bottom + pixel_h)
        glVertex2f(pixel_x, pixel_y_bottom + pixel_h)
        glEnd()
        glLineWidth(1.0)
        
    def __glut_keyboard_handler(self, key:bytes, x:int, y:int) -> None:
        print(key)
        key = key.lower()

        if key == b'q':
            glutLeaveMainLoop()
            return
        elif key == b'h':
            self.ui_manager.handle_help_action(True)
        elif key == b'\x1b':
            self.ui_manager.handle_help_action(False)
        
        redraw_needed = self.input_handler.handle_key_press(key)
        if redraw_needed: glutPostRedisplay()
  
    def __glut_special_key_handler(self, key:int, x:int, y:int) -> None:
        redraw_needed = self.input_handler.handle_special_key_press(key)
        if redraw_needed: glutPostRedisplay()
        
    def __glut_special_key_up_handler(self, key:int, x:int, y:int) -> None:
        self.input_handler.handle_special_key_release(key)
        
    def __glut_mouse_button_handler(self, button:int, state:int, x:int, y:int) -> None:
        generic_button = -1
        if button == GLUT_LEFT_BUTTON: generic_button = 0
        elif button == GLUT_RIGHT_BUTTON: generic_button = 1
        elif button == GLUT_MIDDLE_BUTTON: generic_button = 2

        is_pressed = (state == GLUT_DOWN)
        self.input_handler.handle_mouse_button(generic_button, is_pressed, x, y)

    def __glut_mouse_drag_handler(self, x:int, y:int) -> None:
        redraw_needed = self.input_handler.handle_mouse_drag(x, y)
        if redraw_needed: glutPostRedisplay()

    def __glut_mouse_wheel_handler(self, wheel:int, direction:int, x:int, y:int) -> None:
        redraw_needed = self.input_handler.handle_mouse_wheel(direction)
        if redraw_needed: glutPostRedisplay()

   
