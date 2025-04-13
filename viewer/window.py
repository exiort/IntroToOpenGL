# CENG 487 Assignment1 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from OpenGL.GL import (
    glClearColor, glClearDepth, glDepthFunc, glEnable, glShadeModel,
    glMatrixMode, glLoadIdentity, glViewport, GL_LESS,
    GL_DEPTH_TEST, GL_SMOOTH, GL_PROJECTION, GL_MODELVIEW
)
from OpenGL.GLUT import (
    glutInit, glutInitDisplayMode, glutInitWindowSize, glutInitWindowPosition,
    glutCreateWindow, glutDisplayFunc, glutIdleFunc, glutReshapeFunc,
    glutKeyboardFunc, glutMainLoop,
    GLUT_RGBA, GLUT_DOUBLE, GLUT_DEPTH
)
from OpenGL.GLU import gluPerspective

import sys
from .draw import draw_scene

GLUT_RGBA: int
GLUT_DOUBLE: int
GLUT_DEPTH: int

WINDOW = None
ESCAPE = 27

def init_gl(width:int, height:int) -> None:
    glClearColor(0, 0, 0, 0)
    glClearDepth(1)

    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(45, width, height, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)

def resize_gl_scene(width:int, height:int):
    if height == 0:
        height = 1

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width/height, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)
    
def key_pressed(key, x:int, y:int):
    if ord(key) == ESCAPE:
        sys.exit()

def run_viewer():
    global WINDOW

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow(b"Object Viewer")

    glutDisplayFunc(draw_scene)
    glutIdleFunc(draw_scene)
    glutReshapeFunc(resize_gl_scene)
    glutKeyboardFunc(key_pressed)

    init_gl(640, 480)
    glutMainLoop()
