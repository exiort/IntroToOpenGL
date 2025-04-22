# CENG 487 Assignment2 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from camera import Camera
from generators import create_grid_lines
from math3d import Vec3D
from object3d import Object3D
from .collection import Collection



class Scene:
    root_collection:Collection
    
    active_camera:Object3D
    active_object:Object3D|None
    
    default_camera_position:Vec3D
    default_camera_target:Vec3D
    default_camera_up:Vec3D
    
    def __init__(self) -> None:
        self.root_collection = Collection("RootCollection")

        self.default_camera_position = Vec3D(20, -25, 15)
        self.default_camera_target = Vec3D(0, 0, 0)
        self.default_camera_up = Vec3D(0, 0, 1)

        self.active_camera = Object3D("DefaultCam", Camera(self.default_camera_position, self.default_camera_target, self.default_camera_up))
        self.active_object = None
        
        grid_collection = Collection("WorldGrid")
        for obj in create_grid_lines(count=51):
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

