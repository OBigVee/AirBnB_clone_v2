#!/usr/bin/python3
"""this module defines a DB storage class"""

# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from os import getenv


class DBStorage:
    """storage class"""

    __engine = None
    __session = None

    def __init__(self):
        """DBStorage constructor"""

        dialect = "mysql"
        driver = "mysqldb"

        # url_obj = URL.create(
        #     dialect + driver,
        #     username=getenv("HBNB_MYSQL_USER"),
        #     password=getenv("HBNB_MYSQL_PWD"),
        #     host=getenv("HBNB_MYSQL_HOST", default="localhost"),
        #     database=getenv("HBNB_MYSQL_DB"),
        # )
        cred = ["HBNB_MYSQL_USER","HBNB_MYSQL_PWD",
                "HBNB_MYSQL_HOST","HBNB_MYSQL_DB"]
        env_var = [os.environ.get(env) for env in cred ]
        engine = "mysql+mysqldb://{}:{}@{}/{}".format(*env_var)

        self.__engine = create_engine(engine, pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            from models.base_model import Base

            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Queries the current database session (self.__session) all objects
        depending of the class name"""

        objects = {}

        if cls:
            for obj in self.__session.query(cls):
                key = f"{cls}.__name__.{obj}.id"
                objects[key] = obj
        else:

            from models.user import User
            from models.state import State
            from models.city import City
            from models.amenity import Amenity
            from models.place import Place
            from models.review import Review

            for model in [User, State, City, Amenity, Place, Review]:
                for obj in self.__session.query(model):
                    key = f"{model}.__name__.{obj}.id"
                    objects[key] = obj
        return objects

    def new(self, obj):
        """add object to the current database session"""

        if obj:
            self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""

        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session `obj` if not `None`"""

        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database"""

        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review
        from models.base_model import Base

        Base.metadata.create_all(self.__engine)

        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        
        self.__session = scoped_session(Session)
