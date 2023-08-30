#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

# from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import URL, Column, DateTime, Integer, String, ForeignKey
import os

if os.environ.get("HBNB_TYPE_STORAGE") == "db":
    Base = sqlalchemy.orm.declarative_base()
else:
    Base = object
# Base = declarative_base()G


class BaseModel:
    """A base class for all hbnb models"""

    if os.environ.get("HBNB_TYPE_STORAGE") == "db":
        id = Column(String(60), primary_key=True, unique=True, nullable=False)
        created_at = Column(
            DateTime,
            default=datetime.utcnow(),
            nullable=False
        )
        updated_at = Column(
            DateTime,
            default=datetime.utcnow(),
            nullable=False
        )

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""

        if len(kwargs) != 0:
            kwargs.pop("__class__", None)
            for key, value in kwargs.items():
                if key in ["created_at", "updated_at"]:
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at

    def __str__(self):
        """Returns a string representation of the instance"""
        obj = self.__dict__.copy()
        try:
            del obj['_sa_instance_state']
        except KeyError:
            pass
        # cls = (str(type(self)).split(".")[-1]).split("'")[0]
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, obj)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage

        self.updated_at = datetime.now()
        storage.new(self)  # new line
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update(
            {
                "__class__": (str(type(self)).split(".")[-1]).split("'")[0]
                }
            )
        dictionary["created_at"] = self.created_at.isoformat()
        dictionary["updated_at"] = self.updated_at.isoformat()

        try:
            del dictionary["_sa_instance_state"]
        except KeyError:
            pass
        return dictionary

    def delete(self):
        """function deletes the current instance from the storage"""
        from models import storage

        storage.delete(self)
