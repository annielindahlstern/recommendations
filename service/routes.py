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

    """Based URL response"""
    return app.send_static_file("index.html")

    # app.logger.info("Request for Root URL")
    # return (
    #    jsonify(
    #        name="Recommendation Demo REST API Service",
    #        version="1.0",
    #        paths=url_for("list_recommendations", _external=True),
    #    ),
    #    status.HTTP_200_OK,
#    )

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
def create_recommendations():
    """
    Creates a Recommendation
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

######################################################################
# UPDATE AN EXISTING RECOMMENDATION
######################################################################
@app.route("/recommendations/<int:rec_id>", methods=["PUT"])
def update_recommendations(rec_id):
    """
    Update a Recommendation
    This endpoint will update a Recommendation based the body that is posted
    """
    app.logger.info("Request to update recommendation with id: %s", rec_id)
    check_content_type("application/json")
    rec = RecommendationModel.find(rec_id)
    if not rec:
        raise NotFound("Recommendation with id '{}' was not found.".format(rec_id))
    rec.deserialize(request.get_json())
    rec.id = rec_id
    rec.update()

    app.logger.info("Recommendation with ID [%s] updated.", rec.id)
    return make_response(jsonify(rec.serialize()), status.HTTP_200_OK)

######################################################################
# LIST ALL RECOMMENDATIONS
######################################################################
@app.route("/recommendations", methods=["GET"])
def list_recommendations():
    """
    Lists all Recommendations
    This endpoint will list all recommendations in the database.
    """
    app.logger.info("Request to list all recommendations")

    recs = []

    original_product_id = request.args.get("original_product_id")
    name = request.args.get("name")
    recommendation_product_name = request.args.get("recommendation_product_name")
    reason = request.args.get("reason")
    activated = request.args.get("activated")


    if original_product_id:
        app.logger.info("Filtering by original product ID: %s", original_product_id)
        recs = RecommendationModel.find_by_original_product_id(original_product_id)
    elif name:
        app.logger.info("Filtering by name: %s", name)
        recs = RecommendationModel.find_by_name(name)
    elif recommendation_product_name:
        app.logger.info("Filtering by Recommended Product Name: %s", recommendation_product_name)
        recs = RecommendationModel.find_by_recommendation_product_name(recommendation_product_name)
    elif reason:
        app.logger.info("Filtering by reason: %s", original_product_id)
        recs = RecommendationModel.find_by_reason(reason)
    elif activated:
        app.logger.info("Filtering by whether it is activated: %s", activated)
        recs = RecommendationModel.find_by_activated(activated)
    else:
        recs = RecommendationModel.all()

    results = [rec.serialize() for rec in recs]
    app.logger.info("Returning %d recommendations", len(results))
    return make_response(jsonify(results), status.HTTP_200_OK)



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

########################################################
#CREATE A FUNCTION TO MANUALLY ACTIVATE RECOMMENDATION #
########################################################

@app.route("/recommendations/<int:recommendations_id>/activate", methods=["PUT"])
def activate_recommendation(recommendations_id):
    """Endpoint to Activate a Recommendation"""
    app.logger.info("Request to Activate Recommendation with id: %s", recommendations_id)

    rec = RecommendationModel.find(recommendations_id)
    if not rec:
        abort(status.HTTP_404_NOT_FOUND, f"Recommendation with id '{recommendations_id}' was not found.")

    if rec.activated:
        abort(status.HTTP_409_CONFLICT, f"Recommendation with id '{recommendations_id}' is not available.")

    rec.activated = True
    rec.update()
    return jsonify(rec.serialize()), status.HTTP_200_OK

