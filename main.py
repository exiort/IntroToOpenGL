# CENG 487 Assignment1 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

# --- WAYLAND COMPATIBILITY PATCH ---
# PyOpenGL's glXGetCurrentContext returns 0 on Wayland, causing a hard crash.
# Since we only have one window, we intercept the tracker and mock the ID to 1.
from OpenGL import contextdata

def patched_get_context(context=None):
    return context if context is not None else 1

contextdata.getContext = patched_get_context

from opengl import GLContext



def main():
    context = GLContext(width=1080, height=720)
    context.run()
    
if __name__ == "__main__":
    main()
