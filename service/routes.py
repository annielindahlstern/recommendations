"""
The recommendations resource is a representation a product recommendation based on
another product. In essence it is just a relationship between two products that "go
together" (e.g., radio and batteries, printers and ink, shirts and pants, etc.).
GET /pets - Returns a list all of the Pets
GET /pets/{id} - Returns the Pet with a given id number
POST /pets - creates a new Pet record in the database
PUT /pets/{id} - updates a Pet record in the database
DELETE /pets/{id} - deletes a Pet record in the database
"""

from flask import jsonify, request, url_for, make_response, abort
from werkzeug.exceptions import NotFound
from . import status  # HTTP Status Codes
from . import app  # Import Flask application

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import RecommendationModel, DataValidationError

######################################################################
# GET INDEX
######################################################################
# @app.route("/")
# def index():

#    """Root URL response"""
#    app.logger.info("Request for Root URL")
#    return (
#        jsonify(
#            name="Recommendation Demo REST API Service",
#            version="1.0",
#            paths=url_for("list_recs", _external=True),
#        ),
#        status.HTTP_200_OK,
#    )

######################################################################
# UPDATE AN EXISTING REC
######################################################################
# @app.route("/recs/<int:rec_id>", methods=["PUT"])
# def update_recs(rec_id):
#     """
#     Update a Rec
#     This endpoint will update a Rec based the body that is posted
#     """
#     app.logger.info("Request to update rec with id: %s", rec_id)
#     check_content_type("application/json")
#     rec = Rec.find(rec_id)
#     if not rec:
#         raise NotFound("Rec with id '{}' was not found.".format(rec_id))
#     rec.deserialize(request.get_json())
#     rec.id = rec_id
#     rec.update()

#     app.logger.info("Rec with ID [%s] updated.", rec.id)
#     return make_response(jsonify(rec.serialize()), status.HTTP_200_OK)

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    RecommendationModel.init_db(app)


######################################################################
# ADD A NEW PET
######################################################################
# @app.route("/recommendations", methods=["POST"])
# def create_recs():
#     """
#     Creates a Recommendations
#     This endpoint will create a Pet based the data in the body that is posted
#     """
#     app.logger.info("Request to create a pet")
#     check_content_type("application/json")
#     rec = RecommendationModel()
#     rec.deserialize(request.get_json())
#     rec.create()
#     message = rec.serialize()
#     location_url = url_for("get_recs", rec_id=rec.id, _external=True)

#     app.logger.info("Recommendations with ID [%s] created.", rec.id)
#     return make_response(
#         jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
#     )

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "Content-Type must be {}".format(media_type),
    )
