#!/usr/bin/python3
"""testing the index route"""
import unittest
import pep8
from os import getenv
import requests
import json
from api.v1.app import *


storage = getenv("HBNB_TYPE_STORAGE")


class TestIndex(unittest.TestCase):
    """ Test index """
    def test_status(self):        
        """ Testing status function"""
        with app.test_client() as tc:
            rspns = tc.get('/api/v1/status')
            dta = json.loads(rspns.data.decode('utf-8'))
            self.assertEqual(dta, {'status': 'OK'})


    def test_count(self):
        """ Testing count """
        with app.test_client() as tc:
            rspns = tc.get('/api/v1/stats')
            dta = json.loads(rspns.data.decode('utf-8'))
            for k, val in dta.items():
                self.assertIsInstance(val, int)
                self.assertTrue(val >= 0)

    def test_404(self):
        """ Testing for 404 error """
        with app.test_client() as tc:
            rspns = tc.get('/api/v1/yabbadabbadoo')
            dta = json.loads(rspns.data.decode('utf-8'))
            self.assertEqual(dta, {"error": "Not found"})


if __name__ == '__main__':
    unittest.main()
