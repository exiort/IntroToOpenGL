# CENG 487 Assignment2 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from OpenGL.GL import (
    glClear, glClearColor, glClearDepth, glColor3f, glDepthFunc,
    glDisable, glEnable, glLoadIdentity, glMatrixMode, glPopMatrix,
    glPushMatrix, glRasterPos2f, glShadeModel, glViewport,
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST, GL_LESS,
    GL_MODELVIEW, GL_PROJECTION, GL_SMOOTH
)
from OpenGL.GLU import gluOrtho2D

from OpenGL.GLUT import (
    GLUT_DEPTH, GLUT_DOUBLE, GLUT_RGBA,
    GLUT_DOWN, GLUT_BITMAP_HELVETICA_18,# type: ignore
    GLUT_LEFT_BUTTON, GLUT_MIDDLE_BUTTON, GLUT_RIGHT_BUTTON,
    glutBitmapCharacter,
    glutCreateWindow, glutDisplayFunc, glutIdleFunc,
    glutInit, glutInitDisplayMode, glutInitWindowSize,
    glutKeyboardFunc, glutKeyboardUpFunc,
    glutLeaveMainLoop, glutMainLoop, glutMotionFunc, glutMouseFunc,
    glutMouseWheelFunc, glutPostRedisplay, glutReshapeFunc,
    glutSpecialFunc, glutSpecialUpFunc, glutSwapBuffers
)
from OpenGL.raw.GLUT import GLUT_DOWN

GLUT_RGBA:int
GLUT_DOUBLE:int
GLUT_DEPTH:int
GL_COLOR_BUFFER_BIT:int
GL_DEPTH_BUFFER_BIT:int

from .renderer import Renderer
from scene import Scene
from .timer import Timer
from .input import InputHandler



class GLContext:
    width:int
    height:int
    title:str

    scene:Scene
    timer:Timer

    input_handler:InputHandler
    
    def __init__(self, scene:Scene, title:str="3D", width:int=640, height:int=480, FPS:int=30) -> None:
        self.scene = scene
        self.title = title
        self.width = width
        self.height = height
        self.timer = Timer(FPS)

        self.input_handler = InputHandler(self.scene)

    def __glut_keyboard_handler(self, key:bytes, x:int, y:int) -> None:
        key_char = key.decode().lower()

        if key_char == "q":
            glutLeaveMainLoop()
            return
        
        redraw_needed = self.input_handler.handle_key_press(key_char)
        if redraw_needed: glutPostRedisplay()

    def __glut_keyboard_up_handler(self, key:bytes, x:int, y:int) -> None:
        key_char = key.decode().lower()
        self.input_handler.handle_key_release(key_char)
        
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

    def __draw_overlay_text(self, text: str, x: int, y: int):
        try:
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            gluOrtho2D(0.0, self.width, 0.0, self.height)
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()
            glDisable(GL_DEPTH_TEST)
            glColor3f(1.0, 1.0, 1.0)
            glRasterPos2f(x, y)
            font = GLUT_BITMAP_HELVETICA_18
            for char in text:
                glutBitmapCharacter(font, ord(char))
            glEnable(GL_DEPTH_TEST)
            glPopMatrix()
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)
        except Exception as e:
            print(f"Error drawing overlay text: {e}")
            
    def set_scene(self, scene:Scene) -> None:
        self.scene = scene
        self.input_handler = InputHandler(self.scene)

    def init_gl(self) -> None:
        glClearColor(0.1, 0.1, 0.1, 0.1)
        glClearDepth(1)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)

    def reshape(self, width:int, height:int) -> None:
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.width = width
        self.height = height
        
    def display(self) -> None:
        if not self.timer.is_next_frame():
            return
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Renderer.render_scene(self.scene)

        level = self.input_handler.get_current_sub_division_level()
        if level != -1:
            self.__draw_overlay_text(f"Subdivision Level: {level}", 10, 10)
        
        glutSwapBuffers()
        
    def run(self) -> None:
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)
        glutCreateWindow(self.title.encode())

        self.init_gl()
        self.reshape(self.width, self.height)
        
        glutDisplayFunc(self.display)
        glutIdleFunc(self.display)
        glutReshapeFunc(self.reshape)
        glutKeyboardFunc(self.__glut_keyboard_handler)
        glutKeyboardUpFunc(self.__glut_keyboard_up_handler)
        glutSpecialFunc(self.__glut_special_key_handler)
        glutSpecialUpFunc(self.__glut_special_key_up_handler)
        glutMouseFunc(self.__glut_mouse_button_handler)
        glutMotionFunc(self.__glut_mouse_drag_handler)
        glutMouseWheelFunc(self.__glut_mouse_wheel_handler)
        glutMainLoop()
