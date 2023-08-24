#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from models.city import City

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

import os


class State(BaseModel):
    """ State class """
    __tablename__ = "states"
    name = Column(
        String(138), nullable=False
        ) if os.getenv("HBNB_TYPE_STORAGE") == "db" else ""
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship(
            "City",
            cascade="all, delete, delete-orphan",
            backref="state"
        )
    else:
        @property
        def cities(self):
            """Return the cities in the state"""
            from models import storage
            cities_in_state = []
            for v in storage.all(City).values():
                if v.state_id == self.id:
                    cities_in_state.append(v)
            return cities_in_state