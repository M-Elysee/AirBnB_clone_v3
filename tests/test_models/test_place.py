#!/usr/bin/python3
"""
Contains TestPlaceDocs classes
"""

from datetime import datetime
import inspect
import models
from models import place
from models.base_model import BaseModel
import pep8
import unittest
Place = place.Place


class TestPlaceDocs(unittest.TestCase):
    """Tests to check documentation and style of Place class"""
    @classmethod
    def setUpClass(cls):
        """Set up for doc tests"""
        cls.place_f = inspect.getmembers(Place, inspect.isfunction)

    def test_pep8_conformance_place(self):
        """Testing that models/place.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        res = pep8s.check_files(['models/place.py'])
        self.assertEqual(res.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_place(self):
        """Testing that tests/test_models/test_place.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        res = pep8s.check_files(['tests/test_models/test_place.py'])
        self.assertEqual(res.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_place_module_docstring(self):
        """Testing for place.py module docstring"""
        self.assertIsNot(place.__doc__, None,
                         "place.py needs a docstring")
        self.assertTrue(len(place.__doc__) >= 1,
                        "place.py needs a docstring")

    def test_place_class_docstring(self):
        """Testing for Place class docstring"""
        self.assertIsNot(Place.__doc__, None,
                         "Place class needs a docstring")
        self.assertTrue(len(Place.__doc__) >= 1,
                        "Place class needs a docstring")

    def test_place_func_docstrings(self):
        """Testing for presence of docstrings in Place methods"""
        for func in self.place_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestPlace(unittest.TestCase):
    """Testing Place class"""
    def test_is_subclass(self):
        """Testing that Place is a subclass of BaseModel"""
        plc = Place()
        self.assertIsInstance(plc, BaseModel)
        self.assertTrue(hasattr(plc, "id"))
        self.assertTrue(hasattr(plc, "created_at"))
        self.assertTrue(hasattr(plc, "updated_at"))

    def test_city_id_attr(self):
        """Testing Place has attr city_id, and is an empty string"""
        plc = Place()
        self.assertTrue(hasattr(plc, "city_id"))
        if models.storage_t == 'db':
            self.assertEqual(plc.city_id, None)
        else:
            self.assertEqual(plc.city_id, "")

    def test_user_id_attr(self):
        """Testing Place has attr user_id, and it's an empty string"""
        plc = Place()
        self.assertTrue(hasattr(plc, "user_id"))
        if models.storage_t == 'db':
            self.assertEqual(plc.user_id, None)
        else:
            self.assertEqual(plc.user_id, "")

    def test_name_attr(self):
        """Testing Place has attr name, and it's an empty string"""
        plc = Place()
        self.assertTrue(hasattr(plc, "name"))
        if models.storage_t == 'db':
            self.assertEqual(plc.name, None)
        else:
            self.assertEqual(plc.name, "")

    def test_description_attr(self):
        """Testing Place has attr description, and it's an empty string"""
        plc = Place()
        self.assertTrue(hasattr(plc, "description"))
        if models.storage_t == 'db':
            self.assertEqual(plc.description, None)
        else:
            self.assertEqual(plc.description, "")

    def test_number_rooms_attr(self):
        """Testing Place has attr number_rooms, and it's an int == 0"""
        plc = Place()
        self.assertTrue(hasattr(plc, "number_rooms"))
        if models.storage_t == 'db':
            self.assertEqual(plc.number_rooms, None)
        else:
            self.assertEqual(type(plc.number_rooms), int)
            self.assertEqual(plc.number_rooms, 0)

    def test_number_bathrooms_attr(self):
        """Testing Place has attr number_bathrooms, and it's an int == 0"""
        plc = Place()
        self.assertTrue(hasattr(plc, "number_bathrooms"))
        if models.storage_t == 'db':
            self.assertEqual(plc.number_bathrooms, None)
        else:
            self.assertEqual(type(plc.number_bathrooms), int)
            self.assertEqual(plc.number_bathrooms, 0)

    def test_max_guest_attr(self):
        """Testing Place has attr max_guest, and it's an int == 0"""
        plc = Place()
        self.assertTrue(hasattr(plc, "max_guest"))
        if models.storage_t == 'db':
            self.assertEqual(plc.max_guest, None)
        else:
            self.assertEqual(type(plc.max_guest), int)
            self.assertEqual(plc.max_guest, 0)

    def test_price_by_night_attr(self):
        """Testing Place has attr price_by_night, and it's an int == 0"""
        plc = Place()
        self.assertTrue(hasattr(plc, "price_by_night"))
        if models.storage_t == 'db':
            self.assertEqual(plc.price_by_night, None)
        else:
            self.assertEqual(type(plc.price_by_night), int)
            self.assertEqual(plc.price_by_night, 0)

    def test_latitude_attr(self):
        """Testing Place has attr latitude, and it's a float == 0.0"""
        plc = Place()
        self.assertTrue(hasattr(plc, "latitude"))
        if models.storage_t == 'db':
            self.assertEqual(plc.latitude, None)
        else:
            self.assertEqual(type(plc.latitude), float)
            self.assertEqual(plc.latitude, 0.0)

    def test_longitude_attr(self):
        """Testing Place has attr longitude, and it's a float == 0.0"""
        plc = Place()
        self.assertTrue(hasattr(plc, "longitude"))
        if models.storage_t == 'db':
            self.assertEqual(plc.longitude, None)
        else:
            self.assertEqual(type(plc.longitude), float)
            self.assertEqual(plc.longitude, 0.0)

    @unittest.skipIf(models.storage_t == 'db', "not testing File Storage")
    def test_amenity_ids_attr(self):
        """Testing Place has attr amenity_ids, and it's an empty list"""
        plc = Place()
        self.assertTrue(hasattr(plc, "amenity_ids"))
        self.assertEqual(type(plc.amenity_ids), list)
        self.assertEqual(len(plc.amenity_ids), 0)

    def test_to_dict_creates_dict(self):
        """Testing to_dict method creates a dictionary with proper attrs"""
        plc = Place()
        new_d = plc.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in plc.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """Testing that values in dict returned from to_dict are correct"""
        t_formt = "%Y-%m-%dT%H:%M:%S.%f"
        plc = Place()
        new_d = plc.to_dict()
        self.assertEqual(new_d["__class__"], "Place")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], plc.created_at.strftime(t_formt))
        self.assertEqual(new_d["updated_at"], plc.updated_at.strftime(t_formt))

    def test_str(self):
        """Testing that str method has correct output"""
        plc = Place()
        string = "[Place] ({}) {}".format(plc.id, plc.__dict__)
        self.assertEqual(string, str(plc))
