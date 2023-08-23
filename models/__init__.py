#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
import os


if os.getenv("HBNB_TYPE_STORAGE") == "db":
    """a conditional depending of the value of the environment variable"""
    from models.engine.db_storage import DBStorage

    storage = DBStorage()

else:
    from models.engine.file_storage import FileStorage

    storage = FileStorage()

storage.reload()
