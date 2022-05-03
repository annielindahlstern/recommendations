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

from sqlalchemy import false
from service import app, status
from service.models import DataValidationError, Reason, RecommendationModel, db
from .factories import RecFactory

# Disable all but critical errors during normal test run
# uncomment for debugging failing tests
# logging.disable(logging.CRITICAL)

# DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres/testdb"
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
        self.app = app.test_client()
        db.session.query(RecommendationModel).delete() # clean up the last tests
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    def _create_recommendations(self, count):
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

    def test_list_recommendations_empty(self):
        """Test for an empty list"""
        test_rec = RecFactory()
        logging.debug(test_rec)
        resp = self.app.get(BASE_URL, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        empty_response = resp.get_json()
        # There should be no recs
        self.assertEquals(empty_response, [])

    def test_list_single_recommendations(self):
        """Test for a list with one rec"""
        test_rec = RecFactory()
        logging.debug(test_rec)
        self._create_recommendations(1)

        resp = self.app.get(BASE_URL, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        rec_list = resp.get_json()
        # There should be one rec
        self.assertEqual(len(rec_list), 1)

    def test_list_three_recommendations(self):
        """Test for a list with three recs"""
        test_rec = RecFactory()
        logging.debug(test_rec)
        self._create_recommendations(3)

        resp = self.app.get(BASE_URL, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        rec_list = resp.get_json()
        # There should be three recommendations
        self.assertEqual(len(rec_list), 3)

    def test_index(self):
        """Test the Home Page"""
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # data = resp.get_json()
        # self.assertEqual(data["name"], "Recommendation Demo REST API Service")
        
    def test_create_recommendations(self):
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

    def test_update_recommendations(self):
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

    def test_update_recommendation_not_found(self):
        """Update a non-existing Recommendation"""
        # create a non-existing recommendation to update
        test_rec = RecFactory()
        resp = self.app.put(
            "/recommendations/0",
            json=test_rec.serialize(),
            content_type=CONTENT_TYPE_JSON,
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)


    def test_delete_recommendations(self):
        """Delete a Recommendation"""
        test_recommendation = self._create_recommendations(1)[0]
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
        test_rec = self._create_recommendations(1)[0]
        resp = self.app.get(
            "/recommendations/{}".format(test_rec.id), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], test_rec.name)

    def test_get_recommendations_not_found(self):
        """Get a Rec thats not found"""
        resp = self.app.get("/recommendations/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_query_recommendations_list_by_original_product_id(self):
        """Query Recommendations by Original Product ID"""
        recs = self._create_recommendations(10)
        test_original_product_id = recs[0].original_product_id
        prod_id_list = [rec for rec in recs if rec.original_product_id == test_original_product_id]

        logging.info(
            f"Original Product ID={test_original_product_id}: {len(prod_id_list)} = {prod_id_list}"
        )
        resp = self.app.get(
            BASE_URL, query_string=f"original_product_id={test_original_product_id}"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(prod_id_list))
        
        # check the data just to be sure
        for rec in data:
            self.assertEqual(rec["original_product_id"], test_original_product_id)


    def test_query_recommendation_list_by_name(self):
        """Query Recommendations by Original Product Name"""
        recs = self._create_recommendations(10)
        test_name = recs[0].name
        name_list = [rec for rec in recs if rec.name == test_name]

        logging.info(
            f"Name={test_name}: {len(name_list)} = {name_list}"
        )
        resp = self.app.get(
            BASE_URL, query_string=f"name={test_name}"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(name_list))
        
        # check the data just to be sure
        for rec in data:
            self.assertEqual(rec["name"], test_name)   

    def test_query_recommendation_list_by_recommendation_product_name(self):
        """Query Recommendations by Recommended Product Name"""
        recs = self._create_recommendations(10)
        test_rec_name = recs[0].recommendation_product_name
        Rec_name_list = [rec for rec in recs if rec.recommendation_product_name == test_rec_name]

        logging.info(
            f"Recommendation_Product_Name={test_rec_name}: {len(Rec_name_list)} = {Rec_name_list}"
        )
        resp = self.app.get(
            BASE_URL, query_string=f"recommendation_product_name={test_rec_name}"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(Rec_name_list))
        
        # check the data just to be sure
        for rec in data:
            self.assertEqual(rec["recommendation_product_name"], test_rec_name)   


    # def test_query_recommendation_list_by_activated(self):
    #     """Query Recommendations by Activated Status"""
    #     recs = self._create_recommendations(10)
    #     test_activated = recs[0].activated
    #     activated_list = [rec for rec in recs if rec.activated == test_activated]

    #     logging.info(
    #         f"Activated={test_activated}: {len(activated_list)} = {activated_list}"
    #     )
    #     resp = self.app.get(
    #         BASE_URL, query_string=f"activated={test_activated}"
    #     )
    #     self.assertEqual(resp.status_code, status.HTTP_200_OK)
    #     data = resp.get_json()
    #     self.assertEqual(len(data), len(activated_list))
        
    #     # check the data just to be sure
    #     for rec in data:
    #         self.assertEqual(rec["activated"], test_activated)    

    def test_query_recommendation_list_by_reason(self):
        """Query Recommendations by Reason"""
        recs = self._create_recommendations(10)
        test_reason = recs[0].reason.name
        reason_list = [rec for rec in recs if rec.reason.name == test_reason]

        logging.info(
            f"Reason={test_reason}: {len(reason_list)} = {reason_list}"
        )
        resp = self.app.get(
            BASE_URL, query_string=f"reason={test_reason}"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(reason_list))
        
        # check the data just to be sure
        for rec in data:
            self.assertEqual(rec["reason"], test_reason) 
   
    # Testing Sad Paths

    # def test_recommendations_bad_content_type(self):
    #     """Test for bad content type"""
    #     resp = self.app.get(BASE_URL, content_type='image/jpeg')
    #     self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    #     error_response = resp.get_json()
    #     self.assertEqual(error_response["error"], "Unsupported media type")
    #     self.assertEqual(error_response["message"], "415 Unsupported Media Type: Content-Type must be application/json")
    #     self.assertEqual(error_response["status"], 415)
        
    def test_create_recommendations_bad_request(self):
        """Test for bad request"""
        resp = self.app.post(
            BASE_URL, json='123', content_type=CONTENT_TYPE_JSON
        )
        error_response = resp.get_json()
        self.assertEqual(error_response["error"], "Bad Request")
        self.assertEqual(error_response["message"], "Invalid recommendation: body of request contained bad or no data string indices must be integers")
        self.assertEqual(error_response["status"], 400)

    def test_recommendations_not_found(self):
        """Test for unknown path"""
        resp = self.app.get("testing123", content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        error_response = resp.get_json()
        self.assertEqual(error_response["error"], "Not Found")
        self.assertEqual(error_response["message"], "404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.")
        self.assertEqual(error_response["status"], 404)

    def test_recommendations_method_unsupported(self):
        """Test for unsupported method"""
        resp = self.app.put(BASE_URL, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        error_response = resp.get_json()
        self.assertEqual(error_response["error"], "Method not Allowed")
        self.assertEqual(error_response["message"], "405 Method Not Allowed: The method is not allowed for the requested URL.")
        self.assertEqual(error_response["status"], 405)

    ######################################################################
    # T E S T   A C T I O N S
    ######################################################################

    def activate_test_recommendations(self):
        """Manually Activate Recommendation"""
        rec = RecFactory()
        rec.activated = False
        resp = self.app.post(
            BASE_URL, json=rec.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        rec_data = resp.get_json()
        rec_id = rec_data["id"]
        logging.info(f"Created Recommendation with id {rec_id} = {rec_data}")

        # Request to manually activate recommendation
        resp = self.app.put(f"{BASE_URL}/{rec_id}/activate")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Retrieve the recommendation and make sue it is no longer available
        resp = self.app.get(f"{BASE_URL}/{rec_id}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        rec_data = resp.get_json()
        self.assertEqual(rec_data["id"], rec_id)
        self.assertEqual(rec_data["activated"], True)

    def test_not_activated(self):
        """Activate a recommendation that is already activated"""
        rec = RecFactory()
        rec.activated = True
        resp = self.app.post(
            BASE_URL, json=rec.serialize(), content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        rec_data = resp.get_json()
        rec_id = rec_data["id"]
        logging.info(f"Activate recommendation with id {rec_id} = {rec_data}")

        # Request to activate a recommendation should fail
        resp = self.app.put(f"{BASE_URL}/{rec_id}/activate")
        self.assertEqual(resp.status_code, status.HTTP_409_CONFLICT)

    def activate_test_recommendation_notfound(self):
        """Manually Activate Recommendation not found"""
        resp = self.app.put(f"{BASE_URL}/foo/activate")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)    
    ######################################################################