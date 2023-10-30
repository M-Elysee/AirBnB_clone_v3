#!/usr/bin/python3
"""
Testing index route
"""
import unittest
import pep8
from os import getenv
import requests
import json
from api.v1.app import *
from flask import request, jsonify
from models.amenity import Amenity
from models import storage


class TestAmenities(unittest.TestCase):
    """ Testing Amenity object """
    def test_lists_amenities(self):
        """ Testing amenity GET route """
        with app.test_client() as tc:
            rspns_1 = tc.get('/api/v1/amenities')
            self.assertEqual(rspns_1.status_code, 200)
            rspns_2 = tc.get('/api/v1/amenities/')
            self.assertEqual(rspns_2.status_code, 200)

    def test_create_amenity(self):
        """ Testing amenity POST route """
        with app.test_client() as tc:
            rspns = tc.post('/api/v1/amenities/',
                            data=json.dumps({"name": "treehouse"}),
                            content_type="application/json")
            self.assertEqual(rspns.status_code, 201)

    def test_delete_amenity(self):
        """ Testing amenity DELETE route """
        with app.test_client() as tc:
            amenity_new = Amenity(name="3 meals a day")
            storage.new(amenity_new)
            rspns = tc.get('api/v1/amenities/{}'.format(amenity_new.id))
            self.assertEqual(rspns.status_code, 200)
            rspns1 = tc.delete('api/v1/amenities/{}'.format(amenity_new.id))
            self.assertEqual(rspns1.status_code, 404)
            rspns2 = tc.get('api/v1/amenities/{}'.format(amenity_new.id))
            self.assertEqual(rspns2.status_code, 404)

    def test_get_amenity(self):
        """ Testing amenity GET by id route """
        with app.test_client() as tc:
            amenity_new = Amenity(name="3 meals a day")
            storage.new(amenity_new)
            rspns = tc.get('api/v1/amenities/{}'.format(amenity_new.id))
            self.assertEqual(rspns.status_code, 200)

    def test_update_amenity(self):
        """ Testing amenity PUT route """
        with app.test_client() as tc:
            amenity_new = Amenity(name="3 meals a day")
            storage.new(amenity_new)
            rspns = tc.put('api/v1/amenities/{}'.format(amenity_new.id),
                           data=json.dumps({"name": "2 meals a day"}),
                           content_type="application/json")
            self.assertEqual(rspns.status_code, 200)


if __name__ == '__main__':
    unittest.main()
