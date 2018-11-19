import pytest
import json
from app import app

orders = {}

@pytest.fixture(scope='function')
def client():
    test_client=app.test_client()
    cxt = app.app_context()
    cxt.push()
    yield test_client
    cxt.pop()

#Encode test requests to json
def post_json(client, url, json_dict):
    """Send dictionary json_dict as a json to the specified url """
    return client.post(url, data=json.dumps(json_dict), content_type='application/json')
#Decode json requests
def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))
#Encoding for put request
def put_json(client, url, json_dict):
    """Send dictionary json_dict as a json to the specified url """
    return client.put(url, data=json.dumps(json_dict), content_type='application/json')

#Test order creation and expected reponse code and content
def test_order_creation(client):
    response = post_json(client, 'api/v1/parcels', data['basic'])
    assert response.status_code == 201
    assert json_of_response(response) == {'order': data['jsn_basic']}

#Test order with missing mandatory field not created, correct error message in response
def test_incomplete_order_not_created(client):
    response = post_json(client, 'api/v1/parcels', data['incomplete'])
    assert response.status_code == 400
    assert json_of_response(response) == {'error': 'bad request'}

#Test order created with missing optional components filled by defaults
def test_creation_fills_missing_optional_fields_with_defaults(client):
    response = post_json(client, 'api/v1/parcels', data['basic'])
    assert response.status_code == 201
    assert len(json_of_response(response)['order']) == 13

#Test api can retrieve all orders; correct response code and body
def test_fetch_all_orders(client):
    post_json(client, 'api/v1/parcels', data['basic'])
    post_json(client, 'api/v1/parcels', data['complete'])
    response = client.get('api/v1/parcels')
    assert response.status_code == 200  
    assert json_of_response(response) == {'orders': orders}

##Test api can retrieve all orders created by a given user
#def test_fetch_all_user_orders(client):
#    post_json(client, 'api/v1/parcels', data['basic'])
#    post_json(client, 'api/v1/parcels', data['basic'])
#    post_json(client, 'api/v1/parcels', data['second_user'])
#    post_json(client, 'api/v1/parcels', data['basic'])
#    response = client.get('api/v1/1/parcels')
#    assert response.status_code == 200
#    assert len(json_of_response(response)['orders']) == 3

#Test non admin user cannot retrive all orders, correct response: code and message
#needs user auth first

##Test correct response when no orders to fetch
#def test_fetch_empty(client):
#    response = client.get('api/v1/parcels')
#    assert response.status_code == 404
#    assert json_of_response(response) == {'result': 'no orders'}
#
#Test api can fetch specific order; correct response: __ code and body
def test_fetch_single(client):
    post_json(client, 'api/v1/parcels', data['basic'])
    post_json(client, 'api/v1/parcels', data['complete'])
    response = client.get('api/v1/parcels/1')
    assert response.status_code == 200
    assert json_of_response(response) == {'order': data['jsn_basic']}

##Test only owner and admin can fetch specific order
##needs user auth
#
##Test correct response if specified order missing
#def test_fetch_missing_order(client):
#    post_json(client, 'api/v1/parcels', data['basic'])
#    response = client.get('api/v1/parcels/2')
#    assert response.status_code == 404
#    assert json_of_response(response) == {'result': 'order non existent'}
#
##Test correct response for denial of specific order fetch request
##needs user auth
#
#Test order before delivery can be cancelled
def test_cancel_order(client):
    res = post_json(client, 'api/v1/parcels', data['basic'])
    assert res.status_code == 201
    response = put_json(client, 'api/v1/parcels/1/cancel', {"status": ""})
    assert response.status_code == 200
    assert json_of_response(response) == {'operation': 'canceled'}

#Test order after delivery can not be canceled, correct response; message and code
#def test_cancel_order_delivered_fails(client):
#    res = post_json(client, 'api/v1/parcels', data['basic'])
#    assert res.status_code == 201
#    put_json(client, 'api/v1/parcels/1/update', {"status": "delivered"})
#    response = put_json(client, 'api/v1/parcels/1/cancel', {"status": ""})
#    assert json_of_response(response) == {'result': 'parcel already delivered'}

#Test parcel destination can be changed
def test_order_destination_change(client):
    result = post_json(client, 'api/v1/parcels', data['basic'])
    assert "zambia" not in json_of_response(result)['order']
    response = put_json(client, 'api/v1/parcels/1/changeDestination', {"destination": "zambia"})
    assert response.status_code == 200
    assert json_of_response(response)['order']['destination'] == 'zambia'

#Test order status can be changed
def test_order_status_change(client):
    res = post_json(client, 'api/v1/parcels', data['basic'])
    assert json_of_response(res)['order']['status'] == 'recieved'
    response = put_json(client, 'api/v1/parcels/7/update', {"status": "delivered"})
    assert response.status_code == 200
    assert json_of_response(response)['order']['status'] == 'delivered'

#Test current location of order can be updated
def test_current_location_of_parcel_change(client):
    post_json(client, 'api/v1/parcels', data['basic'])
    response = put_json(client, 'api/v1/parcels/8/update', {'current_location': 'zambia'})
    assert response.status_code == 200
    assert json_of_response(response)['order']['current_location'] == 'zambia'

if __name__=="__main__":
    pytest.main()
    
from test_data import data
