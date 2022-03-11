"""
The recommendations resource is a representation a product recommendation based on
another product. In essence it is just a relationship between two products that "go
together" (e.g., radio and batteries, printers and ink, shirts and pants, etc.).
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from . import status  # HTTP Status Codes

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import RecommendationModel, DataValidationError

# Import Flask application
from . import app

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    app.logger.info("Request for Root URL")
    return (
        jsonify(
            name="Rec Demo REST API Service",
            version="1.0",
            paths=url_for("list_recs", _external=True),
        ),
        status.HTTP_200_OK,
    )

######################################################################
# UPDATE AN EXISTING REC
######################################################################
@app.route("/recs/<int:rec_id>", methods=["PUT"])
def update_recs(rec_id):
    """
    Update a Rec
    This endpoint will update a Rec based the body that is posted
    """
    app.logger.info("Request to update rec with id: %s", rec_id)
    check_content_type("application/json")
    rec = Rec.find(rec_id)
    if not rec:
        raise NotFound("Rec with id '{}' was not found.".format(rec_id))
    rec.deserialize(request.get_json())
    rec.id = rec_id
    rec.update()

    app.logger.info("Rec with ID [%s] updated.", rec.id)
    return make_response(jsonify(rec.serialize()), status.HTTP_200_OK)

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    RecommendationModel.init_db(app)