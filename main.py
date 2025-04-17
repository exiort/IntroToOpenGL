# CENG 487 Assignment1 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from scene import Scene
from opengl import GLContext



def greeting():
    print("\n--- Controls ---")
    print(" Camera Movement:")
    print("  W / S : Move Camera Forward / Backward")
    print("  A / D : Strafe Camera Left / Right")
    print("  X + Left Mouse Drag  : Orbit Camera (Rotate around target)")
    print("  X + Right Mouse Drag : Pan Camera (Look around)")
    print("  Mouse Wheel          : Dolly Camera (Zoom In / Out)")
    print("  F                    : Reset Camera to Initial View")
    print("\n Object & Scene:")
    print("  1                    : Add New Box (if no active object)")
    print("  2                    : Remove Active Box")
    print("  +                    : Increase Subdivision Level (Active Object)")
    print("  -                    : Decrease Subdivision Level (Active Object)")
    print("  0                    : Toggle Grid Visibility")
    print("\n General:")
    print("  Q                    : Quit Application")
    print("------------------")

def main():
    greeting()
    scene = Scene()

    context = GLContext(scene,width=1080, height=720)
    context.run()
    
if __name__ == "__main__":
    main()
