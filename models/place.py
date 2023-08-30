#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base

from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Float, ForeignKey
import os


class Place(BaseModel, Base):
    """A place to stay"""

    if os.environ.get("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = "places"

        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        amenity_ids = []
        reviews = relationship("Review", cascade="all, delete",
                               backref="place")
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """Getter attributes for reviews"""
            from models import storage
            from models.review import Review

            reviews = storage.all(Review)
            result = []

            for review in reviews.values():
                if review.place_id == self.id:
                    result.append(review)
            return result
