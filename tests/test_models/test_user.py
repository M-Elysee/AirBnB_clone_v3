#!/usr/bin/python3
"""
Contains TestUserDocs classes
"""

from datetime import datetime
import inspect
import models
from models import user
from models.base_model import BaseModel
import pep8
import unittest
User = user.User


class TestUserDocs(unittest.TestCase):
    """Tests to check documentation and style of User class"""
    @classmethod
    def setUpClass(cls):
        """Set up for doc tests"""
        cls.user_f = inspect.getmembers(User, inspect.isfunction)

    def test_pep8_conformance_user(self):
        """Testing that models/user.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        res = pep8s.check_files(['models/user.py'])
        self.assertEqual(res.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_user(self):
        """Testing that tests/test_models/test_user.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        res = pep8s.check_files(['tests/test_models/test_user.py'])
        self.assertEqual(res.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_user_module_docstring(self):
        """Testing for user.py module docstring"""
        self.assertIsNot(user.__doc__, None,
                         "user.py needs a docstring")
        self.assertTrue(len(user.__doc__) >= 1,
                        "user.py needs a docstring")

    def test_user_class_docstring(self):
        """Testing for City class docstring"""
        self.assertIsNot(User.__doc__, None,
                         "User class needs a docstring")
        self.assertTrue(len(User.__doc__) >= 1,
                        "User class needs a docstring")

    def test_user_func_docstrings(self):
        """Testing for presence of docstrings in User methods"""
        for func in self.user_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestUser(unittest.TestCase):
    """Testing User class"""
    def test_is_subclass(self):
        """Testing that User is a subclass of BaseModel"""
        usr = User()
        self.assertIsInstance(usr, BaseModel)
        self.assertTrue(hasattr(usr, "id"))
        self.assertTrue(hasattr(usr, "created_at"))
        self.assertTrue(hasattr(usr, "updated_at"))

    def test_email_attr(self):
        """Testing that User has attr email, and is an empty string"""
        usr = User()
        self.assertTrue(hasattr(usr, "email"))
        if models.storage_t == 'db':
            self.assertEqual(usr.email, None)
        else:
            self.assertEqual(usr.email, "")

    def test_password_attr(self):
        """Testing that User has attr password, and is an empty string"""
        usr = User()
        self.assertTrue(hasattr(usr, "password"))
        if models.storage_t == 'db':
            self.assertEqual(usr.password, None)
        else:
            self.assertEqual(usr.password, "")

    def test_first_name_attr(self):
        """Testing that User has attr first_name, and is an empty string"""
        usr = User()
        self.assertTrue(hasattr(usr, "first_name"))
        if models.storage_t == 'db':
            self.assertEqual(usr.first_name, None)
        else:
            self.assertEqual(usr.first_name, "")

    def test_last_name_attr(self):
        """Testing that User has attr last_name, and is an empty string"""
        usr = User()
        self.assertTrue(hasattr(usr, "last_name"))
        if models.storage_t == 'db':
            self.assertEqual(usr.last_name, None)
        else:
            self.assertEqual(usr.last_name, "")

    def test_to_dict_creates_dict(self):
        """Testing to_dict method creates a dictionary with proper attrs"""
        usr = User()
        new_d = usr.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in usr.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """Testing that values in dict returned from to_dict are correct"""
        t_formt = "%Y-%m-%dT%H:%M:%S.%f"
        usr = User()
        new_d = usr.to_dict()
        self.assertEqual(new_d["__class__"], "User")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], usr.created_at.strftime(t_formt))
        self.assertEqual(new_d["updated_at"], usr.updated_at.strftime(t_formt))

    def test_str(self):
        """Testing that str method has correct output"""
        usr = User()
        string = "[User] ({}) {}".format(usr.id, usr.__dict__)
        self.assertEqual(string, str(usr))
