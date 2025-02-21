#!/usr/bin/python3
"""
Contains TestReviewDocs classes
"""

from datetime import datetime
import inspect
import models
from models import review
from models.base_model import BaseModel
import pep8
import unittest
Review = review.Review


class TestReviewDocs(unittest.TestCase):
    """Tests to check documentation and style of Review class"""
    @classmethod
    def setUpClass(cls):
        """Set up for doc tests"""
        cls.review_f = inspect.getmembers(Review, inspect.isfunction)

    def test_pep8_conformance_review(self):
        """Testing that models/review.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        res = pep8s.check_files(['models/review.py'])
        self.assertEqual(res.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_review(self):
        """Testing that tests/test_models/test_review.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        res = pep8s.check_files(['tests/test_models/test_review.py'])
        self.assertEqual(res.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_review_module_docstring(self):
        """Testing for review.py module docstring"""
        self.assertIsNot(review.__doc__, None,
                         "review.py needs a docstring")
        self.assertTrue(len(review.__doc__) >= 1,
                        "review.py needs a docstring")

    def test_review_class_docstring(self):
        """Testing for Review class docstring"""
        self.assertIsNot(Review.__doc__, None,
                         "Review class needs a docstring")
        self.assertTrue(len(Review.__doc__) >= 1,
                        "Review class needs a docstring")

    def test_review_func_docstrings(self):
        """Testing for presence of docstrings in Review methods"""
        for func in self.review_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestReview(unittest.TestCase):
    """Testing Review class"""
    def test_is_subclass(self):
        """Testing if Review is a subclass of BaseModel"""
        review = Review()
        self.assertIsInstance(review, BaseModel)
        self.assertTrue(hasattr(review, "id"))
        self.assertTrue(hasattr(review, "created_at"))
        self.assertTrue(hasattr(review, "updated_at"))

    def test_place_id_attr(self):
        """Testing Review has attr place_id, and it's an empty string"""
        review = Review()
        self.assertTrue(hasattr(review, "place_id"))
        if models.storage_t == 'db':
            self.assertEqual(review.place_id, None)
        else:
            self.assertEqual(review.place_id, "")

    def test_user_id_attr(self):
        """Testing Review has attr user_id, and it's an empty string"""
        review = Review()
        self.assertTrue(hasattr(review, "user_id"))
        if models.storage_t == 'db':
            self.assertEqual(review.user_id, None)
        else:
            self.assertEqual(review.user_id, "")

    def test_text_attr(self):
        """Testing Review has attr text, and it's an empty string"""
        review = Review()
        self.assertTrue(hasattr(review, "text"))
        if models.storage_t == 'db':
            self.assertEqual(review.text, None)
        else:
            self.assertEqual(review.text, "")

    def test_to_dict_creates_dict(self):
        """Testing to_dict method creates a dictionary with proper attrs"""
        r = Review()
        new_d = r.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in r.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """Testing that values in dict returned from to_dict are correct"""
        t_formt = "%Y-%m-%dT%H:%M:%S.%f"
        r = Review()
        new_d = r.to_dict()
        self.assertEqual(new_d["__class__"], "Review")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], r.created_at.strftime(t_formt))
        self.assertEqual(new_d["updated_at"], r.updated_at.strftime(t_formt))

    def test_str(self):
        """Testing that str method has correct output"""
        review = Review()
        string = "[Review] ({}) {}".format(review.id, review.__dict__)
        self.assertEqual(string, str(review))
