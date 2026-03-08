# Python Custom 3D Graphics Engine

## Overview

This project is a custom-built, lightweight 3D graphics application developed in Python. It serves as a comprehensive educational engine demonstrating core computer graphics principles from scratch. Bypassing heavy commercial libraries, this engine implements its own 3D mathematics, hierarchical scene management, procedural geometry generation, and a custom implementation of the Catmull-Clark subdivision surface algorithm. 

Rendering is handled via PyOpenGL using programmable shaders (GLSL) and Vertex Buffer Objects (VBOs), providing a modern, efficient graphics pipeline.

## Key Features

* **Custom Math Library (`math3d`)**: A standalone implementation of vector and matrix mathematics (`Vec2D`, `Vec3D`, `Vec4D`, `Mat3D`) handling perspective/orthographic projections, cross/dot products, and arbitrary axis rotations without relying on external math libraries.
* **Modern OpenGL Pipeline (`renderer` & `shaders`)**: Utilizes VAOs and VBOs for efficient batch rendering. Custom GLSL shaders support dual-texture blending and raw color rendering.
* **Dynamic Mesh Subdivision**: Implements the Catmull-Clark subdivision algorithm from scratch (`MeshAlgorithms`), featuring a robust caching system to smoothly toggle between subdivision levels in real-time.
* **Procedural Geometry Generation**: Built-in factories to procedurally generate complex 3D primitives including Tori, Spheres, Pyramids, Cylinders, Cubes, Tetrahedrons, and 2D shapes.
* **Hierarchical Scene Graph**: Manages objects via a `Scene` and `Collection` architecture, allowing for parent-child relationship management and visibility toggling.
* **Undo/Redo Transformation Stack**: A robust transformation manager utilizing `do_stack`, `redo_stack`, and `temporary_stack` matrices to allow seamless undo/redo of object translations, rotations, and scaling.
* **OBJ File Parsing**: A custom parser to load and reorient external 3D models from `.obj` files into the custom Winged-Edge inspired mesh structure.
* **State-Machine Input Handling**: A highly decoupled input system separating controls into distinct modes (Camera, Object, Scene) for a clean user experience.

## Project Architecture

* **`camera/`**: Viewport management supporting both perspective and orthographic projections.
* **`generators/`**: Procedural mesh factories for 2D and 3D primitives.
* **`geometry/`**: The core topological data structures (`Vertex`, `Edge`, `Face`, `Mesh`) and the Catmull-Clark subdivision logic.
* **`input_modes/`**: Context-aware input handling separating global, scene, object, and camera controls.
* **`math3d/`**: The proprietary linear algebra and matrix transformation library.
* **`object3d/`**: The primary entity node managing spatial transformations, materials, and linking data to the renderer.
* **`opengl/`**: FreeGLUT window context initialization, main loop timing, and raw input delegation.
* **`parser/`**: External `.obj` file loading and geometry extraction.
* **`renderer/`**: OpenGL state management, buffer generation, and draw calls.
* **`scene/`**: Global state management holding the active camera, collections, and world grid.
* **`shaders/`**: GLSL shader compilation, linking, and uniform caching.
* **`ui/`**: On-Screen Display (OSD) rendering using GLUT bitmap characters to show active states and help menus.

## Installation & Requirements

Ensure you have Python 3 installed. The project relies on the following dependencies for windowing, buffer management, and image loading:

```bash
pip install requirements.txt 
```

To launch the application, simply run the main entry point:

```bash
python main.py
```

## Controls

The application uses different interaction modes for various tasks. Press **`M`** to cycle through the active modes. The current active mode, object, and subdivision level are displayed on the OSD.

**Global Controls (Always Available)**
* **M**: Cycle interaction modes.
* **H**: Toggle Help Menu / Cycle Help Pages.
* **Esc**: Close Help Menu.
* **Q**: Quit Application.
* **Ctrl + Z**: Undo last object transformation.
* **Ctrl + Shift + Z**: Redo last object transformation.

**Camera Mode**
* **Alt + Left Mouse Drag**: Orbit Camera (Rotate around target).
* **Alt + Middle Mouse Drag**: Pan Camera.
* **Mouse Wheel**: Dolly Camera (Zoom In/Out).
* **F**: Reset Camera to Default Position.

**Object Mode**
* **+ (Plus)**: Increase Subdivision Level of Active Mesh.
* **- (Minus)**: Decrease Subdivision Level of Active Mesh.
* **Ctrl + '+' / '-'**: Adjust texture blending factor on the active material.
* **Ctrl + Mouse Drag**: Translate Active Object (LMB=X, RMB=Y, MMB=Z).
* **Alt + Mouse Drag**: Rotate Active Object (LMB=X, RMB=Y, MMB=Z).
* **Shift + Mouse Drag**: Scale Active Object (LMB=X, RMB=Y, MMB=Z).
* **X**: Cycle active focus through objects in the scene.

**Scene Mode**
* **Ctrl + 1**: Add Predefined Box Object.
* **Ctrl + 2**: Add Predefined Cylinder Object.
* **Ctrl + 3**: Add Predefined Pyramid Object.
* **Ctrl + 4**: Add Predefined Sphere Object.
* **Ctrl + 5**: Add Predefined Torus Object.
* **Ctrl + 6**: Add Predefined Tetrahedron Object.
* **Ctrl + O**: Load an external `.obj` file.
* **Delete**: Remove Active Object.
* **Ctrl + 0**: Toggle Grid Visibility.

## Technical Notes

* **Linux/Wayland Compatibility**: Modern Linux distributions using the Wayland display server may experience immediate crashes due to PyOpenGL's strict GLX tracking. If you experience context retrieval errors, a simple monkey-patch to PyOpenGL's `contextdata.getContext` is required in your entry file.
* **Performance**: The current Catmull-Clark subdivision implementation runs entirely on the CPU using Python. High subdivision levels (4+) on complex geometry may cause temporary freezes while the topology cache builds.

---

## 📜 License

This project is licensed under the MIT License. Copyright (c) 2026 Buğrahan İmal. You are free to use, copy, modify, merge, publish, and distribute this software as per the license conditions.
