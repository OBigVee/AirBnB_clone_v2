#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base

# from models.state import State
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import os


class City(BaseModel, Base):
    """The city class, contains state ID and name"""

    if os.environ.get("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = "cities"
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
        places = relationship("Place", cascade="all, delete", backref='cities')
    else:
        name = ""
        state_id = ""
