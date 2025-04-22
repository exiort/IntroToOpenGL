# CENG 487 Assignment1 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from scene import Scene
from opengl import GLContext



def greeting():
    print("\n--- Controls ---")
    print(" Camera Movement:")
    print("  SHIFT + Up / Down        : Move Camera Forward / Backward")
    print("  SHIFT + Left / Right     : Strafe Camera Left / Right")
    print("  SHIFT + Left Mouse Drag  : Orbit Camera (Rotate around target)")
    print("  SHIFT + Right Mouse Drag : Pan Camera (Look around)")
    print("  Mouse Wheel              : Dolly Camera (Zoom In / Out)")
    print("  F                        : Reset Camera to Initial View")
    print("\n Object & Scene:")
    print("  A + 1                    : Add New Box (if no active object)")
    print("  A + 0                    : Load .obj file (if no active object)")
    print("  Delete                   : Remove Active Object")
    print("  Left / Right             : Rotate Active Object around z axis(WorldUp)")
    print("  Up / Down                : Rotate Active Object around y axis")
    print("  Alt + Left / Right       : Translate Active Object on y axis")
    print("  Alt + Up / Down          : Translate Active Object on x axis")
    print("  Ctrl + Up / Down         : Scale Active Object %10 on all axis")
    print("  +                        : Increase Subdivision Level (Active Object)")
    print("  -                        : Decrease Subdivision Level (Active Object)")
    print("  0                        : Toggle Grid Visibility")
    print("\n General:")
    print("  Q                        : Quit Application")
    print("  Z                        : Undo")
    print("  R                        : Redo")
    print("------------------")
    print()

def main():
    greeting()
    scene = Scene()

    context = GLContext(scene,width=1080, height=720)
    context.run()
    
if __name__ == "__main__":
    main()
