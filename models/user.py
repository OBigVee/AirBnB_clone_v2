#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, Column, String
import os


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    if os.environ.get("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = "users"
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)

        places = relationship("Place", cascade="all, delete",
                              backref="user")
        reviews = relationship("Review", cascade="all, delete",
                               backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

        places = []
