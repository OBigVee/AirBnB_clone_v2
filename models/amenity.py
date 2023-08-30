#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey
import os


class Amenity(BaseModel, Base):
    """Amenities Class"""
    if os.environ.get("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = "amenities"

        name = Column(String(128), nullable=False)
    else:
        name = ""
