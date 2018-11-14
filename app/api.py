from flask_api import FlaskAPI
from .config import app_config
from flask import request, jsonify, abort, make_response
#from app.errors import *
from werkzeug.http import HTTP_STATUS_CODES
import os

orders = [{'Id': 1, 'sender': 'kuku', 'reciever': 'papa', 'destination': 'arua'}]

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    orders = []

    return app

app = create_app(config_name=os.getenv('FLASK_ENV'))

@app.errorhandler(400)
def Bad_request(error):
    return make_response(jsonify({'error': 'bad request'}), 400)

@app.errorhandler(404)
def Not_found(error):
    return make_response(jsonify({'error': 'resource unavailable'}), 404)

#endpoint to get all delivery orders
@app.route('/api/v1/parcels', methods=['GET'])
def get_orders():
    if len(orders)==0:
        abort(404)
    return orders

#Get a specific delivery order
@app.route('/api/v1/parcels/<int:parcelId>', methods=['GET'])
def get_single_order(parcelId):
    order = [order for order in orders if order['Id']==parcelId]
    if order:
        return jsonify({'order': order})
    abort(404)

#Get all delivery orders created by a specific user
#@app.route('/api/v1/users/<userId>/parcels', methods=['GET'])
#def get_single_user_orders(userId):
 #   user_orders = [order for order in orders if order['senderId']==userId]
  #  if user_orders:
   #     if request.userId==userId or request.user_type=='admin':
    #        return jsonify(user_orders)
     #   abort(403)
    #abort(404)

#Cancel a delivery order
@app.route('/api/v1/parcels/<parcelId>/cancel', methods=['PUT'])
def cancel_order(parcelId):
    order = [order for order in orders if order['Id'] == parcelId][0]
    if not order:
        abort(404)
    order['Id'] = ' '
    return jsonify({'result': 'order canceled'})

#Create a delivery order
@app.route('/api/v1/parcels', methods = ['POST'])
def create_order():
    if not request.json or not 'origin' in request.json or not 'destination' in request.json or not 'reciever' in request.json:
       abort(400)
    #order=Order(len(orders)+1, request.json['sender'], request.json['reciever'], request.json['origin'], request.json['destination'])
    order = {
        'Id': len(orders)+1,
        'origin': request.json['origin'],
        'destination': request.json['destination'],
        'reciever': request.json['reciever'],
        'sender': request.json['sender'],
        'weight': request.json.get('weight', 00),
        'status': request.json.get('status', 'created'),
        'service_class': request.json.get('service_class', 'standard'),
        'category': request.json.get('category', 'domestic'),
        'current_location': request.json.get('current_location', ''),
        'description': request.json.get('description', ''),
        'due_date': request.json.get('due_date', 'unknown'),
        'charge': request.json.get('charge', '0'),
    }
    orders.append(order)
    return jsonify({'order': order}), 201

#Change destination of delivery order
@app.route('/api/v1/parcels/<parcelId>/changeDestination', methods=['PUT'])
def change_destination(parcelId):
    if not request.json or not 'destination' in request.json:
        abort(400)
    order=[order for order in orders if order['Id']==parcelId][0]
    if order:
        order['destination'] = request.json.get('destination', '')
        return jsonify({'order': order})
    abort(404)

#Update location of parcel
@app.route('/api/v1/parcels/<parcelId>/updateLocation', methods=['PUT'])
def update_location(parcelId):
    if not request.json or not 'current_location' in request.json:
        abort(400)
    order = [order for order in orders if order['Id']==parcelId][0]
    if order:
        order['current_location'] = request.json.get("current_location")
        return jsonify({'order': order})
    abort(404)

#Change status
@app.route('/api/v1/parcels/<parcelId>/updateStatus', methods=['PUT'])
def update_status(parcelId):
    if not request.json or not 'status' in request.json:
        abort(400)
    order = [order for order in orders if order['Id']==parcelId][0]
    if order:
        order['status'] = request.json['status']
        return jsonify({'order': order})
    abort(404)

@app.route('/api/v1/parcels/<parcelId>/delete', methods=['DELETE'])
def delete(parcelId):
    order = [order for order in orders if order['Id']==parcelId][0]
    orders.remove(order)
    return jsonify({'result': 'success'})

    
