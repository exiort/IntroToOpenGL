# CENG 487 Assignment2 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from geometry import Material
from camera import Camera
from generators import create_grid_lines
from math3d import Vec3D, Vec4D
from object3d import Object3D
from shaders import Shader
from .collection import Collection



class Scene:
    root_collection:Collection
    
    active_camera:Object3D
    active_object:Object3D|None
    
    default_camera_position:Vec3D
    default_camera_target:Vec3D
    default_camera_up:Vec3D

    default_material:Material
    
    shader:Shader
    
    def __init__(self, shader:Shader) -> None:
        self.shader = shader
        
        self.root_collection = Collection("RootCollection")
        self.object_default_material = Material()
        
        self.default_camera_position = Vec3D(0, 40, 15)
        self.default_camera_target = Vec3D(0, 0, 0)
        self.default_camera_up = Vec3D(0, 0, 1, 0)
        self.active_camera = Object3D(shader, "DefaultCam", Camera("Camera", self.default_camera_position, self.default_camera_target, self.default_camera_up))
        self.active_object = None
        
        grid_collection = Collection("WorldGrid")
        for obj in create_grid_lines(shader, count=71):
            material = Material()
            material.use_raw_color = True
            material.raw_color = Vec4D(0.75, 0.75, 0.75, 1)
            obj.material = material
            grid_collection.add_object(obj, is_visible=True)
        self.root_collection.add_child(grid_collection)
            
    def set_active_camera(self, camera_object:Object3D) -> None:
        self.active_camera = camera_object

    def get_active_camera(self) -> Object3D:
        return self.active_camera

    def set_active_object(self, active_object:Object3D|None) -> None:
        self.active_object = active_object

    def get_active_object(self) -> Object3D|None:
        return self.active_object
    
    def get_visible_objects(self) -> list[Object3D]:
        return self.root_collection.get_all_visible_object()

    def add_object(self, obj:Object3D, is_visible:bool=True) -> None:
        if obj.material:
            obj.material = self.object_default_material.copy()
            
        self.root_collection.add_object(obj, is_visible)

    def remove_object(self, obj:Object3D) -> None:
        self.root_collection.remove_object(obj)

    def add_collection(self, collection:Collection) -> None:
        self.root_collection.add_child(collection)

    def remove_collection(self, collection:Collection) -> None:
        self.root_collection.remove_child(collection)

    def change_grid_visibility(self) -> None:
        for collection in self.root_collection.children:
            if collection.name == "WorldGrid":
                collection.set_collection_visibility(not collection.is_visible)

    def get_latest_object(self) -> Object3D|None:
        objects = self.root_collection.objects
        if len(objects) == 0:
            return None
        return next(iter(objects))
        
    def get_next_object(self, obj:Object3D) -> Object3D|None:
        objs = list(self.root_collection.objects)
        size = len(objs)
        if size == 0:
            return None
        crr_idx = objs.index(obj)
        return objs[(crr_idx + 1) % size]

    def get_object_count(self) -> int:
        return len(self.root_collection.objects)
    
