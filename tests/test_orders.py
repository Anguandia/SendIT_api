import pytest
import json
from flask_api import FlaskAPI
from api import app
from test_data import order_data, orders


orders = [{'Id': 1, 'sender': 'kuku', 'reciever': 'papa', 'destination': 'arua'}]
@pytest.fixture(scope='module')
def client():
    test_client=app.test_client()
    cxt = app.app_context()
    cxt.push()
    yield test_client
    cxt.pop()

#Encode test requests to json
def post_json(client, url, json_dict):
    """Send dictionary json_dict as a json to the specified url """
    return client.post(url, order_data=json.dumps(json_dict), content_type='application/json')
#Decode json requests
def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.order_data.decode('utf8'))
#Encoding for put request
def put_json(client, url, json_dict):
    """Send dictionary json_dict as a json to the specified url """
    return client.put(url, order_data=json.dumps(json_dict), content_type='application/json')

#Test order creation and expected reponse code and content
def test_order_creation(client):
    response = post_json(client, 'api/v1/parcels', order_data['basic'])
    assert response.status_code == 201
    assert json_of_response(response) == {'order': {'reciever': 'kuku', 'origin': 'kla', 'destination': 'arua','Id': 2}}

#Test order with missing mandatory field not created, correct error message in response
def test_incomplete_order_not_created(client):
    response = post_json(client, 'api/v1/parcels', order_data['incomplete'])
    assert response.status_code == 400
    assert json_of_response(response) == {'error': 'bad request'}

#Test order created with missing optional components filled by defaults
def test_creation_optional_fields_defaults(client):
    response = post_json(client, 'api/v1/parcels', order_data['basic'])
    assert response.status_code == 201
    assert hasattr("sender", json_of_response(response))

#Test api can retrieve all orders; correct response code and body
def test_fetch_all_orders(client):
    post_json(client, 'api/v1/parcels', order_data['basic'])
    post_json(client, 'api/v1/parcels', order_data['complete'])
    response = client.get('api/v1/parcels')
    assert response.status_code == 200
    assert json_of_response(response) == {'order': orders}

#Test non admin user cannot retrive all orders, correct response: code and message
'''needs user auth first'''

#Test correct response when no orders to fetch
def test_fetch_empty(client):
    response = client.get('api/v1/parcels')
    assert response.status_code == 404
    assert json_of_response(response) == {'result': 'no orders'}

#Test api can fetch specific order; correct response: __ code and body
def test_fetch_single(client):
    post_json(client, 'api/v1/parcels', order_data['basic'])
    post_json(client, 'api/v1/parcels', order_data['complete'])
    response = client.get('api/v1/parcels/1')
    assert response.status_code == 200
    assert json_of_response(response) == {'result': str(orders[0])}

#Test only owner and admin can fetch specific order
'''needs user auth'''

#Test correct response if specified order missing
def test_fetch_missing_order(client):
    post_json(client, 'api/v1/parcels', order_data['basic'])
    response = client.get('api/v1/parcels/2')
    assert response.status_code == 404
    assert json_of_response(response) == {'result': 'order non existent'}

#Test correct response for denial of specific order fetch request
'''needs user auth'''

#Test order before delivery can be cancelled
def test_cancel_order(client):
    res = post_json(client, 'api/v1/parcels', order_data['basic'])
    assert res.status_code == 201
    response = client.put_json('api/v1/parcels/2/cancel')
    assert response.status_code == 200
    assert json_of_response(response) == {'result': 'canceled'}

#Test order after delivery can not be canceled, correct response; message and code
def test_cancel_order_delivered_fails(client):
    res = post_json(client, 'api/v1/parcels', order_data['basic'])
    assert res.status_code == 201
    client.put('api/v1/parcels/2/changeState', order_data['delivered'])
    response = client.put('api/v1/parcels/2/cancel')
    assert response.status_code == 403
    assert response.body == 'forbidden'
    assert json_of_response(response) == {'result': 'parcel already delivered'}

#Test only owner can cancel order
'''needs user auth'''

#Test correct result if order specified not available
def test_specified_order_non_existent_correct_response(client):
    response1 = client.put('api/v1/parcels/2/cancel')
    assert response1.status_code == 404
    response2 = client.put('api/v1/parcels/2/changeStatus', order_data['delivered'])
    assert response2.status_code == 404
    response3 = client.put('api/v1/parcels/2/changeDest', order_data['dest'])
    assert response3.status_code == 404
    response4 = client.get('api/v1/parcels/2')
    assert response4.status_code == 404

#Test only owner can change destination if not yet delivered(2-part)
'''needs auth'''

#Test only admin can change order status when not yet delivered
'''needs auth'''

#Test Only admin can update current location of order
'''needs auth'''

if __name__=="__main__":
    pytest.main()    

