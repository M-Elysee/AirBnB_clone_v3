#!/usr/bin/python3
"""Testing BaseModel for expected behavior and documentation"""
from datetime import datetime
import inspect
import models
import pep8 as pycodestyle
import time
import unittest
from unitTesting import mock
BaseModel = models.base_model.BaseModel
module_doc = models.base_model.__doc__


class TestBaseModelDocs(unittest.TestCase):
    """Tests to check documentation and style of BaseModel class"""

    @classmethod
    def setUpClass(self):
        """Set up for docstring tests"""
        self.base_funcs = inspect.getmembers(BaseModel, inspect.isfunction)

    def test_pep8_conform(self):
        """Testing that models/base_model.py conforms to PEP8."""
        for pth in ['models/base_model.py',
                    'tests/test_models/test_base_model.py']:
            with self.subTest(path=pth):
                errs = pycodestyle.Checker(pth).check_all()
                self.assertEqual(errs, 0)

    def test_module_docstring(self):
        """Testing for existence of module docstring"""
        self.assertIsNot(module_doc, None,
                         "base_model.py needs a docstring")
        self.assertTrue(len(module_doc) > 1,
                        "base_model.py needs a docstring")

    def test_class_docstring(self):
        """Testing for BaseModel class docstring"""
        self.assertIsNot(BaseModel.__doc__, None,
                         "BaseModel class needs a docstring")
        self.assertTrue(len(BaseModel.__doc__) >= 1,
                        "BaseModel class needs a docstring")

    def test_func_docstrings(self):
        """Testing for presence of docstrings in BaseModel methods"""
        for func in self.base_funcs:
            with self.subTest(function=func):
                self.assertIsNot(
                    func[1].__doc__,
                    None,
                    "{:s} method needs a docstring".format(func[0])
                )
                self.assertTrue(
                    len(func[1].__doc__) > 1,
                    "{:s} method needs a docstring".format(func[0])
                )


class TestBaseModel(unittest.TestCase):
    """Testing BaseModel class"""
    def test_instantiation(self):
        """Testing that object is correctly created"""
        instnc = BaseModel()
        self.assertIs(type(instnc), BaseModel)
        instnc.name = "Holberton"
        instnc.number = 89
        att_types = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "name": str,
            "number": int
        }
        for attr, typ in att_types.items():
            with self.subTest(attr=attr, typ=typ):
                self.assertIn(attr, instnc.__dict__)
                self.assertIs(type(instnc.__dict__[attr]), typ)
        self.assertEqual(instnc.name, "Holberton")
        self.assertEqual(instnc.number, 89)

    def test_datetime_attributes(self):
        """
        Testing that two BaseModel instances have different datetime objects
        & that upon creation have identical updated_at and created_at
        value.
        """
        tic = datetime.now()
        instnc1 = BaseModel()
        toc = datetime.now()
        self.assertTrue(tic <= instnc1.created_at <= toc)
        time.sleep(1e-4)
        tic = datetime.now()
        instnc2 = BaseModel()
        toc = datetime.now()
        self.assertTrue(tic <= instnc2.created_at <= toc)
        self.assertEqual(instnc1.created_at, instnc1.updated_at)
        self.assertEqual(instnc2.created_at, instnc2.updated_at)
        self.assertNotEqual(instnc1.created_at, instnc2.created_at)
        self.assertNotEqual(instnc1.updated_at, instnc2.updated_at)

    def test_uuid(self):
        """Testing that id is a valid uuid"""
        instnc1 = BaseModel()
        instnc2 = BaseModel()
        for instnc in [instnc1, instnc2]:
            uuid = instnc.id
            with self.subTest(uuid=uuid):
                self.assertIs(type(uuid), str)
                self.assertRegex(uuid,
                                 '^[0-9a-f]{8}-[0-9a-f]{4}'
                                 '-[0-9a-f]{4}-[0-9a-f]{4}'
                                 '-[0-9a-f]{12}$')
        self.assertNotEqual(instnc1.id, instnc2.id)

    def test_to_dict(self):
        """Testing conversion of object attributes to dictionary for json"""
        my_model = BaseModel()
        my_model.name = "Holberton"
        my_model.my_number = 89
        d = my_model.to_dict()
        expected_attrs = ["id",
                          "created_at",
                          "updated_at",
                          "name",
                          "my_number",
                          "__class__"]
        self.assertCountEqual(d.keys(), expected_attrs)
        self.assertEqual(d['__class__'], 'BaseModel')
        self.assertEqual(d['name'], "Holberton")
        self.assertEqual(d['my_number'], 89)

    def test_to_dict_values(self):
        """Testing that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        bm = BaseModel()
        new_d = bm.to_dict()
        self.assertEqual(new_d["__class__"], "BaseModel")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], bm.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], bm.updated_at.strftime(t_format))

    def test_str(self):
        """Testing that str method has correct output"""
        instnc = BaseModel()
        string = "[BaseModel] ({}) {}".format(instnc.id, instnc.__dict__)
        self.assertEqual(string, str(instnc))

    @mock.patch('models.storage')
    def test_save(self, mock_storage):
        """
        Testing that save method updates `updated_at` and calls
        `storage.save`
        """
        instnc = BaseModel()
        old_created_at = instnc.created_at
        old_updated_at = instnc.updated_at
        instnc.save()
        new_created_at = instnc.created_at
        new_updated_at = instnc.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertEqual(old_created_at, new_created_at)
        self.assertTrue(mock_storage.new.called)
        self.assertTrue(mock_storage.save.called)
