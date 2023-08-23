#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String,ForeignKey
from sqlalchemy.orm import relationship
import os

class City(BaseModel):
    """ The city class, contains state ID and name """
    if os.environ.get("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = "cities"
        name = Column(String(128), nullable=False)
        state_id = Column(String(60),ForeignKey("states.id") ,nullable=False,)

        places = relationship("Place", cascade="all, delete",
                            backref='cities')
    else:
        name = ""
        state_id = ""