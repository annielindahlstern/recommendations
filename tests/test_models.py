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

from tests.factories import RecFactory


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

    def test_update_a_recommendation(self):
        """Update a Recommendation"""
        rec = RecFactory()
        logging.debug(rec)
        rec.create()
        logging.debug(rec)
        self.assertEqual(rec.id, 1)
        # Change it and save it
        rec.reason = Reason.UP_SELL
        original_id = rec.id
        rec.update()
        self.assertEqual(rec.id, original_id)
        self.assertEqual(rec.reason, Reason.UP_SELL)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        recs = RecommendationModel.all()
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0].id, 1)
        self.assertEqual(recs[0].reason, Reason.UP_SELL)

    def test_delete_a_rec(self):
        """Delete a Recommendation"""
        rec = RecFactory()
        rec.create()
        self.assertEqual(len(RecommendationModel.all()), 1)
        # delete the rec and make sure it isn't in the database
        rec.delete()
        self.assertEqual(len(RecommendationModel.all()), 0)

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

    def test_serialize_a_recommendation(self):
        """Test serialization of a Recommendation"""
        rec = RecFactory()
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
        self.assertEqual(data["reason"], rec.reason.name)

    def test_deserialize_a_rec(self):
        """Test deserialization of a Recommendation"""
        data = {
            "id": 1,
            "name": "iPhone",
            "prod_A_id": 5,
            "prod_B_name": "AirPods",
            "prod_B_id": 10,
            "reason": "ACCESSORY",
        }
        rec = RecommendationModel()
        rec.deserialize(data)
        self.assertNotEqual(rec, None)
        self.assertEqual(rec.id, None)
        self.assertEqual(rec.name, "iPhone")
        self.assertEqual(rec.prod_A_id, 5)
        self.assertEqual(rec.prod_B_name, "AirPods")
        self.assertEqual(rec.prod_B_id, 10)
        self.assertEqual(rec.reason, Reason.ACCESSORY)

    def test_deserialize_missing_data(self):
        """Test deserialization of a Recommendation with missing data"""
        data ={
            "id": 1,
            "name": "iPhone",
            "prod_A_id": 5,
            "prod_B_name": "AirPods",
            "prod_B_id": 10,
        }
        rec = RecommendationModel()
        self.assertRaises(DataValidationError, rec.deserialize, data)

    def test_deserialize_bad_data(self):
        """Test deserialization of bad data"""
        data = "this is not a dictionary"
        rec = RecommendationModel()
        self.assertRaises(DataValidationError, rec.deserialize, data)

    def test_deserialize_bad_reason(self):
        """Test deserialization of bad available attribute"""
        test_rec = RecFactory()
        data = test_rec.serialize()
        data["reason"] = "Bad Item"
        rec = RecommendationModel()
        self.assertRaises(DataValidationError, rec.deserialize, data)

    def test_find_recommendation(self):
        """Find a Recommendation by ID"""
        recs = RecFactory.create_batch(3)
        for rec in recs:
            rec.create()
        logging.debug(recs)
        # make sure they got saved
        self.assertEqual(len(RecommendationModel.all()), 3)
        # find the 2nd pet in the list
        rec = RecommendationModel.find(recs[1].id)
        self.assertIsNot(rec, None)
        self.assertEqual(rec.id, recs[1].id)
        self.assertEqual(rec.name, recs[1].name)
        self.assertEqual(rec.prod_A_id, recs[1].prod_A_id)
        self.assertEqual(rec.prod_B_name, recs[1].prod_B_name)
        self.assertEqual(rec.prod_B_id, recs[1].prod_B_id)
        self.assertEqual(rec.reason, recs[1].reason)

    def test_find_by_name(self):
        """Find a Recommendation by Name"""
        RecommendationModel(name="iPhone", prod_A_id=1,prod_B_name="AirPods", prod_B_id=10, reason = Reason.ACCESSORY).create()
        RecommendationModel(name="Radio", prod_A_id=2,prod_B_name="Batteries", prod_B_id=6, reason = Reason.CROSS_SELL).create()
        recs = RecommendationModel.find_by_name("iPhone")
        self.assertEqual(recs[0].prod_B_name, "AirPods")
        self.assertEqual(recs[0].prod_A_id, 1)
        self.assertEqual(recs[0].prod_B_id, 10)
        self.assertEqual(recs[0].reason, Reason.ACCESSORY)

    def test_find_by_product_A_id(self):
        """Find Recommendation by product_A_id"""
        RecommendationModel(name="iPhone", prod_A_id=1,prod_B_name="AirPods", prod_B_id=10, reason = Reason.ACCESSORY).create()
        RecommendationModel(name="Radio", prod_A_id=2,prod_B_name="Batteries", prod_B_id=6, reason = Reason.CROSS_SELL).create()
        recs = RecommendationModel.find_by_prod_A_id(1)
        self.assertEqual(recs[0].prod_B_name, "AirPods")
        self.assertEqual(recs[0].name, "iPhone")
        self.assertEqual(recs[0].prod_B_id, 10)
        self.assertEqual(recs[0].reason, Reason.ACCESSORY)

    def test_find_by_reason(self):
        """Find Recommendations by Reason"""
        RecommendationModel(name="iPhone", prod_A_id=1,prod_B_name="AirPods", prod_B_id=10, reason = Reason.ACCESSORY).create()
        RecommendationModel(name="Radio", prod_A_id=2,prod_B_name="Batteries", prod_B_id=6, reason = Reason.CROSS_SELL).create()
        RecommendationModel(name="Printer", prod_A_id=125,prod_B_name="Ink", prod_B_id=33, reason = Reason.CROSS_SELL).create()
        recs = RecommendationModel.find_by_reason(Reason.CROSS_SELL)
        rec_list = list(recs)
        self.assertEqual(len(rec_list), 2)
        self.assertEqual(recs[0].prod_B_name, "Batteries")
        self.assertEqual(recs[0].name, "Radio")
        self.assertEqual(recs[0].prod_B_id, 6)
        recs = RecommendationModel.find_by_reason(Reason.ACCESSORY)
        rec_list = list(recs)
        self.assertEqual(len(rec_list), 1)

    def test_find_by_prod_B_id(self):
        """Find Recommendations by product_B_id"""
        RecommendationModel(name="iPhone", prod_A_id=1,prod_B_name="AirPods", prod_B_id=10, reason = Reason.ACCESSORY).create()
        RecommendationModel(name="Radio", prod_A_id=2,prod_B_name="Batteries", prod_B_id=6, reason = Reason.CROSS_SELL).create()
        recs = RecommendationModel.find_by_prod_B_id(10)
        self.assertEqual(recs[0].prod_B_name, "AirPods")
        self.assertEqual(recs[0].name, "iPhone")
        self.assertEqual(recs[0].prod_A_id, 1)
        self.assertEqual(recs[0].reason, Reason.ACCESSORY)

    def test_find_or_404_found(self):
        """Find or return 404 found"""
        recs = RecFactory.create_batch(3)
        for rec in recs:
            rec.create()

        rec = RecommendationModel.find_or_404(recs[1].id)
        self.assertIsNot(rec, None)
        self.assertEqual(rec.id, recs[1].id)
        self.assertEqual(rec.name, recs[1].name)
        self.assertEqual(rec.prod_A_id, recs[1].prod_A_id)
        self.assertEqual(rec.prod_B_name, recs[1].prod_B_name)
        self.assertEqual(rec.prod_B_id, recs[1].prod_B_id)

    def test_find_or_404_not_found(self):
        """Find or return 404 NOT found"""
        self.assertRaises(NotFound, RecommendationModel.find_or_404, 0)
