orders = {}
users = {}
data = {
    'basic': {"reciever": "kuku", "origin": "kla", "destination": "arua", "senderId": "1"},
    'jsn_basic': {
        'Id': 1,
        'category': 'domestic',
        'charge': '00',
        'current_location': 'source',
        'description': 'none',
        'destination': 'arua',
        'due_date': 'unknown',
        'origin': 'kla',
        'reciever': 'kuku',
        'senderId': '1',
        'service_class': 'standard',
        'status': 'recieved',
        'weight': '00'
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
            'orderId': 1,
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