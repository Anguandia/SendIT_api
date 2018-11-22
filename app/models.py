import psycopg2
import datetime

class Data:
    connection=psycopg2.connect(
        "dbname=kuku user=postgres password=kukuer1210 host=localhost port=5432"
        )
    cursor=connection.cursor()

    #def to_turple(self):
    #    for property in self.properties:
    #        turp=(str(self.property),)
    #        return turp

class User(Data):
    def create_table(self):
        create_user_table_query= '''CREATE TABLE IF NOT EXISTS users(
            userId serial PRIMARY KEY NOT NULL, name varchar, email varchar, password_hash varchar, user_type=varchar
            )'''
        self.cursor.execute(create_user_table_query)
        self.connection.commit()
    def __init__(self, userId, name, email, password_hash, user_type):
        self.userId = userId
        self.name = name 
        self.email = email
        self.password_hash = password_hash
        self.user_type = user_type
        #self.create_user()

    #def create_user(self):
        try:
            create_user_query = """ INSERT INTO users (userId, name, email, password_hash, user_type) VALUES (%s,%s,%s,%s,%s)"""
            self.cursor.execute(create_user_query, (str(self.userId), str(self.name), str(self.email),str(self.password_hash), str(self.user_type)))
            self.connection.commit()
            print ("user", self.to_dict(), "created")
        except (Exception, psycopg2.Error) as error :
            if(self.connection):
                print("Failed to create user:", error)
        #finally:
        #    if(self.connection):
        #        self.cursor.close()
        #        self.connection.close()
        #        print("done")
    
    def get_users(self):
        self.cursor.execute("SELECT * FROM users")
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
    
    def fetch_user(self, userId):
        self.cursor.execute("SELECT * FROM users where parcelId = %s")
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
    
    def edit_user(self, name, userId):
        try:
            sql_update_query = """Update users set name = %s where parcelId = %s"""
            self.cursor.execute(sql_update_query, (name, userId))
            self.connection.commit()
            print("name changed to ", name)
        except (Exception, psycopg2.Error) as error:
            print("Error in update operation", error)
        #finally:
        #    if (self.connection):
        #        self.cursor.close()
        #        self.connection.close()
        #        print("done")
    
    def delete_user(self, userId):
        try:
            sql_delete_query='''delete from users where parcelId=%s'''
            self.cursor.execute(sql_delete_query, (userId))
            self.connection.commit()
            print("deleted")
        except (Exception, psycopg2.Error) as error:
            print("Error in update operation", error)
        finally:
            if (self.connection):
                self.cursor.close()
                self.connection.close()
                print("done")
    def to_dict(self):
        user = {
            'userId': self.userId,
            'name': self.name,
            'email': self.email,
            'password_hash': self.password_hash,
            'user_type': self.user_type
        }
        return user

    def get_user(self):
        print('user: {}, email: {}, user_type: {}'.format(self.name, self.email, self.user_type))

    #def __str__(self):
    #    for field in (self.parcelId, self.name, self.email, self.password, self.user_type):
    #        field = str(self.field)
    #        return (field,)

class Order(Data):
    def __init__(self, parcelId, userId, reciever, origin, destination, weight=00, status='recieved', service_class='standard', category='domestic', current_location='unknown', description='none', due_date=datetime.datetime.now(), charge=00):
        self.parcelId = parcelId
        self.userId = userId
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

        create_order_table_query = '''CREATE TABLE IF NOT EXISTS orders(
            parcelId serial PRIMARY KEY NOT NULL, userId  INT NOT NULL, reciever varchar, origin varchar, destination varchar, weight INT, status varchar, service_class varchar, category varchar, current_location varchar, description varchar, due_date date, charge INT 
            )'''
        self.cursor.execute(create_order_table_query)
        self.connection.commit()

        try:
            create_order_query = """ INSERT INTO orders (userId, reciever, origin, destination, weight, status, service_class, category, current_location, description, due_date, charge ) VALUES (%s,%s,%s, %s,%s, %s, %s,%s,%s,%s,%s,%s)"""
            self.cursor.execute(
                create_order_query, (str(self.userId), str(self.reciever), str(self.origin), str(self.destination), str(self.weight), str(self.status), str(self.service_class), str(self.category), str(self.current_location), str(self.description), str(self.due_date), self.charge))
            self.connection.commit()
            print ("created")
        except (Exception, psycopg2.Error) as error :
            if(self.connection):
                print("Failed to create order", error)
        finally:
            if(self.connection):
                self.cursor.close()
                self.connection.close()
                print("done")

        #def to_turple(self):
        #    for property in self
    def to_dict_order(self):
        order = {
            'Id': self.parcelId,
            'senderId': self.userId,
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

    def show_order(self):
        print('sender: {}, reciever: {}, ID: {}, destination: {}, origin: {}, charge: {}'.format(self.userId, self.reciever, self.parcelId, self.destination, self.origin, self.charge))
    
    def update_order(self, parcelId, input):
        try:
            sql_update_query = """Update orders set(destination, status, current_location ) VALUES (%s,%s,%s) where parcelId = %s"""
            self.cursor.execute(sql_update_query, (input, parcelId))
            self.connection.commit()
            print("success")
        except (Exception, psycopg2.Error) as error:
            print("Error in update operation", error)
        finally:
            if (self.connection):
                self.cursor.close()
                self.connection.close()
                print("done")
    
    def delete_order(self, parcelId):
        try:
            sql_delete_query='''delete from orders where parcelId=%s'''
            self.cursor.execute(sql_delete_query, (parcelId))
            self.connection.commit()
            print("deleted")
        except (Exception, psycopg2.Error) as error:
            print("Error in update operation", error)
        finally:
            if (self.connection):
                self.cursor.close()
                self.connection.close()
                print("done")
    
    
    def get_orders(self):
        self.cursor.execute("SELECT * FROM orders")
        self.connection.commit()
        orders=self.cursor.fetchall()
        count=self.cursor.rowcount
        print(count, orders, "orders fetched")
        self.cursor.close()
        self.connection.close()
        dict_orders_list = [order.to_dict() for order in orders]
        return dict_orders_list
    
    def get_user_orders(self, userId):
        self.cursor.execute("SELECT * FROM orders where userID=%s")
        print()
        self.connection.commit()
        orders = self.cursor.fetchall()
        user_orders_list = [order.to_dict() for order in orders]
        count=self.cursor.rowcount
        print(count, "orders fetched")
        self.cursor.close()
        self.connection.close()
        return user_orders_list
    
    def get_order(self, parcelId):
        self.cursor.execute("SELECT * FROM orders where parcelId=%s")
        order=self.cursor.fetchone()
        self.connection.commit()
        print("order fetched")
        self.cursor.close()
        self.connection.close()
        return order.to_dict()

    def get_count(self):
        count = self.cursor.rowcount
        return count
    

#self.connection.commit()
#self.cursor.close()
#self.connection.close()

#user = (7, 'kuere', 'ang@e.c', 'none', 'user')
#create_user(user)
#
#parcelId = 2
#name = 'anguandia mike'
#edit_user(name, parcelId)

