"""
Models for RecommendationModel
All of the models are stored in this module
"""
import logging
from enum import Enum
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

class Reason(Enum):
    """Enumeration of Different Reasons"""

    CROSS_SELL = 0
    UP_SELL = 1
    ACCESSORY = 2
    OTHER  = 3

class RecommendationModel(db.Model):
    """
    Class that represents a Recommendation
    """

    app = None

    # Table Schema

    id = db.Column(db.Integer, primary_key=True)

    # what is the original product (original product)
    name = db.Column(db.String(63), nullable = False)
    original_product_id = db.Column(db.Integer, nullable = False)
    # what is being recommended based on the product (recommendation product)
    recommendation_product_name = db.Column(db.String(63), nullable = False)
    recommendation_product_id = db.Column(db.Integer, nullable = False)

    # the Reason for the recommendation based on enumerators
    reason = db.Column(db.Enum(Reason), nullable=False, server_default=(Reason.OTHER.name))

    def __repr__(self):
        return "<Recommendation %r id=[%s]>" % (self.name, self.id)

    def create(self):
        """
        Creates a RecommendationModel to the database
        """
        logger.info("Creating Recommendation for %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Pet to the database
        """
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """ Removes a RecommendationModel from the data store """
        logger.info("Deleting Recommendation for %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a YourResourceModel into a dictionary """
        return {
            "id": self.id,
            "name": self.name,
            "original_product_id": self.original_product_id,
            "recommendation_product_name": self.recommendation_product_name,
            "recommendation_product_id": self.recommendation_product_id,
            "reason" :self.reason.name
        }

    def deserialize(self, data):
        """
        Deserializes a Recommendation from a dictionary
        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.original_product_id = data["original_product_id"]
            self.recommendation_product_name = data["recommendation_product_name"]
            self.recommendation_product_id = data["recommendation_product_id"]
            self.reason = getattr(Reason, data["reason"])  # create enum from string
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError("Invalid pet: missing " + error.args[0]) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid pet: body of request contained bad or no data " + str(error)
            ) from error
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the RecommendationModel in the database """
        logger.info("Processing all RecommendationModels")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a YourResourceModel by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_or_404(cls, by_id):
        """ Find a YourResourceModel by it's id """
        logger.info("Processing lookup or 404 for id %s ...", by_id)
        return cls.query.get_or_404(by_id)

    @classmethod
    def find_by_name(cls, name):

        """Returns all Recommendations with the given name
        Args:
            name (string): the name of the RecommendationModel you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_original_product_id(cls, original_product_id):
        """Returns all Recommendations with the given original product ID
        Args:
            name (string): the ID of the original product you want to match
        """
        logger.info("Processing name query for %r ...", original_product_id)
        return cls.query.filter(cls.original_product_id == original_product_id)

    @classmethod
    def find_by_reason(cls, reason : Reason = Reason.OTHER):
        """Returns all Recommendations with the given reason
        Args:
            name (string): the reason of the Recommendation you want to match
        """
        logger.info("Processing name query for %s ...", reason)
        return cls.query.filter(cls.reason == reason)

    @classmethod
    def find_by_recommendation_product_id(cls, recommendation_product_id):
        """Returns all Recommendations with the given recommendation product ID
        Args:
            name (string): the recommended product ID of the Recommendation you want to match
        """
        logger.info("Processing name query for %r ...", recommendation_product_id)
        return cls.query.filter(cls.recommendation_product_id == recommendation_product_id)

    @classmethod
    def find_by_recommendation_product_name(cls, recommendation_product_name):
        """Returns all Recommendations with the given recommendation product name
        Args:
            name (string): the recommended product name of the Recommendation you want to match
        """
        logger.info("Processing name query for %r ...", recommendation_product_name)
        return cls.query.filter(cls.recommendation_product_id == recommendation_product_name)
