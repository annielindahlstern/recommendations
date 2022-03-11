"""
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
@app.route("/")
def index():

    """Root URL response"""
    app.logger.info("Request for Root URL")
    return (
        jsonify(
            name="Recommendation Demo REST API Service",
            version="1.0",
            paths=url_for("list_recs", _external=True),
        ),
        status.HTTP_200_OK,
    )

######################################################################
# LIST ALL RECS
######################################################################
@app.route("/recs", methods=["GET"])
def list_recs():
    """Returns all of the recs"""
    app.logger.info("Request for rec list")
    recs = []
    category = request.args.get("category")
    name = request.args.get("name")
    if category:
        recs = Rec.find_by_category(category)
    elif name:
        recs = Rec.find_by_name(name)
    else:
        recs = Rec.all()

    results = [rec.serialize() for rec in recs]
    app.logger.info("Returning %d recs", len(results))
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# RETRIEVE A REC
######################################################################
@app.route("/recs/<int:rec_id>", methods=["GET"])
def get_recs(rec_id):
    """
    Retrieve a single Rec
    This endpoint will return a Rec based on it's id
    """
    app.logger.info("Request for rec with id: %s", rec_id)
    rec = Rec.find(rec_id)
    if not rec:
        raise NotFound("Rec with id '{}' was not found.".format(rec_id))

    app.logger.info("Returning rec: %s", rec.name)
    return make_response(jsonify(rec.serialize()), status.HTTP_200_OK)


######################################################################
# ADD A NEW REC
######################################################################
@app.route("/recs", methods=["POST"])
def create_recs():
    """
    Creates a Rec
    This endpoint will create a Rec based the data in the body that is posted
    """
    app.logger.info("Request to create a rec")
    check_content_type("application/json")
    rec = Rec()
    rec.deserialize(request.get_json())
    rec.create()
    message = rec.serialize()
    location_url = url_for("get_recs", rec_id=rec.id, _external=True)

    app.logger.info("Rec with ID [%s] created.", rec.id)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
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
# DELETE A REC
######################################################################
@app.route("/recs/<int:rec_id>", methods=["DELETE"])
def delete_recs(rec_id):
    """
    Delete a Rec
    This endpoint will delete a Rec based the id specified in the path
    """
    app.logger.info("Request to delete rec with id: %s", rec_id)
    rec = Rec.find(rec_id)
    if rec:
        rec.delete()

    app.logger.info("Rec with ID [%s] delete complete.", rec_id)
    return make_response("", status.HTTP_204_NO_CONTENT)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    RecommendationModel.init_db(app)


    ######################################################################
# LIST ALL RECOMMENDATIONS
######################################################################
@app.route("/recs", methods=["GET"])
def list_recs():
    """Returns all of the Recommendations"""
    app.logger.info("Request for recommendation list")
    recs = []
    prod_A_id = request.args.get("prod_A_id")
    prod_B_id = request.args.get("prod_B_id")
    prod_B_name = request.args.get("prod_B_name")
    name = request.args.get("name")
    if prod_A_id:
        recs = RecommendationModel.find_by_prod_A_id(prod_A_id)
    elif name:
        recs = RecommendationModel.find_by_name(name)
    elif prod_B_id:
        recs = RecommendationModel.find_by_prod_B_id(prod_B_id)
    elif prod_B_name:
        recs = RecommendationModel.find_by_prod_B_name(prod_B_name)
    else:
        recs = RecommendationModel.all()

    results = [rec.serialize() for rec in recs]
    app.logger.info("Returning %d recommendation", len(results))
    return make_response(jsonify(results), status.HTTP_200_OK)