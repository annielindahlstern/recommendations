"""
TestRecommendationModel API Service Test Suite
=======
Recommendation API Service Test Suite
Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
  codecov --token=$CODECOV_TOKEN
  While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_service.py:TestRecommendationServer
"""

import os
import logging
import unittest

# from unittest.mock import MagicMock, patch
from urllib.parse import quote_plus
from service import app, status
from service.models import DataValidationError, Reason, RecommendationModel, db
from .factories import RecFactory

# Disable all but critical errors during normal test run
# uncomment for debugging failing tests
# logging.disable(logging.CRITICAL)

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
        """Factory method to create recommendations in bulk"""
        recs = []
        for _ in range(count):
            test_rec = RecFactory()
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

    def test_list_recs_empty(self):
        """Test for an empty list"""
        test_rec = RecFactory()
        logging.debug(test_rec)
        resp = self.app.get(BASE_URL, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        empty_response = resp.get_json()
        # There should be no recs
        self.assertIsNone(empty_response)

    def test_list_single_recs(self):
        """Test for a list with one rec"""
        test_rec = RecFactory()
        logging.debug(test_rec)
        self._create_recs(1)

        resp = self.app.get(BASE_URL, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        rec_list = resp.get_json()
        # There should be one rec
        self.assertEqual(len(rec_list), 1)

    def test_list_three_recs(self):
        """Test for a list with three recs"""
        test_rec = RecFactory()
        logging.debug(test_rec)
        self._create_recs(3)

        resp = self.app.get(BASE_URL, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        rec_list = resp.get_json()
        # There should be three recs
        self.assertEqual(len(rec_list), 3)

    def test_index(self):
        """Test the Home Page"""
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], "Recommendation Demo REST API Service")
        
    def test_create_rec(self):
        """Create a new Recommendation"""
        test_rec = RecFactory()
        logging.debug(test_rec)
        resp = self.app.post(
            BASE_URL, json=test_rec.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)
        # Check the data is correct
        new_rec = resp.get_json()
        self.assertEqual(new_rec["name"], test_rec.name, "Names do not match")
        self.assertEqual(
            new_rec["original_product_id"],
            test_rec.original_product_id,
            "original product IDs do not match"
        )
        self.assertEqual(
            new_rec["recommendation_product_id"],
            test_rec.recommendation_product_id,
            "recommendation product IDs do not match"
        )
        self.assertEqual(
            new_rec["recommendation_product_name"],
            test_rec.recommendation_product_name,
            "recommendation product names does not match"
        )
        self.assertEqual(
            new_rec["reason"], test_rec.reason.name, "Reasons does not match"
        )
        # Check that the location header was correct
        resp = self.app.get(location, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_rec = resp.get_json()
        self.assertEqual(new_rec["name"], test_rec.name, "Names do not match")
        self.assertEqual(
            new_rec["original_product_id"],
            test_rec.original_product_id,
            "original product IDs do not match"
        )
        self.assertEqual(
            new_rec["recommendation_product_id"],
            test_rec.recommendation_product_id,
            "recommendation product IDs do not match"
        )
        self.assertEqual(
            new_rec["recommendation_product_name"],
            test_rec.recommendation_product_name,
            "recommendation product names does not match"
        )
        self.assertEqual(
            new_rec["reason"], test_rec.reason.name, "Reasons does not match"
        )

    def test_update_rec(self):
        """Update an existing Recommendation"""
        # create a recommendation to update
        test_rec = RecFactory()
        resp = self.app.post(
            BASE_URL, json=test_rec.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the recommendation
        new_recommendation = resp.get_json()
        logging.debug(new_recommendation)
        new_recommendation["name"] = "Test123"
        resp = self.app.put(
            "/recommendations/{}".format(new_recommendation["id"]),
            json=new_recommendation,
            content_type=CONTENT_TYPE_JSON,
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_rec = resp.get_json()
        self.assertEqual(updated_rec["name"], "Test123")

    def test_delete_recommendation(self):
        """Delete a Recommendation"""
        test_recommendation = self._create_recs(1)[0]
        resp = self.app.delete(
            "{0}/{1}".format(BASE_URL, test_recommendation.id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get(
            "{0}/{1}".format(BASE_URL, test_recommendation.id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_rec(self):
        """Get a single Rec"""
        # get the id of a Rec
        test_rec = self._create_recs(1)[0]
        resp = self.app.get(
            "/recommendations/{}".format(test_rec.id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], test_rec.name)

    def test_get_rec_not_found(self):
        """Get a Rec thats not found"""
        resp = self.app.get("/recommendations/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_query_recommendation_list_by_original_product_id(self):
        """Query Recommendations by Original Product ID"""
        recs = self._create_recs(10)
        test_original_product_id = recs[0].original_product_id
        prod_id_list = [rec for rec in recs if rec.original_product_id == test_original_product_id]

        print(prod_id_list)
        logging.info(
            f"Original Product ID={test_original_product_id}: {len(prod_id_list)} = {prod_id_list}"
        )
        resp = self.app.get(
            BASE_URL, query_string=f"original_product_id = {test_original_product_id}"
        )

        print(resp.get_json())
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(prod_id_list))
        
        # check the data just to be sure
        for rec in data:
            self.assertEqual(rec["original_product_id"], test_original_product_id)
            
    # Testing Sad Paths

    # def test_recs_bad_content_type(self):
    #     """Test for bad content type"""
    #     resp = self.app.get(BASE_URL, content_type='image/jpeg')
    #     self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    #     error_response = resp.get_json()
    #     self.assertEqual(error_response["error"], "Unsupported media type")
    #     self.assertEqual(error_response["message"], "415 Unsupported Media Type: Content-Type must be application/json")
    #     self.assertEqual(error_response["status"], 415)
        
    def test_create_rec_bad_request(self):
        """Test for bad request"""
        resp = self.app.post(
            BASE_URL, json='123', content_type=CONTENT_TYPE_JSON
        )
        error_response = resp.get_json()
        self.assertEqual(error_response["error"], "Bad Request")
        self.assertEqual(error_response["message"], "Invalid recommendation: body of request contained bad or no data string indices must be integers")
        self.assertEqual(error_response["status"], 400)

    def test_recs_not_found(self):
        """Test for unknown path"""
        resp = self.app.get("testing123", content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        error_response = resp.get_json()
        self.assertEqual(error_response["error"], "Not Found")
        self.assertEqual(error_response["message"], "404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.")
        self.assertEqual(error_response["status"], 404)

    def test_recs_method_unsupported(self):
        """Test for unsupported method"""
        resp = self.app.put(BASE_URL, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        error_response = resp.get_json()
        self.assertEqual(error_response["error"], "Method not Allowed")
        self.assertEqual(error_response["message"], "405 Method Not Allowed: The method is not allowed for the requested URL.")
        self.assertEqual(error_response["status"], 405)