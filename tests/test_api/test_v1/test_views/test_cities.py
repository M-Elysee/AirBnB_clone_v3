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
from models.state import State
from models.city import City
from models import storage


class TestCities(unittest.TestCase):
    """ Testing city """
    def test_lists_cities_of_state(self):
        """ Testing cities GET route """
        with app.test_client() as tc:
            state_new = State(name="Beckystan")
            storage.new(state_new)
            city_new = City(name="Chensville", state_id=state_new.id)
            storage.new(city_new)
            rspns_1 = tc.get('/api/v1/states/{}/cities'.format(state_new.id))
            self.assertEqual(rspns_1.status_code, 200)
            rspns_2 = tc.get('/api/v1/states/{}/cities/'.format(state_new.id))
            self.assertEqual(rspns.status_code, 200)

    def test_creates_city(self):
        """ Testing city POST route """
        with app.test_client() as tc:
            state_new = State(name="Beckystan")
            storage.new(state_new)
            city_new = City(name="Chensville", state_id=state_new.id)
            storage.new(city_new)
            rspns = tc.post('/api/v1/states/{}/cities'.format(state_new.id),
                            data=json.dumps({"name": "Chentown"}),
                            content_type="application/json")
            self.assertEqual(rspns.status_code, 201)

    def test_deletes_city(self):
        """ Testing city DELETE route """
        with app.test_client() as tc:
            state_new = State(name="Beckystan")
            storage.new(state_new)
            city_new = City(name="Chensville", state_id=state_new.id)
            storage.new(city_new)
            rspns = tc.get('api/v1/cities/{}'.format(city_new.id))
            self.assertEqual(rspns.status_code, 200)
            rspns1 = tc.delete('api/v1/cities/{}'.format(city_new.id))
            self.assertEqual(rspns1.status_code, 404)
            rspns2 = tc.get('api/v1/cities/{}'.format(city_new.id))
            self.assertEqual(rspns2.status_code, 404)

    def test_gets_city(self):
        """ Testing city GET by id route """
        with app.test_client() as tc:
            state_new = State(name="Beckystan")
            storage.new(state_new)
            city_new = City(name="Chensville", state_id=state_new.id)
            storage.new(city_new)
            rspns = tc.get('/api/v1/states/{}/cities'.format(state_new.id))
            self.assertEqual(rspns.status_code, 200)

    def test_updates_city(self):
        """ Test city PUT route """
        with app.test_client() as tc:
            state_new = State(name="Beckystan")
            storage.new(state_new)
            city_new = City(name="Chensville", state_id=state_new.id)
            storage.new(city_new)
            rspns = tc.put('api/v1/cities/{}'.format(city_new.id),
                           data=json.dumps({"name": "Becktropolis"}),
                           content_type="application/json")
            self.assertEqual(rspns.status_code, 200)


if __name__ == '__main__':
    unittest.main()
