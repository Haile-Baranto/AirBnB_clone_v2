#!/usr/bin/python3
"""
DBStorage module for HBNB project.
Defines the DBStorage class that manages database storage for hbnb models.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from models.base_model import BaseModel, Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place, place_amenity
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """
    Class that manages storage of hbnb models in a SQL database.
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes the SQL database storage.
        """
        user = os.getenv('HBNB_MYSQL_USER')
        pword = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST', 'localhost')
        db_name = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')

        DATABASE_URL = f"mysql+mysqldb://{user}:{pword}@{host}/\
            {db_name}"

        self.__engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True
        )

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Returns a dictionary of models currently in storage.
        """
        objects = dict()
        all_classes = (User, State, City, Amenity, Place, Review)

        if cls is None:
            for class_type in all_classes:
                query = self.__session.query(class_type)
                for obj in query.all():
                    obj_key = f'{obj.__class__.__name__}.{obj.id}'
                    objects[obj_key] = obj
        else:
            query = self.__session.query(cls)
            for obj in query.all():
                obj_key = f'{obj.__class__.__name__}.{obj.id}'
                objects[obj_key] = obj

        return objects

    def delete(self, obj=None):
        """
        Removes an object from the storage database.
        """
        if obj is not None:
            self.__session.delete(obj)

    def new(self, obj):
        """
        Adds a new object to the storage database.
        """
        if obj is not None:
            self.__session.add(obj)

    def save(self):
        """
        Commits the session changes to the database.
        """
        self.__session.commit()

    def reload(self):
        """
        Loads the storage database.
        """
        Base.metadata.create_all(self.__engine)
        SessionFactory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        self.__session = scoped_session(SessionFactory)()

    def close(self):
        """
        Closes the storage engine.
        """
        self.__session.close()
