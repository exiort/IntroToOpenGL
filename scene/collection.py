# CENG 487 Assignment2 by
# Bugrahan Imal
# StudentId: 280201012
# April 2025

from __future__ import annotations
from object3d import Object3D



class Collection:
    name:str
    is_visible:bool
    objects:dict[Object3D, bool] #Object:is_visible
    children:list[Collection]
    
    def __init__(self, name:str="Collection", objects:dict[Object3D, bool]|None=None, children:list[Collection]|None=None) -> None:
        self.name = name
        self.is_visible = True
        if objects is None:
            self.objects = {}
        else:
            self.objects = objects

        if children is None:
            self.children = []
        else:
            self.children = children

    def set_collection_visibility(self, status:bool) -> None:
        self.is_visible = status
        
    def add_object(self, obj:Object3D, is_visible:bool) -> None:
        self.objects[obj] = is_visible

    def remove_object(self, obj:Object3D) -> None:
        if obj in self.objects:
            del self.objects[obj]

    def set_object_visibility(self, obj:Object3D, status:bool) -> None:
        if obj in self.objects:
            self.objects[obj] = status

    def add_child(self, collection:Collection) -> None:
        self.children.append(collection)

    def remove_child(self, child:Collection) -> None:
        if child in self.children:
            self.children.remove(child)

    def set_child_visibility(self, child:Collection, status:bool) -> None:
        if child in self.children:
            child.set_collection_visibility(status)

    def get_all_visible_object(self) -> list[Object3D]:
        objects = []

        if self.is_visible:
            for obj, is_visible in self.objects.items():
                if is_visible:
                    objects.append(obj)

            for child in self.children:
                objects.extend(child.get_all_visible_object())

        return objects

