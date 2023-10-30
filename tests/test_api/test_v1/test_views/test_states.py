#!/usr/bin/python3
"""testing the index route"""
import unittest
import pep8
from os import getenv
import requests
import json
from api.v1.app import *
from flask import request, jsonify
from models.state import State
from models import storage


class TestStates(unittest.TestCase):
    """ Testing state """
    def test_lists_states(self):
        """ Testing state GET route """
        with app.test_client() as tc:
            rspns = tc.get('/api/v1/states')
            self.assertEqual(rspns.status_code, 200)
            rspns2 = tc.get('/api/v1/states/')
            self.assertEqual(rspns.status_code, 200)

    def test_gets_state(self):
        """ Testing state GET by id route """
        with app.test_client() as tc:
            state_new = State(name="Beckystan")
            storage.new(state_new)
            rspns = tc.get('api/v1/states/{}'.format(state_new.id))
            self.assertEqual(rspns.status_code, 200)

    def test_deletes_state(self):
        """ Testing state DELETE route """
        with app.test_client() as tc:
            state_new = State(name="Beckystan")
            storage.new(state_new)
            rspns = tc.get('api/v1/states/{}'.format(state_new.id))
            self.assertEqual(rspns.status_code, 200)
            rspns1 = tc.delete('api/v1/states/{}'.format(state_new.id))
            self.assertEqual(rspns1.status_code, 404)
            rspns2 = tc.get('api/v1/states/{}'.format(state_new.id))
            self.assertEqual(rspns2.status_code, 404)

    def test_creates_state(self):
        """ Testing state POST route """
        with app.test_client() as tc:
            rspns = tc.post('/api/v1/states/',
                          data=json.dumps({"name": "California"}),
                          content_type="application/json")
            self.assertEqual(rspns.status_code, 201)

    def test_updates_state(self):
        """ Testing state PUT route """
        with app.test_client() as tc:
            state_new = State(name="Beckystan")
            storage.new(state_new)
            rspns = tc.put('api/v1/states/{}'.format(state_new.id),
                         data=json.dumps({"name": "Beckytopia"}),
                         content_type="application/json")
            self.assertEqual(rspns.status_code, 200)


if __name__ == '__main__':
    unittest.main()
