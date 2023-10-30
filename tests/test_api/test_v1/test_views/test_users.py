#!/usr/bin/python3
"""testing the index route"""
from api.v1.app import *
import json
import unittest
import pep8
from os import getenv
import requests
from flask import request, jsonify
from models.user import User
from models import storage


class TestUsers(unittest.TestCase):
    """ Testing user """
    def test_lists_users(self):
        """ Testing user GET route """
        with app.test_client() as tc:
            rspns = tc.get('/api/v1/users')
            self.assertEqual(rspns.status_code, 200)
            rspns2 = tc.get('/api/v1/users/')
            self.assertEqual(rspns.status_code, 200)

    def test_creates_user(self):
        """test user POST route"""
        with app.test_client() as tc:
            rspns = tc.post('/api/v1/users/',
                          data=json.dumps(dict(email="123@abtc.com",
                                               password="0000")),
                          content_type="application/json")
            self.assertEqual(rspns.status_code, 201)

    def test_deletes_user(self):
        """ Testing user DELETE route """
        with app.test_client() as tc:
            new_user = User(first_name="Mojo", last_name="Jojo",
                            email="123@abtc.com", password="0000")
            storage.new(new_user)
            rspns = tc.get('api/v1/users/{}'.format(new_user.id))
            self.assertEqual(rspns.status_code, 200)
            rspns1 = tc.delete('api/v1/users/{}'.format(new_user.id))
            self.assertEqual(rspns1.status_code, 404)
            rspns2 = tc.get('api/v1/users/{}'.format(new_user.id))
            self.assertEqual(rspns2.status_code, 404)

    def test_gets_user(self):
        """ Testing user GET by id route """
        with app.test_client() as tc:
            new_user = User(first_name="Mojo", last_name="Jojo",
                            email="123@abtc.com", password="0000")
            storage.new(new_user)
            rspns = tc.get('api/v1/users/{}'.format(new_user.id))
            self.assertEqual(rspns.status_code, 200)

    def test_updates_user(self):
        """ Testing user PUT route """
        with app.test_client() as tc:
            new_user = User(first_name="Mojo", last_name="Jojo",
                            email="123@abtc.com", password="0000")
            storage.new(new_user)
            rspns = tc.put('api/v1/users/{}'.format(new_user.id),
                         data=json.dumps({"first_name": "Sailor",
                                          "last_name": "Moon"}),
                         content_type="application/json")
            self.assertEqual(rspns.status_code, 200)


if __name__ == '__main__':
    unittest.main()
