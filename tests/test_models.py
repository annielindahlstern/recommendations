"""
Test cases for YourResourceModel Model
"""
import logging
import unittest
import os

from flask import redirect
from service.models import Reason, RecommendationModel, DataValidationError, db
from service import app
from werkzeug.exceptions import NotFound

from tests.factories import RecsFactory

######################################################################
#  <your resource name>   M O D E L   T E S T   C A S E S
######################################################################
class TestRecommendationModel(unittest.TestCase):
    """ Test Cases for YourResourceModel Model """

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

    def test_add_a_pet(self):
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

