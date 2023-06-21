#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from os import getenv
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """Class Storage"""
    __engine = None
    __session = None

    def __init__(self):
        """Instance a DBStorage object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(HBNB_MYSQL_USER,
                                              HBNB_MYSQL_PWD,
                                              HBNB_MYSQL_HOST,
                                              HBNB_MYSQL_DB),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session"""
        if cls is None:
            objs_query = self.__session.query(State).all()
            objs_query.extend(self.__session.query(City).all())
            objs_query.extend(self.__session.query(User).all())
            objs_query.extend(self.__session.query(Place).all())
            objs_query.extend(self.__session.query(Review).all())
            objs_query.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            objs_query = self.__session.query(cls)
        return {"{}.{}".format(type(objt).__name__, objt.id):
                objt for objt in objs_query}

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = Session()

    def close(self):
        """call remove() method on the private session attribute """
        self.__session.close()
