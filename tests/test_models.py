"""
Test cases for Recommendation Model
"""
import logging
import unittest
import os

from flask import redirect
from service.models import Reason, RecommendationModel, DataValidationError, db
from service import app
from werkzeug.exceptions import NotFound

from tests.factories import RecsFactory


DATABASE_URI = os.getenv(
      "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)
######################################################################
#  R E C O M M E N D A T I O N   M O D E L   T E S T   C A S E S
######################################################################
class TestRecommendationModel(unittest.TestCase):
    """ Test Cases for Recommendation Model """

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        RecommendationModel.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_XXXX(self):
        """ Test something """
        self.assertTrue(True)

    def test_update_a_recommendation(self):
        """Update a Recommendation"""
        rec = RecFactory()
        logging.debug(rec)
        rec.create()
        logging.debug(rec)
        self.assertEqual(rec.id, 1)
        # Change it and save it
        rec.reason = 2
        original_id = rec.id
        rec.update()
        self.assertEqual(rec.id, original_id)
        self.assertEqual(rec.reason, 2)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        recs = Rec.all()
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0].id, 1)
        self.assertEqual(recs[0].reason, 2)

    def test_delete_a_rec(self):
        """Delete a Recommendation"""
        rec = RecFactory()
        rec.create()
        self.assertEqual(len(Rec.all()), 1)
        # delete the rec and make sure it isn't in the database
        rec.delete()
        self.assertEqual(len(Rec.all()), 0)

    def test_serialize_a_rec(self):
        """Test serialization of a Recommendation"""
        rec = PetFactory()
        data = rec.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], rec.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], rec.name)
        self.assertIn("prod_A_id", data)
        self.assertEqual(data["prod_A_id"], rec.prod_A_id)
        self.assertIn("prod_B_name", data)
        self.assertEqual(data["prod_B_name"], rec.prod_B_name)
        self.assertIn("prod_B_id", data)
        self.assertEqual(data["prod_B_id"], rec.prod_B_id)
        self.assertIn("reason", data)
        self.assertEqual(data["reason"], rec.reason)
    
    def test_deserialize_a_rec(self):
        """Test deserialization of a Recommendation"""
        data = {
            "id": 1,
            "name": "Desk",
            "prod_A_id": 2,
            "prod_B_name": "Chair",
            "prod_B_id": 3,
            "reason": 2
        }
        rec = Ret()
        rec.deserialize(data)
        self.assertNotEqual(rec, None)
        self.assertEqual(rec.id, None)
        self.assertEqual(rec.name, "Desk")
        self.assertEqual(rec.prod_A_id, 2)
        self.assertEqual(rec.prod_B_name, Chair)
        self.assertEqual(rec.prod_B_id, 3)
        self.assertEqual(rec.reason, 2)

    def test_create_a_recommendation(self):
        """ Create a recommendation and assert that it exists """
        rec = RecommendationModel(name="iPhone", prod_A_id = 5, prod_B_name = "AirPods", prod_B_id = 10, reason = Reason.ACCESSORY )
        self.assertTrue(rec is not None)
        self.assertEqual(rec.id, None)
        self.assertEqual(rec.name, "iPhone")
        self.assertEqual(rec.prod_A_id, 5)
        self.assertEqual(rec.prod_B_name, "AirPods")
        self.assertEqual(rec.prod_B_id, 10)
        self.assertEqual(rec.reason, Reason.ACCESSORY)
        rec = RecommendationModel(name="iPhone", prod_A_id = 5, prod_B_name = "AirPods", prod_B_id = 8, reason = Reason.CROSS_SELL)
        self.assertEqual(rec.prod_B_id, 8)
        self.assertEqual(rec.reason, Reason.CROSS_SELL)

    def test_add_a_recommendation(self):
        """Create a recommendation and add it to the database"""
        recs = RecommendationModel.all()
        self.assertEqual(recs, [])
        rec = RecommendationModel(name="iPhone", prod_A_id = 5, prod_B_name = "AirPods", prod_B_id = 10, reason = Reason.ACCESSORY )
        self.assertTrue(rec is not None)
        self.assertEqual(rec.id, None)
        rec.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(rec.id, 1)
        recs = RecommendationModel.all()
        self.assertEqual(len(recs), 1)


