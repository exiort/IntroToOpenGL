# CENG 487 Assignment1 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from OpenGL.GL import (
    glClear, glLoadIdentity, glTranslatef, glBegin, glVertex3f, glEnd,
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_POLYGON
)
from OpenGL.GLUT import glutSwapBuffers
GL_COLOR_BUFFER_BIT:int
GL_DEPTH_BUFFER_BIT:int

from generators import create_triangle, create_square
from transform import rotate_around_vec
from math3d import Mat3D
from utils import Timer

import math

triangle = create_triangle()
triangle.do_transform(Mat3D.translation(-2, 0, 0))
triangle.apply_transform()
triangle_pivot = triangle.data.vertices[0].possition

square = create_square()
square.do_transform(Mat3D.translation(2, 0, 0))
square.apply_transform()
square_pivot = square.data.vertices[0].possition

rotation_angle = 0.0
FPS = 30

timer = Timer(FPS)

print(triangle_pivot)
print(triangle.data.vertices)
def draw_scene():
    global rotation_angle

    if not timer.is_next_frame():
        return
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0, -6)

    rotation_angle = (rotation_angle + 0.01) % (2*math.pi) 

    rotate_matrix = rotate_around_vec("z", rotation_angle, triangle_pivot)
    triangle.do_transform(rotate_matrix)
    baked_triangle = triangle.bake()
    triangle.clear_transform()

    rotate_matrix = rotate_around_vec("z", rotation_angle, square_pivot)
    square.do_transform(rotate_matrix)
    baked_square = square.bake()
    square.clear_transform()
    
    glBegin(GL_POLYGON)
    for v in baked_triangle.data.vertices:
        glVertex3f(v.possition.x, v.possition.y, v.possition.z)
    glEnd()

    glBegin(GL_POLYGON)
    for v in baked_square.data.vertices:
        glVertex3f(v.possition.x, v.possition.y, v.possition.z)
    glEnd()
    
    
    glutSwapBuffers()

 
