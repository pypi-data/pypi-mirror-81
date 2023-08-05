import datetime
import unittest
from builtins import RuntimeError
from unittest import mock
from unittest.mock import call

import freezegun
import mongomock
from bson import ObjectId
from pymongo import MongoClient

from pymongo_odm.document import Document
from pymongo_odm.helpers import Map
from pymongo_odm.helpers.type_hints import Datetime
from test.helpers import random_dict, random_str, random_datetime, random_int


class FakeDoc(Document):
    db = 'test'
    collection = 'fake_doc'

    def for_json(self) -> dict:
        pass


class TestDocument(unittest.TestCase):
    DOCUMENT_MODULE_PATH = 'pymongo_odm'
    DOCUMENT_PATH = f'{DOCUMENT_MODULE_PATH}.Document'
    _SET_PATH = f'{DOCUMENT_PATH}._set'
    _UPDATE_DB_CACHE_PATH = f'{DOCUMENT_PATH}._update_db_cache'
    _GET_DIFF_PATH = f'{DOCUMENT_PATH}._get_diff'
    _INSERT_PATH = f'{DOCUMENT_PATH}._insert'
    _UPDATE_PATH = f'{DOCUMENT_PATH}._update'
    _DEFAULT_PRE_INSERT_PATH = f'{DOCUMENT_PATH}._default_pre_insert'
    PRE_INSERT_PATH = f'{DOCUMENT_PATH}.pre_insert'
    POST_INSERT_PATH = f'{DOCUMENT_PATH}.post_insert'
    _DEFAULT_PRE_UPDATE_PATH = f'{DOCUMENT_PATH}._default_pre_update'
    PRE_UPDATE_PATH = f'{DOCUMENT_PATH}.pre_update'
    POST_UPDATE_PATH = f'{DOCUMENT_PATH}.post_update'

    def setUp(self):
        super().setUp()

        FakeDoc.client = mongomock.MongoClient()

    def test_cannot_instantiate_the_base_document(self):
        """
        Test Method:
        """
        # Given

        # I expect it to raise
        with self.assertRaises(NotImplementedError):
            # When I try to instantiate
            doc = Document()

    def test_get_db_should_return_the_db_object(self):
        """
        Test Method:
        """
        # Given I've got a doc model

        # When I call
        result = FakeDoc.get_db()

        # Then I expect
        self.assertIsInstance(result, mongomock.Database)
        self.assertEqual(FakeDoc.db, result.name)

    def test_get_collection_should_return_the_collection_object(self):
        """
        Test Method:
        """
        # Given I've got a doc model

        # When I call
        result = FakeDoc.get_collection()

        # Then I expect
        self.assertIsInstance(result, mongomock.Collection)
        self.assertEqual(FakeDoc.collection, result.name)

    def test_create_collection_should_skip_when_collection_exists(self):
        """
        Test Method:
        """
        # Given I know a collection exists
        FakeDoc().save()  # Saves in a collection

        # When I call
        FakeDoc.create_collection()

        # Then I expect
        self.assertEqual(1, FakeDoc.count())

    def test_create_collection_should_skip_when_collection_does_not_have_a_capped_attr(self):
        """
        Test Method:
        """
        # Given I know a we dont have a given collection
        FakeDoc.get_collection().drop()

        # When I call
        FakeDoc.create_collection()

        # Then I expect
        self.assertFalse(FakeDoc.collection in FakeDoc.get_db().list_collection_names())

    def test_create_collection_should_create_when_collection_has_a_capped_attr(self):
        """
        Test Method:
        """
        FakeDoc.client = MongoClient()

        # Given I know a we dont have a given collection
        FakeDoc.get_collection().drop()
        # And I know
        FakeDoc.capped = {
            'size': random_int(),
            'max': random_int()
        }

        # When I call
        FakeDoc.create_collection()

        # Then I expect
        self.assertTrue(FakeDoc.collection in FakeDoc.get_db().list_collection_names())
        self.assertTrue(FakeDoc.get_collection().options().get('capped', False))

        FakeDoc.capped = None
        FakeDoc.get_collection().drop()

    def test__update_db_cache_should_copy_data_to_data_in_db(self):
        """
        Test Method:
        """
        # Given I've got a doc model
        doc = FakeDoc()
        # And I know it has some data that is not stored in db (and not cached as stored in db)
        doc._data = Map({random_str(): random_str() for _ in range(5)})

        # When I call
        doc._update_db_cache()

        # Then I expect
        self.assertEqual(doc._data, doc._data_in_db)

    @mock.patch(_UPDATE_DB_CACHE_PATH)
    @mock.patch(_SET_PATH)
    def test__load_args_should_set_given_data_and_not_update_cache_when_doc_is_not_created(self, mock__set,
                                                                                           mock__update_db_cache):
        """
        Test Method:
        """
        # Given I've got a new doc model
        doc = FakeDoc()
        # And I've got a a raw doc
        raw_doc = {'_id': random_str(), 'created': random_datetime(), 'modified': random_datetime()}
        # And I don't won't to treat it as a document that exists in db yet
        is_created = False

        # When I call
        doc._load_args(raw_doc, is_created)

        # Then I expect
        calls = [call(key, raw_doc[key]) for key in raw_doc]
        mock__set.assert_has_calls(calls)
        mock__update_db_cache.assert_not_called()

    @mock.patch(_UPDATE_DB_CACHE_PATH)
    @mock.patch(_SET_PATH)
    def test__load_args_should_raise_when_is_created_is_true_but_not_given_an__id(self, mock__set,
                                                                                  mock__update_db_cache):
        """
        Test Method:
        """
        # Given I've got a new doc model
        doc = FakeDoc()
        # And I've got a a raw doc
        raw_doc = {'created': random_datetime(), 'modified': random_datetime()}
        # And I want to set the doc as created in db
        is_created = True

        # I expect it to raise
        with self.assertRaises(ValueError):
            # When I call
            doc._load_args(raw_doc, is_created)

        # Then I expect
        calls = [call(key, raw_doc[key]) for key in raw_doc]
        mock__set.assert_has_calls(calls)
        mock__update_db_cache.assert_not_called()

    @mock.patch(_UPDATE_DB_CACHE_PATH)
    @mock.patch(_SET_PATH)
    def test__load_args_should_set_given_data_and_update_cache_when_doc_is_created(self, mock__set,
                                                                                   mock__update_db_cache):
        """
        Test Method:
        """
        # Given I've got a new doc model
        doc = FakeDoc()
        # And I've got a a raw doc
        raw_doc = {'_id': random_str(), 'created': random_datetime(), 'modified': random_datetime()}
        # And I want to set the doc as created in db
        is_created = True

        # When I call
        doc._load_args(raw_doc, is_created)

        # Then I expect
        calls = [call(key, raw_doc[key]) for key in raw_doc]
        mock__set.assert_has_calls(calls)
        mock__update_db_cache.assert_called_once()

    def test__set_should_do_nothing_when_given_value_matches_the_existing_one(self):
        """
        Test Method:
        """
        # Given I've got a doc model
        doc = FakeDoc()
        # And I know the doc has some data
        key = random_str()
        value = random_str()
        doc._data[key] = value

        # When I call
        doc._set(key, value)

        # Then I expect
        self.assertEqual(value, doc._data[key])

    def test__set_should_update_value_when_is_different_than_exiting_value(self):
        """
        Test Method:
        """
        # Given I've got a doc model
        doc = FakeDoc()
        # And I know the doc has some data
        key = random_str()
        value = random_str()
        doc._data[key] = value
        new_value = random_str()

        # When I call
        doc._set(key, new_value)

        # Then I expect
        self.assertEqual(new_value, doc._data[key])

    def test__set_should_add_key_and_value_when_key_does_not_exist_yet(self):
        """
        Test Method:
        """
        # Given I've got a doc model
        doc = FakeDoc()
        # And I know the doc has no data
        doc._data.clear()
        # And I've got
        key = random_str()
        value = random_str()

        # When I call
        doc._set(key, value)

        # Then I expect
        self.assertEqual(value, doc._data[key])

    def test__get_diff_should_return_empty_dict_when_data_and_data_in_db_are_equal(self):
        """
        Test Method:
        """
        # Given I've got a doc model
        doc = FakeDoc()
        # And I know that the doc's data in memory is equal to the data in db
        data = random_dict(20)
        doc._data = data.copy()
        doc._data_in_db = data.copy()

        # When I call
        diff = doc._get_diff()

        # Then I expect
        self.assertEqual({}, diff)

    def test__get_diff_should_return_the_difference_between_data_and_data_in_db(self):
        """
        Test Method:
        """
        # Given I've got a doc model
        doc = FakeDoc()
        # And I know that the doc's data in memory is not equal to the data in db
        data = random_dict(20)
        data_in_db = random_dict(13)
        doc._data = data.copy()
        doc._data_in_db = data_in_db.copy()

        # When I call
        diff = doc._get_diff()

        # Then I expect
        self.assertEqual(data, diff)

    def test_saving_a_new_doc_should_add_created_and_modified_properties(self):
        """
        Test Method: INTEGRATION
        """
        # Given I've got a new doc instance
        doc = FakeDoc()

        # When I call
        doc.save()

        # Then I expect
        self.assertIsInstance(doc.created, Datetime)
        self.assertIsInstance(doc.modified, Datetime)
        self.assertIsInstance(doc.id, ObjectId)

    @mock.patch(_UPDATE_DB_CACHE_PATH)
    @mock.patch(_UPDATE_PATH)
    @mock.patch(_INSERT_PATH)
    def test_saving_a_new_doc_should_insert(self, mock__insert, mock__update, mock__update_db_cache):
        """
        Test Method:
        """
        # Given I've got a new doc instance
        doc = FakeDoc()

        # When I call
        result = doc.save()

        # Then I expect
        mock__insert.assert_called_once_with()
        mock__update.assert_not_called()
        mock__update_db_cache.assert_called_once()
        self.assertIs(doc, result)

    @mock.patch(_UPDATE_DB_CACHE_PATH)
    @mock.patch(_UPDATE_PATH)
    @mock.patch(_INSERT_PATH)
    def test_saving_an_existing_doc_should_raise_because_it_is_not_supported(self, mock__insert,
                                                                             mock__update, mock__update_db_cache):
        """
        Test Method:
        """
        # Given I've got an existing doc instance
        doc = FakeDoc()
        doc._data_in_db._id = random_str()

        # I expect it to raise
        with self.assertRaises(RuntimeError):
            # When I call
            result = doc.save()

        # Then I expect
        mock__insert.assert_not_called()
        mock__update_db_cache.assert_not_called()

    @freezegun.freeze_time('1999-11-11')
    @mock.patch(POST_INSERT_PATH)
    @mock.patch(_GET_DIFF_PATH)
    @mock.patch(PRE_INSERT_PATH)
    @mock.patch(_DEFAULT_PRE_INSERT_PATH)
    def test__insert_should_call_lifecycle_hooks_and_insert(self, mock__default_pre_insert, mock_pre_insert,
                                                            mock__get_diff, mock_post_insert):
        """
        Test Method:
        """
        # Given I've got a new Doc
        doc = FakeDoc()
        # And I know the new values (changes)
        date = datetime.datetime.utcnow()
        doc.created = date
        doc.modified = date
        changes = {'created': date, 'modified': date}
        mock__get_diff.return_value = changes

        # When I call
        doc._insert()

        # Then I expect
        mock__default_pre_insert.assert_called_once()
        mock_pre_insert.assert_called_once()
        mock__get_diff.assert_called_once()
        mock_post_insert.assert_called_once()
        _id = doc.id
        self.assertIsInstance(_id, ObjectId)
        expected = FakeDoc.get_collection().find_one({'_id': _id})
        self.assertIsNotNone(expected)
        self.assertEqual(expected.get('created'), doc.created)
        self.assertEqual(expected.get('created'), date)
        self.assertEqual(expected.get('modified'), doc.modified)
        self.assertEqual(expected.get('modified'), date)

    @freezegun.freeze_time('1999-11-11')
    def test__default_pre_insert_should_set_created_and_modified(self):
        """
        Test Method:
        """
        # Given I've got a new Doc
        doc = FakeDoc()

        # When I call
        doc._default_pre_insert()

        # Then I expect
        self.assertEqual(doc.created, datetime.datetime(1999, 11, 11))
        self.assertEqual(doc.modified, datetime.datetime(1999, 11, 11))

    def test__to_map_should_return_a_map_with_the_given_keys(self):
        """
        Test Method:
        """
        # Given I've got a doc model
        doc = FakeDoc()
        # And It has some data
        data = {'a': random_str(), 'b': random_str(), 'c': random_str()}
        doc._data = data

        # When I call
        result = doc._to_map('a', 'c', 'F')

        # Then I expect
        expected = Map({'_id': None, 'created': None, 'modified': None, 'a': data['a'], 'c': data['c'], 'F': None})
        self.assertEqual(expected, result)

    def test_from_dict_should_instantiate_document(self):
        """
        Test Method:
        """
        # Given I've got a raw doc
        raw_doc = {'_id': 4343, 'created': 4343244}

        # When I call
        result = FakeDoc.from_dict(raw_doc)

        # Then I expect
        self.assertIsInstance(result, FakeDoc)
        self.assertTrue(result.is_created)
        self.assertEqual(result._data, result._data_in_db)

    def test_from_dict_should_instantiate_document_without_setting_is_created(self):
        """
        Test Method:
        """
        # Given I've got a raw doc
        raw_doc = {'_id': 4343, 'created': 4343244}

        # When I call
        result = FakeDoc.from_dict(raw_doc, False)

        # Then I expect
        self.assertIsInstance(result, FakeDoc)
        self.assertFalse(result.is_created)
        self.assertNotEqual(result._data, result._data_in_db)

    def test_count_should_return_the_collection_count(self):
        """
        Test Method:
        """
        # Given I've got some docs in collection
        amount_of_docs = random_int(start=3)
        for _ in range(amount_of_docs):
            FakeDoc().save()

        # When I call
        result = FakeDoc.count()

        # Then I expect
        self.assertEqual(amount_of_docs, result)

    def test_document_should_not_equal_data_when_has_id_and_data_does_not_match(self):
        """
        Test Method:
        """
        # Given I've got 2 docs
        doc1 = FakeDoc().save()
        doc2 = FakeDoc().save()

        # When I call
        result = doc1 == doc2

        # Then I expect
        self.assertFalse(result)

    def test_document_should_equal_data_when_has_id(self):
        """
        Test Method:
        """
        # Given I've got 2 docs
        doc1 = FakeDoc().save()
        doc2 = FakeDoc()
        doc2._data = doc1._data

        # When I call
        result = doc1 == doc2

        # Then I expect
        self.assertTrue(result)

    def test_document_should_not_equal_itself_when_it_has_no_id(self):
        """
        Test Method:
        """
        # Given I've got 2 docs without id
        doc1 = FakeDoc()
        doc2 = FakeDoc()
        doc2._data = doc1._data

        # When I call
        result = doc1 == doc2

        # Then I expect
        self.assertFalse(result)

    def test_document_should_equal_itself_when_it_has_no_id(self):
        """
        Test Method:
        """
        # Given I've got a doc without an ID
        doc1 = FakeDoc()
        doc2 = doc1

        # When I call
        result = doc1 == doc2

        # Then I expect
        self.assertTrue(result)

    def test_delete_will_delete_the_doc_from_memory_when_doc_not_saved_yet(self):
        """
        Test Method:
        """
        # Given I've got a doc that is created (saved in db)
        doc = FakeDoc()
        doc._data = random_dict()

        # When I call
        result = doc.delete()

        # Then I expect
        self.assertFalse(hasattr(doc, '_data'))
        self.assertFalse(hasattr(doc, '_data_in_db'))
        self.assertTrue(result)

    def test_delete_will_delete_the_doc_from_db_and_from_memory(self):
        """
        Test Method:
        """
        # Given I've got a doc that is created (saved in db)
        doc = FakeDoc().save()
        _id = doc.id

        # When I call
        result = doc.delete()

        # Then I expect
        expected = FakeDoc.get_collection().find_one({'_id': _id})
        self.assertIsNone(expected)
        self.assertFalse(hasattr(doc, '_data'))
        self.assertFalse(hasattr(doc, '_data_in_db'))
        self.assertTrue(result)
