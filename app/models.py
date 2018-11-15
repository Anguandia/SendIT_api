class Order(object):
    orders = {}
    def __init__(self, Id, senderId, reciever, origin, destination, weight=00, status='created', service_class='standard', category='domestic', current_location='', description='', due_date='unknown', charge=0):
        self.Id = Id
        self.senderId = senderId
        self.reciever = reciever
        self.origin = origin
        self.destination = destination
        self.weight = weight
        self.status = status
        self.service_class = service_class
        self.category = category
        self.current_location = current_location
        self.description = description
        self.due_date = due_date
        self.charge = charge
    def to_dict_order(self):
        order = {
            'Id': self.Id,
            'senderId': self.senderId,
            'reciever': self.reciever,
            'origin': self.origin,
            'destination': self.destination,
            'weight': self.weight,
            'status': self.status,
            'service_class': self.service_class,
            'category': self.category,
            'current_location': self.current_location,
            'description': self.description,
            'due_date': self.due_date,
            'charge': self.charge
        }
        return order
    def get_order(self):
        print('sender: {}, reciever: {}, ID: {}, destination: {}, origin: {}, charge: {}'.format(self.senderId, self.reciever, self.Id, self.destination, self.origin, self.charge))

class User:
    users = []
    def __init__(self, userId, name, email, password, user_type='user'):
        self.userId = userId
        self.name = name
        self.email = email
        self.password = password
        self.user_type = user_type

    def __str__(self):
        user = {
            'userId': self.userId,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'user_type': self.user_type
        }
        return user

    def get_user(self):
        print('user: {}, email: {}, user_type: {}'.format(self.name, self.email, self.user_type))
