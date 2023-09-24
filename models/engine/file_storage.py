#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
import os
from importlib import import_module


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}
    def __init__(self):
        """Initialize instance of FileStorage class"""
        self.model_classes = {
            'Amenity': import_module('models.amenity').Amenity,
            'BaseModel': import_module('models.base_model').BaseModel,
            'City': import_module('models.city').City,
            'Place': import_module('models.place').Place,
            'Review': import_module('models.review').Review,
            'State': import_module('models.state').State,
            'User': import_module('models.user').User
        }

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            return self.__objects
        else:
            select_dict = {}
            for key, value in self.__objects.items():
                if type(value) is cls:
                    select_dict[key] = value
            return select_dict

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dict from file"""
        classes = self.model_classes
        if os.path.isfile(self.__file_path):
            temp = {}
            with open(self.__file_path, 'r') as file:
                temp = json.load(file)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)

    def close(self):
        """Closes the storage file."""
        self.reload()

    def delete(self, obj=None):
        """Removes an object from the storage dictionary if it exists"""
        if obj is not None:
            object_key = obj.to_dict()['__class__'] + '.' + obj.id
            if object_key in self.__objects.keys():
                del self.__objects[object_key]
