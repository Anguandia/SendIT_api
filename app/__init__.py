from flask_api import FlaskAPI
import os
from flask import request, jsonify, abort, make_response
from werkzeug.http import HTTP_STATUS_CODES
from instance.config import app_config
from .models import Order, User

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    return app

app = create_app(config_name=os.getenv('FLASK_ENV'))
@app.errorhandler(400)
def Bad_request(error):
    return make_response(jsonify({'error': 'bad request'}), 400)

@app.errorhandler(404)
def Not_found(error):
    return make_response(jsonify({'error': 'resource unavailable'}), 404)
orders = {}
#endpoint to get all delivery orders
@app.route('/api/v1/parcels', methods=['GET'])
def get_orders():
    if orders:
        dict_orders = [orders[key].to_dict_order() for key in orders.keys()]
        return jsonify({'orders': dict_orders})
    abort(404)

#Get a specific delivery order
@app.route('/api/v1/parcels/<int:parcelId>', methods=['GET'])
def get_single_order(parcelId):
    order = orders[str(parcelId)]
    if order:
        return jsonify({'order': order.to_dict_order()})
    abort(404)

#Get all delivery orders created by a specific user
@app.route('/api/v1/<userId>/parcels', methods=['GET'])
def get_single_user_orders(userId):
    user_orders = {}
    keys = [key for key in orders.keys() if key==str(userId)]
    if keys:
        for key in keys:
            user_orders[key]=orders[key]
            dict_user_orders=[user_orders[k].to_dict_order() for k in user_orders.keys()]
            return jsonify({'orders': dict_user_orders})
    abort(404)

#Cancel a delivery order
@app.route('/api/v1/parcels/<parcelId>/cancel', methods=['PUT'])
def cancel_order(parcelId):
    if request.json:
        order = orders[parcelId]
        if order:
            order.status = "canceled"
            return jsonify({'order': order.to_dict_order()})
        abort(404)
    abort(400)

#Create a delivery order
@app.route('/api/v1/parcels', methods = ['POST'])
def create_order():
    if not request.json or not 'origin' in request.json or not 'destination' in request.json or not 'reciever' in request.json:
       abort(400)
    order=Order(
        len(orders)+1, 
        request.json['senderId'], 
        request.json['reciever'], 
        request.json['origin'], 
        request.json['destination'],
        request.json.get('weight', '00'), 
        request.json.get('status', "recieved"), 
        request.json.get('service_class', 'standard'), 
        request.json.get('category', 'domestic'), 
        request.json.get('current_location', 'source'), 
        request.json.get('description', 'none'), 
        request.json.get('due_date', 'unknown'), 
        request.json.get('charge', '00')
    ) 
    #order = {
    #    'Id': len(orders)+1,
    #    'origin': request.json['origin'],
    #    'destination': request.json['destination'],
    #    'reciever': request.json['reciever'],
    #    'sender': request.json['sender'],
    #    'weight': request.json.get('weight', 00),
    #    'status': request.json.get('status', 'created'),
    #    'service_class': request.json.get('service_class', 'standard'),
    #    'category': request.json.get('category', 'domestic'),
    #    'current_location': request.json.get('current_location', ''),
    #    'description': request.json.get('description', ''),
    #    'due_date': request.json.get('due_date', 'unknown'),
    #    'charge': request.json.get('charge', '0'),
    #}
    orders[str(order.Id)] = order
    dict_orders = [orders[key].to_dict_order() for key in orders.keys()]
    return jsonify({'order': dict_orders}), 201

#Change destination of delivery order
@app.route('/api/v1/parcels/<parcelId>/changeDestination', methods=['PUT'])
def change_destination(parcelId):
    if not request.json or not 'destination' in request.json:
        abort(400)
    order=orders[parcelId]
    if order:
        order.destination = request.json['destination']
        return jsonify({'order': order.to_dict_order()})
    abort(404)

#Update location and atatus of parcel
@app.route('/api/v1/parcels/<parcelId>/update', methods=['PUT'])
def update_location(parcelId):
    if request.json and 'current_location' or 'status' in request.json:
        order = orders[parcelId]
        if order:
            for key in ['current_location', 'status']:
                order.to_dict_order()[key] = request.json.get(key, order.to_dict_order()[key])
                return jsonify({'order': order.to_dict_order()})
        abort(404)
    abort(400)

#delete order
@app.route('/api/v1/parcels/<parcelId>/delete', methods=['DELETE'])
def delete(parcelId):
    if request.json:
        order = orders[parcelId]
        if order:
            del orders[parcelId]
            return jsonify({'operation': 'deleted'})
        abort(404)
    abort(400)

    
if __name__=="__main__":
    app.run