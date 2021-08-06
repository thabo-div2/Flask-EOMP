# class 2 Thabo Setsubi
# Testing the app.py file
import unittest
from app import app


# Testing Api
class ApiTest(unittest.TestCase):

    # check if responses is 200
    def test_user_register(self):
        test = app.test_client(self)
        response = test.get('/user-registration/')
        status = response.status_code
        self.assertEqual(status, 405)

    # check if response is 200
    def test_user_id(self):
        test = app.test_client(self)
        response = test.get('/view-profile/3')
        status = response.status_code
        self.assertEqual(status, 200)

    # check if responses is 200
    def test_products(self):
        test = app.test_client(self)
        response = test.get('/show-products/')
        status = response.status_code
        self.assertEqual(status, 404)

    # check if responses is 200
    def test_product_id(self):
        test = app.test_client(self)
        response = test.get('/edit-product/3/')
        status = response.status_code
        self.assertEqual(status, 404)

    # check content type
    def test_type(self):
        test = app.test_client(self)
        response = test.get('/show-products/')
        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    # check the email
    def test_sending_email(self):
        test = app.test_client(self)
        response = test.get('/send-email')
        status = response.status_code
        self.assertEqual(status, 404)


if __name__ == "__main__":
    unittest.main()
