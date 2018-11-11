from flask_api import FlaskAPI

from instance.config import app_config

from flask import request, jsonify, abort, make_response

from models import Order, User

import errors

from werkzeug.http import HTTP_STATUS_CODES
import os

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    return app

orders = [{'Id': 1, 'sender': 'kuku', 'reciever': 'papa'}]
app = create_app(config_name=os.getenv('FLASK_ENV'))

#Get all delivery orders
@app.route('/api/v1/parcels', methods=['GET'])
def get_orders():
    if request.user_type != 'admin':
        abort(403)
    elif len(orders)==0:
        abort(404)
    else:
        return jsonify({'orders': orders})

#Get a specific delivery order
@app.route('/api/v1/parcels/<parcelId>', methods=['GET'])
def get_single_order(parcelId):
    order = [order for order in orders if order['Id']==parcelId]
    if order:
        if request.userId==order.senderId or request.user_type=='admin':
            return jsonify({'order': order})
        abort(403)
    abort(404)

#Get all delivery orders created by a specific user
@app.route('/api/v1/users/<userId>/parcels', methods=['GET'])
def get_single_user_orders(userId):
    user_orders = [order for order in orders if order['senderId']==userId]
    if user_orders:
        if request.userId==userId or request.user_type=='admin':
            return jsonify({'order': user_orders})
        abort(403)
    abort(404)

#Cancel a delivery order
@app.route('/api/v1/parcels/<parcelId>/cancel', methods=['PUT'])
def cancel_order(parcelId):
    order = [order for order in orders if order['Id']==parcelId]
    if order:
        if order['status']!='delivered':
            if order['senderId']==request.userId:
                order['Id'] = ''
                order['origin'] = ''
                order['destination'] = ''
                order['reciever'] = ''
                return jsonify({'order': order})
            abort(403)
        abort(405)
    abort(404)

#Create a delivery order
@app.route('/api/v1/parcels', methods=['POST'])
def create_order():
    if not request.json or not 'origin' in request.json or not 'destination' in request.json or not 'reciever' in request.json:
        abort(400)
    order = {
        'Id': orders[-1]['Id']+1,
        'origin': request.json['origin'],
        'destination': request.json['destination'],
        'reciever': request.json['reciever'],
        'sender': request.user,
    }
    orders.append(order)
    response = jsonify({'order': order})
    response.status_code = 201

#Change destination of delivery order
@app.route('/api/v1/parcels/<parcelId>/changeDest', methods=['PUT'])
def change_destination(parcelId):
    if not request.json or not 'destination' in request.json:
        abort(400)
    order = [order for order in orders if order['Id']==parcelId]
    if order:
        if order['status']!='delivered':
            if order['senderId']==request.userId:
                order['destination'] = request.json['destination']
                return jsonify({'order': order})
            abort(403)
        abort(405)
    abort(404)

#Update location of parcel
@app.route('/api/v1/parcels/<parcelId>/updateLocation', methods=['PUT'])
def update_location(parcelId):
    if not request.json or not 'current_location' in request.json:
        abort(400)
    order = [order for order in orders if order['Id']==parcelId]
    if order:
        if order['status']!='delivered':
            if request.user_type=='admin':
                order['current_location'] = request.json['current_location']
                return jsonify({'order': order})
            abort(403)
        order['current_location'] = order['destination']
        return jsonify({'order': order})
    abort(404)

#Change status
@app.route('/api/v1/parcels/<parcelId>/updateStatus', methods=['PUT'])
def update_status(parcelId):
    if not request.json or not 'status' in request.json:
        abort(400)
    order = [order for order in orders if order['Id']==parcelId]
    if order:
        if order['status']!='delivered':
            if request.user_type=='admin':
                order['status'] = request.json['status']
                return jsonify({'order': order})
            abort(403) 
        abort(405)
    abort(404)

    
