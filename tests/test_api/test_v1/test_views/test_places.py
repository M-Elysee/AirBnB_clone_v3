#!/usr/bin/python3
"""testing the index route"""
import unittest
import pep8
from os import getenv
import requests
import json
from api.v1.app import *
from flask import request, jsonify
from models.place import Place
from models.city import City
from models.state import State
from models.user import User
from models import storage


class TestPlaces(unittest.TestCase):
    """ Testing city"""
    def test_lists_places_of_city(self):
        """ Testing places GET route """
        with app.test_client() as tc:
            state_new = State(name="Beckystan")
            storage.new(state_new)
            city_new = City(name="Chensville", state_id=state_new.id)
            storage.new(city_new)
            user_new = User(email="abc@123.com", password="chicken")
            storage.new(user_new)
            new_place = Place(name="Becky's Bathhouse",
                              description="best bath ever", number_rooms=3,
                              number_bathrooms=0, max_guest=2,
                              price_by_night=100, latitude=33.0,
                              longitude=22.1, city_id=city_new.id,
                              user_id=user_new.id)
            storage.new(new_place)
            rspns = tc.get('/api/v1/cities/{}/places'.format(city_new.id))
            self.assertEqual(rspns.status_code, 200)
            rspns2 = tc.get('/api/v1/cities/{}/places/'.format(city_new.id))
            self.assertEqual(rspns.status_code, 200)

    def test_creates_place(self):
        """ Testing place POST route """
        with app.test_client() as tc:
            state_new = State(name="Beckystan")
            storage.new(state_new)
            city_new = City(name="Chensville", state_id=state_new.id)
            storage.new(city_new)
            user_new = User(email="abc@123.com", password="chicken")
            storage.new(user_new)
            new_place = Place(name="Becky's Bathhouse",
                              description="best bath ever", number_rooms=3,
                              number_bathrooms=0, max_guest=2,
                              price_by_night=100, latitude=33.0,
                              longitude=22.1, city_id=city_new.id,
                              user_id=user_new.id)
            storage.new(new_place)
            rspns = tc.post('/api/v1/cities/{}/places'.format(city_new.id),
                          data=json.dumps(dict(name="Becky's Bakery",
                                               description="best egg tarts",
                                               number_rooms=3,
                                               number_bathrooms=0, max_guest=2,
                                               price_by_night=100,
                                               latitude=33.0, longitude=22.1,
                                               city_id=city_new.id,
                                               user_id=user_new.id)),
                          content_type="application/json")
            self.assertEqual(rspns.status_code, 201)

    def test_deletes_place(self):
        """ Testing place DELETE route """
        with app.test_client() as tc:
            state_new = State(name="Beckystan")
            storage.new(state_new)
            city_new = City(name="Chensville", state_id=state_new.id)
            storage.new(city_new)
            user_new = User(email="abc@123.com", password="chicken")
            storage.new(user_new)
            new_place = Place(name="Becky's Bathhouse",
                              description="best bath ever", number_rooms=3,
                              number_bathrooms=0, max_guest=2,
                              price_by_night=100, latitude=33.0,
                              longitude=22.1, city_id=city_new.id,
                              user_id=user_new.id)
            storage.new(new_place)
            rspns = tc.get('api/v1/places/{}'.format(new_place.id))
            self.assertEqual(rspns.status_code, 200)
            rspns1 = tc.delete('api/v1/places/{}'.format(new_place.id))
            self.assertEqual(rspns1.status_code, 404)
            rspns2 = tc.get('api/v1/places/{}'.format(new_place.id))
            self.assertEqual(rspns2.status_code, 404)

    def test_gets_place(self):
        """ Testing place GET by id route """
        with app.test_client() as tc:
            state_new = State(name="Beckystan")
            storage.new(state_new)
            city_new = City(name="Chensville", state_id=state_new.id)
            storage.new(city_new)
            user_new = User(email="abc@123.com", password="chicken")
            storage.new(user_new)
            new_place = Place(name="Becky's Bathhouse",
                              description="best bath ever", number_rooms=3,
                              number_bathrooms=0, max_guest=2,
                              price_by_night=100, latitude=33.0,
                              longitude=22.1, city_id=city_new.id,
                              user_id=user_new.id)
            storage.new(new_place)
            rspns = tc.get('/api/v1/cities/{}/places'.format(city_new.id))
            self.assertEqual(rspns.status_code, 200)

    def test_updates_place(self):
        """ Testing place PUT route """
        with app.test_client() as tc:
            state_new = State(name="Beckystan")
            storage.new(state_new)
            city_new = City(name="Chensville", state_id=state_new.id)
            storage.new(city_new)
            user_new = User(email="abc@123.com", password="chicken")
            storage.new(user_new)
            new_place = Place(name="Becky's Bathhouse",
                              description="best bath ever", number_rooms=3,
                              number_bathrooms=0, max_guest=2,
                              price_by_night=100, latitude=33.0,
                              longitude=22.1, city_id=city_new.id,
                              user_id=user_new.id)
            storage.new(new_place)
            rspns = tc.put('api/v1/places/{}'.format(new_place.id),
                         data=json.dumps({"name": "Becky's Billards"}),
                         content_type="application/json")
            # data = json.loads(rspns.data.decode('utf-8'))
            # print(data)
            self.assertEqual(rspns.status_code, 200)


if __name__ == '__main__':
    unittest.main()
