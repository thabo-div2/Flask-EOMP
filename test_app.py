# class 2 Thabo Setsubi
# Testing the app.py file
import json
import unittest
from app import app
import db
import os


# Testing Database class
class ApiTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_user(self):
        payload = json.dumps({
            "username": "thabo",
            "password": "abcxyz"
        })

        response = self.app.post('/auth')

        self.assertEqual(str, type(response.json['id']))
        self.assertEqual(200, response.status_code)
        print(response)

    def test_product(self):
        response = self.app.get("/view-profile/3")
        self.assertEqual(200, response.status_code)
        self.assertEqual(str, response.json['id'])
        print(response)

    def test_sending_email(self):
        pass


if __name__ == "__main__":
    unittest.main()
