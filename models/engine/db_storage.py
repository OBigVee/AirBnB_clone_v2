#!/usr/bin/python3
"""this module defines a DB storage class"""

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

        """I prefer to use the method described here in
        documentation to connect the database :
        https://docs.sqlalchemy.org/en/20/core/engines.html#:~:text=Creating%20URLs%20Programmatically%C2%B6
        """
        url_obj = URL.create(
            dialect + "+" + driver,
            username=getenv("HBNB_MYSQL_USER"),
            password=getenv("HBNB_MYSQL_PWD"),
            host=getenv("HBNB_MYSQL_HOST", default="localhost"),
            database=getenv("HBNB_MYSQL_DB"),
        )

        self.__engine = create_engine(url_obj, pool_pre_ping=True)

        """
        You can also connect the database with the connection credentials in
        the following way:

            credentials = [
                "HBNB_MYSQL_USER",
                "HBNB_MYSQL_PWD",
                "HBNB_MYSQL_HOST",
                "HBNB_MYSQL_DB"
            ]
            env_var = [os.environ.get(env) for env in credentials]
            engine = "mysql+mysqldb://{}:{}@{}/{}".format(*env_var[:])
            self.__engine = create_engine(engine, pool_pre_ping=True)
        """

        if getenv("HBNB_ENV") == "test":
            from models.base_model import Base

            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Queries the current database session (self.__session) all objects
        depending of the class name"""
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        objects = {}

        if cls:
            for obj in self.__session.query(cls).all():
                key = f"{cls}.__name__.{obj}.id"
                objects[key] = obj
        else:
            for model in [State, City, User, Place, Review, Amenity]:
                for obj in self.__session.query(model):
                    key = f"{model.__name__}.{obj.id}"
                    objects[key] = obj
        return objects

        # class_list = [State, City]#, User, Place, Review, Amenity]
        # objs = {}
        # if cls is not None:
        #     for obj in self.__session.query(cls).all():
        #         objs.update({obj.to_dict()['__class__'] + '.' + obj.id: obj})
        # else:
        #     for class_item in class_list:
        #         for obj in self.__session.query(class_item).all():
        #             key = obj.to_dict()['__class__'] + '.' + obj.id
        #             objs.update({key: obj})
        # return objs

    def new(self, obj):
        """add new object to the current database session"""

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

    def close(self):
        """call close method for committing obj to DB"""
        self.__session.close()
