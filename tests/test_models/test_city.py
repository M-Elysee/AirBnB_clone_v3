#!/usr/bin/python3
"""
Contains TestCityDocs classes
"""
from datetime import datetime
import inspect
import models
from models import city
from models.base_model import BaseModel
import pep8
import unittest

City = city.City


class TestCityDocs(unittest.TestCase):
    """Tests to check documentation and style of City class"""
    @classmethod
    def setUpClass(cls):
        """Set up for doc tests"""
        cls.city_f = inspect.getmembers(City, inspect.isfunction)

    def test_pep8_conformance_city(self):
        """Testing that models/city.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        res = pep8s.check_files(['models/city.py'])
        self.assertEqual(res.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_city(self):
        """Testing that tests/test_models/test_city.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        res = pep8s.check_files(['tests/test_models/test_city.py'])
        self.assertEqual(res.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_city_module_docstring(self):
        """Testing for city.py module docstring"""
        self.assertIsNot(city.__doc__, None,
                         "city.py needs a docstring")
        self.assertTrue(len(city.__doc__) >= 1,
                        "city.py needs a docstring")

    def test_city_class_docstring(self):
        """Testing for City class docstring"""
        self.assertIsNot(City.__doc__, None,
                         "City class needs a docstring")
        self.assertTrue(len(City.__doc__) >= 1,
                        "City class needs a docstring")

    def test_city_func_docstrings(self):
        """Testing for presence of docstrings in City methods"""
        for func in self.city_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestCity(unittest.TestCase):
    """Testing City class"""
    def test_is_subclass(self):
        """Testing that City is a subclass of BaseModel"""
        cty = City()
        self.assertIsInstance(cty, BaseModel)
        self.assertTrue(hasattr(cty, "id"))
        self.assertTrue(hasattr(cty, "created_at"))
        self.assertTrue(hasattr(cty, "updated_at"))

    def test_state_id_attr(self):
        """Testing that City has attribute state_id, and is an empty string"""
        cty = City()
        self.assertTrue(hasattr(cty, "state_id"))
        if models.storage_t == 'db':
            self.assertEqual(cty.state_id, None)
        else:
            self.assertEqual(cty.state_id, "")

    def test_name_attr(self):
        """Testing that City has attribute name, and is an empty string"""
        cty = City()
        self.assertTrue(hasattr(cty, "name"))
        if models.storage_t == 'db':
            self.assertEqual(cty.name, None)
        else:
            self.assertEqual(cty.name, "")

    def test_to_dict_values(self):
        """Testing that values in dict returned from to_dict are correct"""
        t_formt = "%Y-%m-%dT%H:%M:%S.%f"
        cty = City()
        new_d = cty.to_dict()
        self.assertEqual(new_d["__class__"], "City")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], cty.created_at.strftime(t_formt))
        self.assertEqual(new_d["updated_at"], cty.updated_at.strftime(t_formt))

    def test_to_dict_creates_dict(self):
        """Testing to_dict method creates a dictionary with proper attrs"""
        cty = City()
        new_d = cty.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in cty.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_str(self):
        """Testing that str method has correct output"""
        cty = City()
        string = "[City] ({}) {}".format(cty.id, cty.__dict__)
        self.assertEqual(string, str(cty))
