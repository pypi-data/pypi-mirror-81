# -*- coding: utf-8 -*-
"""
Created on 9/30/20

@author dor
"""


class DocumentMeta(type):
    def __call__(cls, *args, **kwargs):
        obj = type.__call__(cls, *args, **kwargs)

        cls._check_db(obj)
        cls._check_collection(obj)

        return obj

    def _check_db(cls, obj):
        if obj.db is None:
            raise NotImplementedError('Every document must define db = "db_name"')

    def _check_collection(cls, obj):
        if obj.collection is None:
            raise NotImplementedError('Every document must define collection = "collection_name"')
