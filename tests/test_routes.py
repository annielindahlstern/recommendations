"""
TestRecommendationModel API Service Test Suite
=======
"""
"""
Recommendation API Service Test Suite
Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
  codecov --token=$CODECOV_TOKEN
  While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_service.py:TestPetServer
"""

import os
import logging
import unittest

# from unittest.mock import MagicMock, patch
from urllib.parse import quote_plus
from service import app, status
from service.models import Reason, RecommendationModel, db
from .factories import RecsFactory

# Disable all but critical errors during normal test run
# uncomment for debugging failing tests
logging.disable(logging.CRITICAL)

# DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/recommendations"
CONTENT_TYPE_JSON = "application/json"

######################################################################
#  T E S T   C A S E S
######################################################################
class TestYourRecommendationServer(unittest.TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        RecommendationModel.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def _create_recs(self, count):
        """Factory method to create pets in bulk"""
        recs = []
        for _ in range(count):
            test_rec = RecsFactory()
            resp = self.app.post(
                BASE_URL, json=test_rec.serialize(), content_type=CONTENT_TYPE_JSON
            )
            self.assertEqual(
                 resp.status_code, status.HTTP_201_CREATED, "Could not create test recommendation"
            )
            new_rec = resp.get_json()
            test_rec.id = new_rec["id"]
            recs.append(test_rec)
        return recs
    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################
    def test_index(self):
        """Test the Home Page"""
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], "Recommendation Demo REST API Service")
    
    
    # def test_create_rec(self):
    #     """Create a new Pet"""
    #     test_rec = RecsFactory()
    #     logging.debug(test_rec)
    #     resp = self.app.post(
    #         BASE_URL, json=test_rec.serialize(), content_type=CONTENT_TYPE_JSON
    #     )
    #     self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
    #     # Make sure location header is set
    #     location = resp.headers.get("Location", None)
    #     self.assertIsNotNone(location)
    #     # Check the data is correct
    #     new_rec = resp.get_json()
    #     self.assertEqual(new_rec["name"], test_rec.name, "Names do not match")
    #     self.assertEqual(
    #         new_rec["prod_A_id"], test_rec.prod_A_id, "Product A IDs do not match"
    #     )
    #     self.assertEqual(
    #         new_rec["prod_B_id"], test_rec.prod_B_id, "Product B IDs do not match"
    #     )
    #     self.assertEqual(
    #         new_rec["prod_B_name"], test_rec.prod_B_name, "Product B names does not match"
    #     )
    #     self.assertEqual(
    #         new_rec["reason"], test_rec.reason.name, "Reasons does not match"
    #     )
    #     # Check that the location header was correct
    #     resp = self.app.get(location, content_type=CONTENT_TYPE_JSON)
    #     self.assertEqual(resp.status_code, status.HTTP_200_OK)
    #     new_rec = resp.get_json()
    #     self.assertEqual(new_rec["name"], test_rec.name, "Names do not match")
    #     self.assertEqual(
    #         new_rec["prod_A_id"], test_rec.prod_A_id, "Product A IDs do not match"
    #     )
    #     self.assertEqual(
    #         new_rec["prod_B_id"], test_rec.prod_B_id, "Product B IDs do not match"
    #     )
    #     self.assertEqual(
    #         new_rec["prod_B_name"], test_rec.prod_B_name, "Product B names does not match"
    #     )
    #     self.assertEqual(
    #         new_rec["reason"], test_rec.reason.name, "Reasons does not match"
    #     )
