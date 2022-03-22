"""
The recommendations resource is a representation a product recommendation based on
another product. In essence it is just a relationship between two products that "go
together" (e.g., radio and batteries, printers and ink, shirts and pants, etc.).
GET /recommendations - Returns a list all of the recommendations
GET /recommendations/{id} - Returns the Recommendation with a given id number
POST /recommendations - creates a new Recommendation record in the database
PUT /recommendations/{id} - updates a Recommendation record in the database
DELETE /recommendations/{id} - deletes a Recommendation record in the database
"""

from flask import jsonify, request, url_for, make_response, abort
from werkzeug.exceptions import NotFound
from . import status  # HTTP Status Codes
from . import app  # Import Flask application

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from service.models import RecommendationModel

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


#####################################################################
# ADD A NEW RECOMMENDATION
#####################################################################
@app.route("/recommendations", methods=["POST"])
def create_recs():
    """
    Creates a Recommendations
    This endpoint will create a Recommendation based the data in the body that is posted
    """
    app.logger.info("Request to create a recommendation")
    check_content_type("application/json")
    rec = RecommendationModel()
    rec.deserialize(request.get_json())
    rec.create()
    message = rec.serialize()
    location_url = url_for("get_recommendation", recommendations_id=rec.id, _external=True)


    app.logger.info("Recommendations with ID [%s] created.", rec.id)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

# LIST ALL RECOMMENDATIONS
######################################################################
@app.route("/recommendations", methods=["GET"])
def list_recs():
    """
    Lists all Recommendations
    This endpoint will list all recommendations in the database.
    """
    app.logger.info("Request to list all recommendations")
    check_content_type("application/json")
    
    all_recs = RecommendationModel.all()
    app.logger.info("Fetched [%i] recs.", len(all_recs))

    data = []
    for rec in all_recs:
        data.append(rec.serialize())

    if data == []:
        return make_response('', status.HTTP_204_NO_CONTENT)
    else:
        return make_response(jsonify(data), status.HTTP_200_OK)

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

######################################################################
# RETRIEVE A RECOMMENDATION
######################################################################
@app.route("/recommendations/<int:recommendations_id>", methods=["GET"])
def get_recommendation(recommendations_id):
    """
    Retrieve a single recommendation
    This endpoint will return a recommendation based on it's id
    """
    app.logger.info("Request for recommendation with id: %s", recommendations_id)
    recommendation = RecommendationModel.find(recommendations_id)
    if not recommendation:
        raise NotFound("Recommendation with id '{}' was not found.".format(recommendations_id))

    app.logger.info("Returning recommendation: %s", recommendation.name)
    return make_response(jsonify(recommendation.serialize()), status.HTTP_200_OK)
######################################################################
# DELETE A RECOMMENDATION
######################################################################
@app.route("/recommendations/<int:recommendations_id>", methods=["DELETE"])
def delete_recommendations(recommendations_id):
    """Delete a Recommendations
        This endpoint will delete a Recommendations based the id specified in the path
    """
    app.logger.info("Request to delete Recommendations with id: %s", recommendations_id)
    recommendations = RecommendationModel.find(recommendations_id)
    if recommendations:
        recommendations.delete()

    app.logger.info("Recommendations with ID [%s] delete complete.", recommendations_id)
    return make_response("", status.HTTP_204_NO_CONTENT)

