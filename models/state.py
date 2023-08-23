#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String 

class State(BaseModel):
    """ State class """
    __tablename__ = "states"
    name = Column(String(138), nullable=False)
    