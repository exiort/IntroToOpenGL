# Object3D Transformations and Geometry Project

## Overview

This project implements a 3D object system with support for transformations and hierarchical geometry. The main components include:

- **Object3D**: Core structure representing a 3D object, containing a mesh and transformation stacks.
- **Mesh / Geometry**: Meshes are composed of vertices, edges, and faces.
- **Transformations**: Modular system using 3x3 matrices for 2D/3D transformations including translation, rotation (with pivot support), and scaling.
- **Factories**: Organized under the `generators` directory to create geometric shapes like triangles and squares.
- **Viewer**: OpenGL-based viewer implemented with a draw loop and frame timer.
- **Utilities**: Time-based update mechanism to support smooth animation logic (with bonus points in mind).

## Highlights

- Stack-based transformation system with undo/redo.
- Explicit transformation baking (`bake`) and applying (`apply_transform`).
- Modular transformation functions using matrix math.
- Cleanly separated `basefactory2d.py` and `factory2d.py` structure.
- Pivot-based rotation implementation via composition: `rotate_around_vec`.

## Directory Structure

```
project_root/
│
├── object3d/
│   └── object3d.py
├── geometry/
│   └── vertex.py, edge.py, face.py, mesh.py
├── math3d/
│   └── vec3d.py, mat3d.py
├── transform/
│   └── rotate.py, pivot.py, ...
├── generators/
│   ├── basefactory2d.py
│   └── factory2d.py
├── viewer/
│   ├── window.py
│   └── draw.py
├── utils/
│   └── timer.py
└── main.py
```

## Notes

- assignment.py has been moved into the viewer/ folder. This structure is more compatible with the overall modularity of the project.
- Some modules currently do not have an active function (e.g., Face, Edge). However, they have been included during the design phase as they may be useful in the future and are expected to simplify the process of adding new features.
- viewer/ is a temporary folder. Although its current structure is more modular, it is still too large and unorganized. The viewer folder will be removed once Scene and Render modules are added.
- Color support for Object3D has been postponed, as creating a Texture class may provide more flexibility and benefit in the long term.
- Calculating and storing normal vectors for faces has been deferred. Developing general methods for all polygons and non-planar surfaces introduces significant complexity at this stage.
- Rotation operations around a pivot currently involve to_origin and to_pivot matrices for each transformation. While optimizing this for better performance has been considered, it has been postponed for now as it is not a priority at this stage.
---

© Bugrahan Imal - April, 2025
