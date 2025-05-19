# CENG 487 Assignment1 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from scene import Scene
from opengl import GLContext



def main():
    scene = Scene()
    context = GLContext(scene,width=1080, height=720)
    context.run()
    
if __name__ == "__main__":
    main()
