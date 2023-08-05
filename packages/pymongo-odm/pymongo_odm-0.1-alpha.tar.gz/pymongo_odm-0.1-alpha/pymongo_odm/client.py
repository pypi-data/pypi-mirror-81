# -*- coding: utf-8 -*-
"""
Created on 9/30/20

@author dor
"""
from typing import Optional

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

CLIENT: Optional[MongoClient] = None


def connect(host: str = 'localhost', port: int = 27017):
    """
    Supports only one client
    """
    global CLIENT

    if isinstance(CLIENT, MongoClient):
        try:
            CLIENT.server_info()
            return
        except ServerSelectionTimeoutError as e:
            pass

    else:
        CLIENT = MongoClient(
            host,
            port,
            # username=username,
            # password=password,
            connect=False,
        )


def get_client() -> MongoClient:
    return CLIENT
