# class 2 Thabo Setsubi
# Testing the app.py file
import unittest
import app
import os


TEST_DB = "test.db"


# Testing Database class
class TestDatabase(unittest.TestCase):
    def setUp(self, db=None):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                                os.path.join(app.config['BASEDIR'], TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()


if __name__ == "__main__":
    unittest.main()
