#!/usr/bin/python3
"""
Contains TestStateDocs classes
"""

from datetime import datetime
import inspect
import models
from models import state
from models.base_model import BaseModel
import pep8
import unittest
State = state.State


class TestStateDocs(unittest.TestCase):
    """Tests to check documentation and style of State class"""
    @classmethod
    def setUpClass(cls):
        """Set up for doc tests"""
        cls.state_f = inspect.getmembers(State, inspect.isfunction)

    def test_pep8_conformance_state(self):
        """Testing that models/state.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        res = pep8s.check_files(['models/state.py'])
        self.assertEqual(res.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_state(self):
        """Testing that tests/test_models/test_state.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        res = pep8s.check_files(['tests/test_models/test_state.py'])
        self.assertEqual(res.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_state_module_docstring(self):
        """Testing for state.py module docstring"""
        self.assertIsNot(state.__doc__, None,
                         "state.py needs a docstring")
        self.assertTrue(len(state.__doc__) >= 1,
                        "state.py needs a docstring")

    def test_state_class_docstring(self):
        """Testing for State class docstring"""
        self.assertIsNot(State.__doc__, None,
                         "State class needs a docstring")
        self.assertTrue(len(State.__doc__) >= 1,
                        "State class needs a docstring")

    def test_state_func_docstrings(self):
        """Testing for presence of docstrings in State methods"""
        for func in self.state_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestState(unittest.TestCase):
    """Testing State class"""
    def test_is_subclass(self):
        """Testing that State is a subclass of BaseModel"""
        sta = State()
        self.assertIsInstance(sta, BaseModel)
        self.assertTrue(hasattr(sta, "id"))
        self.assertTrue(hasattr(sta, "created_at"))
        self.assertTrue(hasattr(sta, "updated_at"))

    def test_to_dict_creates_dict(self):
        """Testing to_dict method creates a dictionary with proper attrs"""
        sta = State()
        new_d = s.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in sta.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_name_attr(self):
        """Testing that State has attribute name, and is as an empty string"""
        sta = State()
        self.assertTrue(hasattr(sta, "name"))
        if models.storage_t == 'db':
            self.assertEqual(sta.name, None)
        else:
            self.assertEqual(sta.name, "")

    def test_to_dict_values(self):
        """Testing that values in dict returned from to_dict are correct"""
        t_formt = "%Y-%m-%dT%H:%M:%S.%f"
        sta = State()
        new_d = sta.to_dict()
        self.assertEqual(new_d["__class__"], "State")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], sta.created_at.strftime(t_formt))
        self.assertEqual(new_d["updated_at"], sta.updated_at.strftime(t_formt))

    def test_str(self):
        """Testing that str method has correct output"""
        sta = State()
        string = "[State] ({}) {}".format(sta.id, sta.__dict__)
        self.assertEqual(string, str(sta))
