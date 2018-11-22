from flask_api import FlaskAPI
import os
from flask import request, jsonify, abort, make_response
from instance.config import app_config
from .models import Order


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    from app.users import user_bp
    app.register_blueprint(user_bp, url_prefix='/api/v1')
    return app


app = create_app(config_name=os.getenv('FLASK_ENV'))


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'resource unavailable'}), 404)


# endpoint to get all delivery orders


@app.route('/api/v1/parcels', methods=['GET'])
def get_orders():
    orders = Order.get_orders
    if orders:
        return jsonify({'orders': orders})
    abort(404)

# Get a specific delivery order


@app.route('/api/v1/parcels/<int:parcelid>', methods=['GET'])
def get_single_order(parcelid):
    order = Order.get_order(parcelid)
    if order:
        return jsonify({'order': order})
    abort(404)

# Get all delivery orders created by a specific user


@app.route('/api/v1/<userid>/parcels', methods=['GET'])
def get_single_user_orders(userid):
    user_orders = Order.get_user_orders(userid)
    if user_orders:
        return jsonify({'orders': user_orders})
    abort(404)

# Cancel a delivery order


@app.route('/api/v1/parcels/<parcelid>/cancel', methods=['PUT'])
def cancel_order(parcelid):
    if request.json:
        order = Order.get_order(parcelid)
        if order:
            if order['status'] == 'delivered':
                return jsonify({'result': 'parcel already deliverd!'})
            else:
                Order.update_order(parcelid, (
                    order.destination, 'canceled', order.current_location))
                return jsonify({'operation': 'canceled'})
        abort(404)
    abort(400)

# Create a delivery order


@app.route('/api/v1/parcels', methods=['POST'])
def create_order():
    if not request.json or 'origin' not in request.json or 'destination' \
            not in request.json or 'reciever' not in request.json:
        abort(400)
    # order = {
    #    'Id': len(orders)+1,
    #    'origin': request.json['origin'],
    #    'destination': request.json['destination'],
    #    'reciever': request.json['reciever'],
    #    'senderId': request.json['senderId'],
    #    'weight': request.json.get('weight', '00'),
    #    'status': request.json.get('status', 'recieved'),
    #    'service_class': request.json.get('service_class', 'standard'),
    #    'category': request.json.get('category', 'domestic'),
    #    'current_location': request.json.get('current_location', 'source'),
    #    'description': request.json.get('description', 'none'),
    #    'due_date': request.json.get('due_date', 'unknown'),
    #    'charge': request.json.get('charge', '00'),
    # }
    # orders[str(order['Id'])] = order
    # dict_orders = [
    # orders[key].to_dict_order() for key in orders.keys()]
    count = Order.get_count()
    order = Order(
        count,
        request.json['userid'],
        request.json['recievr'],
        request.json['origin'],
        request.json['detination'],
        request.json.get('weight', '00'),
        request.json.get('status', 'recieved'),
        request.json.get('service_class', 'standard'),
        request.json.get('category', 'domestic'),
        request.json.get('current_location', 'source'),
        request.json.get('description', 'none'),
        request.json.get('due_date', 'unknown'),
        request.json.get('charge', '00'),
         )
    return jsonify({'order': order}), 201

# Change destination of delivery order


@app.route('/api/v1/parcels/<parcelid>/changeDestination', methods=['PUT'])
def change_destination(parcelid):
    if not request.json or 'destination' not in request.json:
        abort(400)
    order = Order.get_order(parcelid)
    if order:
        Order.update_order(parcelid, (
            request.json['destination'], order['status'], order[
                'current_location']))
        return jsonify({'order': 'destination changed'})
    abort(404)

# Update location and atatus of parcel


@app.route('/api/v1/parcels/<parcelid>/update', methods=['PUT'])
def update_location(parcelid):
    if request.json and 'current_location' or 'status' in request.json:
        order = Order.get_order(parcelid)
        if order:
            Order.update_order(parcelid, (
                order['destination'],
                request.json.get('status', order['status']),
                request.json.get('current_location', order[
                    'current_location'])))
            return jsonify({'order': 'updated'})
        abort(404)
    abort(400)


# delete order
# @app.route('/api/v1/parcels/<parcelid>/delete', methods=['DELETE'])
# def delete(parcelid):
#     if request.json:
#         order = orders[parcelid]
#         if order:
#             del orders[parcelid]
#             return jsonify({'operation': 'deleted'})
#         abort(404)
#     abort(400)


if __name__ == "__main__":
    app.run
