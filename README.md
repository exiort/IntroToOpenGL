# Object3D Transformations and Geometry Project

## Overview

This project implements a 3D graphics application foundation featuring hierarchical scene management, an interactive camera, stack-based transformations, procedural geometry generation, and dynamic mesh subdivision. Key components include:

- **Scene / Collection**: Manages a hierarchy of 3D objects within the scene.
- **Object3D**: Core structure for scene nodes, holding transformation data (position, rotation, scale) and linking to geometry or camera data. Using a matrix stack for transformations.
- **Camera**: Represents the viewpoint, handling view and projection matrix calculations (including perspective and orthographic). Supports interactive controls.
- **Mesh / Geometry**: Represents 3D shapes using vertices, edges, and faces. The `Mesh` class now includes infrastructure for dynamic subdivision levels and caching.
- **Generators**: Located in the `generators` directory, responsible for procedurally creating primitive shapes. Includes helpers for generating oriented quads (`_create_oriented_quad`), polygon disks (`_create_polygon_disk`), and merging geometry parts (`merge_geometry_parts`).
- **Math3D**: Provides `Vec3D` and `Mat3D` classes for vector and matrix operations, including standard transformations and arbitrary axis rotation (`rotation_around_axis`).
- **OpenGL Context & Input**: Separated OpenGL context setup (`context.py`) and input handling (`input.py`). `InputHandler` processes generic input events, decoupled from GLUT.
- **Renderer**: Basic OpenGL immediate mode renderer (`renderer.py`).

## Highlights

- Hierarchical scene graph using `Scene` and `Collection`.
- Interactive Camera Controls:
  - WASD movement (forward/back/strafe)
  - Mouse orbit (e.g., X + Left Drag) around target
  - Mouse pan (e.g., X + Right Drag) to look around
  - Mouse wheel dolly to zoom in/out
  - 'F' key to reset the camera view
- Dynamic Mesh Subdivision:
  - '+' / '-' keys adjust the subdivision level of the active mesh object
  - `Mesh` class handles subdivision levels and caching
  - Linear subdivision algorithm implemented
- Matrix Math: `Mat3D` class supports standard transformations and rotation around an arbitrary axis. Z-Up coordinate system used.
- Input Handling: Decoupled `InputHandler` class manages user input logic.

## Directory Structure

```
project_root/
│
├── camera/
│   └── camera.py
│
├── generators/
│   ├── basefactory2d.py
│   ├── factory2d.py
│   ├── factory3d.py
│   ├── grid.py
│   ├── line.py
│   └── utils.py
│
├── geometry/
│   ├── edge.py
│   ├── face.py
│   ├── mesh.py
│   └── vertex.py
│
├── math3d/
│   ├── mat3d.py
│   └── vec3d.py
│
├── object3d/
│   └── object3d.py
│
├── opengl/
│   ├── context.py
│   ├── input.py
│   ├── renderer.py
│   └── timer.py
│
├── scene/
│   ├── collection.py
│   └── scene.py
│
├── main.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Controls Summary

- **W/A/S/D**: Move camera Forward/Left/Backward/Right
- **Left Drag**: Orbit camera around its target
- **Right Drag**: Pan camera (look around)
- **Mouse Wheel**: Dolly camera (zoom in/out)
- **F**: Reset camera view
- **0**: Toggle grid visibility
- **1**: Add a new Box object (if none active)
- **2**: Remove the active Box object
- **+**: Increase active object's subdivision level
- **-**: Decrease active object's subdivision level
- **Q**: Quit application

## Notes / Current Status

- The core application structure (Scene, Object3D, Mesh, Math, Context, Input) is functional. Camera controls and the basic subdivision mechanism are working.
- **Primitive Generation**: Currently limited, with `create_box` implemented using the procedural helper functions. Significant effort was spent debugging procedural cylinder generation (`create_cylinder`) using the geometry merging function (`merge_geometry_parts`). This revealed subtle challenges in vertex merging/face reconstruction which remain unresolved and is postponed. Implementation of other primitives (Sphere, Plane, Torus, etc.) is planned for subsequent development stages.
- **Scene/Collection**: The Scene/Collection hierarchy provides a solid foundation for managing more complex scenes in the future, although current scene interaction is basic (add/remove one object).
- **Controls**: The implemented controls provide good interactivity. Modifier key detection (`Alt`, `Ctrl`, `Shift`) via `glutGetModifiers` proved unreliable in the development environment.
- **Generators Module**: The structure includes helpers like `_create_oriented_quad`, `_create_polygon_disk`, and `merge_geometry_parts`. The organization within the `generators` folder will be further refined as more primitives are added.
- **Subdivision**: The `Mesh` class supports subdivision levels and caching. Currently, only a linear subdivision algorithm (`_split_geometry`) is implemented. The `_smooth_vertices` method exists as a placeholder for future smoothing algorithms (e.g., Catmull-Clark).
- **Normals**: Calculating and storing normal vectors for faces has been deferred due to the complexity involved with generic polygons and subdivision.
- **GitHub Repository**: All assignments completed throughout this semester will be available in the `github.com/exiort/IntroToOpenGL` repository. In line with the incremental nature of the assignments, each week's submission will be stored in a dedicated branch named `week-n`. It is highly recommended to check these branches weekly to follow the progress and changes over time.

---

© Bugrahan Imal - April, 2025
