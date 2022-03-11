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