orders = {}
users = {}
data = {
    'basic': {"reciever": "kuku", "origin": "kla", "destination": "arua", "senderId": "1"},
    'json_basic': {
        'Id': 3,
        'category': '',
        'charge': '',
        'current_location': '',
        'description': '',
        'destination': 'arua',
        'due_date': '',
        'origin': 'kla',
        'reciever': 'kuku',
        'senderId': '1',
        'service_class': '',
        'status': '',
        'weight': ''
    },
    'incomplete': {"reciever": "kuku", "destination": "arua"},
    'second_user': {"reciver": "x", "origin": "y", "destination": "z", "senderId": "2"},
    'complete': {
            'orderId': 2,
            'senderId': 3,
            'reciever': 'john',
            'origin': 'origin',
            'destination': 'home',
            'weight': '10kg',
            'status': 'transit',
            'service_class': 'standard',
            'category': 'domestic',
            'current_location': 'midwy',
            'description': 'art pieces',
            'due_date': '12/12/2018',
            'charge': '$3000'
        },
    'default': {
            'orderId': 3,
            'senderId': 4,
            'reciever': 'john',
            'origin': 'origin',
            'destination': 'home',
            'weight': '00',
            'status': 'recieved',
            'service_class': 'standard',
            'category': 'domestic',
            'current_location': 'origin',
            'description': '',
            'due_date': '',
            'charge': '00'
        },
    'delivered': {
            'orderId': 2,
            'senderId': 5,
            'reciever': 'john',
            'origin': 'origin',
            'destination': 'home',
            'weight': '10kg',
            'status': 'delivered',
            'service_class': 'standard',
            'category': 'domestic',
            'current_location': 'midwy',
            'description': 'art pieces',
            'due_date': '12/12/2018',
            'charge': '$3000'
        },
    'registration': {
        'name': 'mike',
        'username': 'angmike',
        'emil': 'anguamike@yahoo.com',
        'password': 'abc123',
        'user_type': 'admin'
    }
}