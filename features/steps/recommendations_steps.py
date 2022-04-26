"""
Recommendation Steps
Steps file for recommendations.feature
For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import json
import requests
from behave import given
from compare import expect

@given('the following recommendations')
def step_impl(context):
    """ Delete all Recommendations and load new ones """
    headers = {'Content-Type': 'application/json'}
    # list all of the Recommendations and delete them one by one
    context.resp = requests.get(context.base_url + '/recommendations', headers=headers)
    expect(context.resp.status_code).to_equal(200)
    for recommendation in context.resp.json():
        context.resp = requests.delete(context.base_url + '/recommendations/' + str(recommendation["id"]), headers=headers)
        expect(context.resp.status_code).to_equal(204)
    
    # load the database with new Recommendations
    create_url = context.base_url + '/recommendations'
    for row in context.table:
        data = {
            "original_product_name": row['original_product_name'],
            "original_product_id": row['original_product_id'],
            "recommendation_product_id": row['recommendation_product_id'],
            "recommendation_product_name": row['recommendation_product_name'],
            "reason": row['reason'],
            "activated": row['activated'] in ['True', 'true', '1']
        }
        payload = json.dumps(data)
        context.resp = requests.post(create_url, data=payload, headers=headers)
        expect(context.resp.status_code).to_equal(201)