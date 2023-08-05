# -*- coding: utf-8 -*-
"""
Created on 9/30/20

@author dor
"""
from typing import List, Optional

from bson import ObjectId
from pymongo import MongoClient, IndexModel
from pymongo.collection import Collection
from pymongo.database import Database

from pymongo_odm.helpers import strict, Map, now
from pymongo_odm.helpers.type_hints import DocumentId, Datetime
from pymongo_odm.document_meta import DocumentMeta
from pymongo_odm.client import get_client


@strict
class Document(metaclass=DocumentMeta):
    client: MongoClient = get_client()

    db: str = None
    collection: str = None
    indexes: List[IndexModel] = None
    capped: dict = None

    def __init__(self, is_created: bool = False, **kwargs):
        self._data = Map()  # Data in memory
        self._data_in_db = Map()  # A cache of data stored in db

        self._load_args(kwargs, is_created)

    @classmethod
    def get_db(cls) -> Database:
        return cls.client[cls.db]

    @classmethod
    def get_collection(cls) -> Collection:
        return cls.get_db()[cls.collection]

    @classmethod
    def create_collection(cls):
        """Create collection manually if 'capped' is set"""
        if cls.collection in cls.get_db().list_collection_names():
            return

        # Check if has valid capped value
        if cls.capped:
            size = cls.capped.get('size')
            _max = cls.capped.get('max')

            if size is None:
                return

            doc = {'capped': True, 'size': size}

            if _max:
                doc['max'] = _max

            cls.get_db().create_collection(cls.collection, capped=True, size=size, max=_max)

    @classmethod
    def ensure_indexes(cls):
        """Make sure to call it after creating the
        class not the instances (dont need to call it more then once)
        """
        if cls.indexes:
            cls.get_collection().create_indexes(cls.indexes)

    @property
    def is_created(self) -> bool:
        """I know the doc is created when it has an _id.

        Returns:

        """
        return self._data_in_db.get('_id') is not None

    @property
    def id(self) -> Optional[DocumentId]:
        return self._data.get('_id')

    @property
    def created(self) -> Datetime:
        return self._data.get('created')

    @created.setter
    def created(self, value: Datetime):
        self._set('created', value)

    @property
    def modified(self) -> Datetime:
        return self._data.get('modified')

    @modified.setter
    def modified(self, value: Datetime):
        self._set('modified', value)

    @classmethod
    def from_dict(cls, data: dict, is_created: bool = True):
        doc = cls(is_created=is_created, **data)
        return doc

    @classmethod
    def count(cls, _filter: dict = None) -> int:
        """Count the document in the collection

        Args:
            _filter: Filter the documents that you want to count, default: {}

        Returns:
            int: Number of documents in collection.
        """
        return cls.get_collection().count_documents(_filter or {})

    @classmethod
    def find_one(cls, _filter: dict, raw: bool = False):
        """

        Args:
            _filter:
            raw: Return the raw doc (dict) retrieved from mongo

        Returns:

        """
        doc = cls.get_collection().find_one(_filter)

        if not doc:
            return

        if raw:
            return doc

        return cls.from_dict(doc)

    @classmethod
    def by_id(cls, _id: DocumentId, raw: bool = False):
        """

        Args:
            _id:
            raw: Return the raw doc (dict) retrieved from mongo

        Returns:

        """
        if not isinstance(_id, ObjectId):
            _id = ObjectId(_id)

        return cls.find_one({'_id': _id}, raw)

    def _update_db_cache(self):
        if self._data != self._data_in_db:
            self._data_in_db = self._data.copy()

    def _load_args(self, kwargs: dict, is_created: bool):
        """Load the default args that may be included when instantiating a doc

        Args:
            kwargs:
            is_created: When true will set the doc as a created doc (that the doc already exists in db)
        """
        default_keys = ('_id', 'created', 'modified')

        for key in default_keys:
            if key in kwargs:
                self._set(key, kwargs[key])

        if is_created:
            if not kwargs.get('_id'):
                raise ValueError('Document can not be set as created when it does not have an _id')

            self._update_db_cache()

    def _set(self, key: str, value):
        """Set a value to a key, and add key to the changed set if the value has changed.

        Args:
            key:
            value:
        """
        if value != self._data.get(key):
            self._data[key] = value

    def _get_diff(self) -> dict:
        """Get a dict with the difference between the data in memory and data in db.

        Notes:
            This will compare against a cache and not the actual data in db,
            for performance response. So when using the document model class make sure
            that the collection is not being updated from other resources.

        TODO: when adding update options, need to check for $unset as well as $set data

        Returns:

        """
        diff = {}

        if self._data == self._data_in_db:
            return diff

        for key, value in self._data.items():
            db_value = self._data_in_db.get(key, 'NONE')

            if value != db_value:
                diff[key] = value

        return diff

    def save(self):

        if not self.is_created:
            self._insert()
        else:
            raise RuntimeError('We do not support updates via the instance. '
                               'Use pymongo atomic update functions via self.get_collection().update_one() etc.')
            # self._update()

        self._update_db_cache()
        return self

    def _insert(self):

        self._default_pre_insert()
        self.pre_insert()

        changes = self._get_diff()

        _id = self.get_collection().insert_one(changes).inserted_id
        self._data._id = _id

        self.post_insert()

    def _update(self):
        """
        NOT IMPLEMENTED
        Returns:

        """
        raise Exception('NOT IMPLEMENTED')
        # self._default_pre_update()
        # self.pre_update()
        #
        # changes = self._get_diff()
        #
        # if not changes:
        #     return
        #
        # modified = self.collection.update_one({'_id': self.id}, {'$set': changes}).modified_count
        #
        # if modified == 0:
        #     raise RuntimeError()
        #
        # self.post_update()

    def delete(self):
        deleted = True
        if self.is_created:
            result = self.get_collection().delete_one({'_id': self.id})
            deleted = result.deleted_count == 1

        del self._data
        del self._data_in_db

        return deleted

    """
    HOOKS
    """

    def _default_pre_insert(self):
        self.created = now()
        self.modified = now()

    def _default_pre_update(self):
        """We don't have an updater implemented yet"""
        self.modified = now()

    def pre_insert(self):
        pass

    def post_insert(self):
        pass

    def pre_update(self):
        pass

    def post_update(self):
        pass

    def _to_map(self, *keys, exclude_default: bool = False) -> Map:
        """Get specific keys from doc and return it in a Map

        Args:
            *keys:

        Returns:

        """
        if not exclude_default:
            mapped = Map({
                '_id': self.id,
                'created': self.created,
                'modified': self.modified,
            })
        else:
            mapped = Map()

        for key in keys:
            mapped[key] = self._data.get(key)

        return mapped

    def for_json(self) -> dict:
        """The default behavior of a document when converting to json

        """
        return Map(self._data)

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self._data}>'

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if isinstance(other, self.__class__) and other.id is not None:
            return self._data == other._data
        if self.id is None:
            return self is other
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
