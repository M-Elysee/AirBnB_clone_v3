#!/usr/bin/python3
""" Contains the TestAmenityDocs classes """

from datetime import datetime
import inspect
import models
from models import amenity
from models.base_model import BaseModel
import pep8
import unittest
Amenity = amenity.Amenity


class TestAmenityDocs(unittest.TestCase):
    """Tests to check the documentation and style of Amenity class"""
    @classmethod
    def setUpClass(cls):
        """ Testing Set up for the doc tests """
        cls.amenity_f = inspect.getmembers(Amenity, inspect.isfunction)

    def test_pep8_conform_amenity(self):
        """ Testing that models/amenity.py conforms to PEP8. """
        pep8s = pep8.StyleGuide(quiet=True)
        res = pep8s.check_files(['models/amenity.py'])
        self.assertEqual(res.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conform_test_amenity(self):
        """Testing that tests/test_models/test_amenity.py conforms to PEP8"""
        pep8s = pep8.StyleGuide(quiet=True)
        res = pep8s.check_files(['tests/test_models/test_amenity.py'])
        self.assertEqual(res.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_amenity_module_docstring(self):
        """ Testing for the amenity.py module docstring """
        self.assertIsNot(amenity.__doc__, None,
                         "amenity.py needs a docstring")
        self.assertTrue(len(amenity.__doc__) >= 1,
                        "amenity.py needs a docstring")

    def test_amenity_class_docstring(self):
        """ Testing for the Amenity class docstring """
        self.assertIsNot(Amenity.__doc__, None,
                         "Amenity class needs a docstring")
        self.assertTrue(len(Amenity.__doc__) >= 1,
                        "Amenity class needs a docstring")

    def test_amenity_func_docstrings(self):
        """ Testing for presence of docstrings in Amenity methods """
        for func in self.amenity_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestAmenity(unittest.TestCase):
    """ Testing the Amenity class """
    def test_is_subclass(self):
        """ Testing that Amenity is a subclass of BaseModel """
        amnty = Amenity()
        self.assertIsInstance(am, BaseModel)
        self.assertTrue(hasattr(amnty, "id"))
        self.assertTrue(hasattr(amnty, "created_at"))
        self.assertTrue(hasattr(amnty, "updated_at"))

    def test_name_attr(self):
        """Testing that Amenity has attribute name, and is an empty string"""
        amnty = Amenity()
        self.assertTrue(hasattr(amnty, "name"))
        if models.storage_t == 'db':
            self.assertEqual(amnty.name, None)
        else:
            self.assertEqual(amnty.name, "")

    def test_to_dict_creates_dict(self):
        """ Testing to_dict method creates a dictionary with proper attrs """
        amnty = Amenity()
        print(amnty.__dict__)
        new_dct = amnty.to_dict()
        self.assertEqual(type(new_dct), dict)
        self.assertFalse("_sa_instance_state" in new_dct)
        for attr in amnty.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_dct)
        self.assertTrue("__class__" in new_dct)

    def test_to_dict_values(self):
        """ Testing that values in dict returned from to_dict are correct """
        t_formt = "%Y-%m-%dT%H:%M:%S.%f"
        am = Amenity()
        n_dct = amn.to_dict()
        self.assertEqual(n_dct["__class__"], "Amenity")
        self.assertEqual(type(n_dct["created_at"]), str)
        self.assertEqual(type(n_dct["updated_at"]), str)
        self.assertEqual(n_dct["created_at"], am.created_at.strftime(t_formt))
        self.assertEqual(n_dct["updated_at"], am.updated_at.strftime(t_formt))

    def test_str(self):
        """ Testing that the str method has correct output """
        amnty = Amenity()
        string = "[Amenity] ({}) {}".format(amenity.id, amnty.__dict__)
        self.assertEqual(string, str(amnty))
