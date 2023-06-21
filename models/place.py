#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Table, Column, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


place_amenity = Table('place_amenity', Base.metadata,
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True,
                             nullable=False),
                      Column('place_id', String(60),
                             ForeignKey('places.id'),
                             primary_key=True,
                             nullable=False)
                      )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship("Review", backref="place",
                               cascade="all, delete")
        amenities = relationship('Amenity',
                                 secondary="place_amenity",
                                 viewonly=False, backref="places")

    else:
        @property
        def reviews(self):
            """Getter attribute cities that returns the list of Review"""
            from models import storage
            from models.review import Review
            my_list = []
            all_reviews = storage.all(Review)
            for review in all_reviews.values():
                if review.place_id == self.id:
                    my_list.append(review)
            return my_list

        @property
        def amenities(self):
            """Getter attribute cities that returns the list of Amenity"""
            from models import storage
            from models.amenity import Amenity
            my_list = []
            all_amenities = storage.all(Amenity)
            for amenities in all_amenities.values():
                if amenities.amenity_ids == self.id:
                    my_list.append(amenities)
            return my_list

        @amenities.setter
        def amenities(self, obj=None):
            """Setter atrributes for amenities"""
            from models.amenity import Amenity
            if type(obj) is Amenity:
                self.amenity_ids.append(obj.id)
            # else:
            #    return
