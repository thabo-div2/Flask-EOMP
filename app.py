# Class 2 Thabo Setsubi
# Flask End of Module Project
# Point of Sale API
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
from smtplib import SMTPRecipientsRefused, SMTPAuthenticationError
import sqlite3


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


class Products(object):
    def __init__(self, product_id, name, price, desc, product_type):
        self.id = product_id
        self.name = name
        self.price = price
        self.desc = desc
        self.type = product_type


class Admin(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


class Database:
    def __init__(self):
        self.init_users_table()
        self.init_admin_table()
        self.init_products_table()

    # function that initialises the user table
    def init_users_table(self):
        conn = sqlite3.connect('shoppers.db')
        print("Opened database successfully")

        conn.execute("CREATE TABLE IF NOT EXISTS user(user_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "first_name TEXT NOT NULL,"
                     "last_name TEXT NOT NULL,"
                     "address TEXT NOT NULL,"
                     "email TEXT NOT NULL,"
                     "username TEXT NOT NULL,"
                     "password TEXT NOT NULL)")
        print("user table created successfully")
        conn.close()
        return self.init_users_table

    # Initialising the products table
    def init_products_table(self):
        with sqlite3.connect("shoppers.db") as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS product (id INTEGER PRIMARY KEY AUTOINCREMENT,"
                         "name TEXT NOT NULL,"
                         "price INTEGER NOT NULL,"
                         "description TEXT NOT NULL,"
                         "type TEXT NOT NULL,"
                         "quantity INTEGER NOT NULL,"
                         "total INTEGER NOT NULL)")
            print("products table created successfully")
        return self.init_products_table

    def init_admin_table(self):
        with sqlite3.connect("shoppers.db") as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS admin (admin_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                         "first_name TEXT NOT NULL,"
                         "last_name TEXT NOT NULL,"
                         "email TEXT NOT NULL,"
                         "username TEXT NOT NULL,"
                         "password TEXT NOT NULL)")
            print("admin table created successfully")
        return self.init_admin_table

    # function that fetches the users and puts it into a list
    def fetch_users(self):
        with sqlite3.connect('shoppers.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user")
            shoppers = cursor.fetchall()

            new_data = []

            for data in shoppers:
                print(data)
                new_data.append(User(data[0], data[5], data[6]))
        return new_data

    def fetch_products(self):
        with sqlite3.connect("shoppers.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM product")
            items = cursor.fetchall()

            new_item = []

            for data in items:
                print(data)
                new_item.append(Products(data[0], data[1], data[2], data[3], data[4]))
            return new_item

    def fetch_admin(self):
        with sqlite3.connect('shoppers.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM admin")
            users_data = cursor.fetchall()

            new_data = []

            for data in users_data:
                print(data)
                new_data.append(Admin(data[0], data[4], data[5]))

            return new_data


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# to start the flask app
app = Flask(__name__)
# to make sure that the front end can fetch the api
CORS(app)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
# this is for the flask mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'lifechoiceslotto147@gmail.com'
app.config['MAIL_PASSWORD'] = 'lifechoices2021'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


# a route that register a new user
@app.route('/user-registration/', methods=["POST"])
def user_registration():
    response = {}

    try:
        # using a POST method to create a new user
        if request.method == "POST":
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            address = request.form['address']
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']
            # connecting to the database
            with sqlite3.connect('shoppers.db') as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO user("
                               "first_name,"
                               "last_name,"
                               "address,"
                               "email,"
                               "username,"
                               "password) VALUES(?, ?, ?, ?, ?, ?)",
                               (first_name, last_name, address, email, username, password))
                conn.commit()
                # this response sent to the frontend
                response["message"] = "success"
                response["status_code"] = 201
                return response
    # error handling for the email
    except SMTPRecipientsRefused:
        response["message"] = "Invalid email used"
        response["status_code"] = 400
        return response


@app.route("/login", methods=['PATCH'])
def user_login():
    response = {}
    username = request.json["username"]
    password = request.json["password"]
    if request.method == "PATCH":
        with sqlite3.connect("shoppers.db") as conn:
            conn.row_factory = dict_factory
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user WHERE username=? AND password=?", (username, password))
            user = cursor.fetchone()

            response['user'] = user
            response['message'] = "Login successfully"
            response['status_code'] = 200
            return response
    else:
        response['error_message'] = "Wrong Method"
        response['status_code'] = 404
        return response


@app.route("/admin-registration", methods=["POST"])
def admin_registration():
    response = {}
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        # connecting to the database
        with sqlite3.connect('shoppers.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO admin("
                           "first_name,"
                           "last_name,"
                           "email,"
                           "username,"
                           "password) VALUES(?, ?, ?, ?, ?)",
                           (first_name, last_name, email, username, password))
            conn.commit()
            # this response sent to the frontend
            response["message"] = "success"
            response["status_code"] = 201
        return response


@app.route("/admin-login", methods=["PATCH"])
def admin_login():
    response = {}
    if request.method == "PATCH":
        username = request.json["username"]
        password = request.json["password"]
        conn = sqlite3.connect("shoppers.db")
        conn.row_factory = dict_factory
        c = conn.cursor()
        statement = (f"SELECT * FROM admin WHERE username='{username}' and password ="
                     f"'{password}'")
        c.execute(statement)
        if not c.fetchone():
            response['message'] = "failed"
            response["status_code"] = 400
            return response
        else:
            admin = c.fetchone()
            response['data'] = admin
            response['message'] = "welcome admin user"
            response["status_code"] = 200
            return response
    else:
        return "wrong method"


# a route to view a single users profile
@app.route('/view-profile/<int:user_id>')
def view_profile(user_id):
    response = {}

    # connecting to the database
    with sqlite3.connect("shoppers.db") as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        # Select statement to view all the details about a certain user
        cursor.execute("SELECT * FROM user WHERE user_id=" + str(user_id))

        # message to the front end
        response["status_code"] = 200
        response["description"] = "Profile retrieved successfully"
        response["data"] = cursor.fetchone()
    # putting the in a JSON format
    return jsonify(response)


# a route to add new products
@app.route('/create-products', methods=["POST"])
def create_products():
    response = {}

    try:
        # using post method to create products
        if request.method == "POST":
            # the user fill in certain details about the product
            name = request.form['name']
            price = request.form['price']
            desc = request.form['description']
            product_type = request.form['type']
            quantity = request.form['quantity']
            total = int(price) * int(quantity)

            # CONNECTING TO THE DATABASE
            with sqlite3.connect("shoppers.db") as conn:
                cursor = conn.cursor()
                # using the insert statement to create a product
                cursor.execute("INSERT INTO product("
                               "name,"
                               "price,"
                               "description,"
                               "type,"
                               "quantity,"
                               "total) VALUES (?, ?, ?, ?, ?, ?)",
                               (name, price, desc, product_type, quantity, total))
                conn.commit()
                data = (name, price, desc, product_type,quantity, total)
                # sending a message to the front end developer
                response["status_code"] = 201
                response['data'] = data
                response["description"] = "Product created successfully"
            return response
    except ConnectionError as e:
        return e
    # using this generic statement to catch all the errors
    except Exception as e:
        return e


# a route to show all the products
@app.route('/show-products')
def show_products():
    response = {}

    # connecting to the database
    with sqlite3.connect("shoppers.db") as conn:
        cursor = conn.cursor()
        # Using select statement to display the information
        cursor.execute("SELECT * FROM product")

        response["status_code"] = 200
        response["description"] = "Displaying all products successfully"
        response["data"] = cursor.fetchall()
    return jsonify(response)


@app.route('/show-users')
def show_users():
    response = {}

    with sqlite3.connect("shoppers.db") as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM user")

        response["status_code"] = 200
        response["description"] = "Displaying all users successfully"
        response["data"] = cursor.fetchall()
    return jsonify(response)


# a route to delete a specific product
@app.route('/delete-products/<int:product_id>')
def delete_products(product_id):
    response = {}

    # connecting to the database
    with sqlite3.connect("shoppers.db") as conn:
        cursor = conn.cursor()
        # using the delete statement to delete the product
        cursor.execute("DELETE FROM product WHERE id=" + str(product_id))
        conn.commit()
        # a message that gets sent to the front end
        response['status_code'] = 200
        response['message'] = "Product successfully deleted"

    return response


# a route that allows the user to edit certain details about the product
@app.route('/edit-products/<int:product_id>', methods=["PUT"])
def edit_products(product_id):
    response = {}
    # using the PUT method to update certain details of a certain product
    if request.method == "PUT":
        # connecting to a database
        with sqlite3.connect("shoppers.db") as conn:
            # making the data a dictionary
            incoming_data = dict(request.json)

            put_data = {}
            # changing the specific details
            if incoming_data.get("price") is not None:
                put_data["price"] = incoming_data.get("price")
                with sqlite3.connect("shoppers.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE product SET price=? WHERE id=?", (put_data["price"], product_id))
                    conn.commit()
                    # a message that gets sent to the front end
                    response['message'] = "Update was successful"
                    response['status_code'] = 200
                return response
            if incoming_data.get("quantity") is not None:
                put_data["quantity"] = incoming_data.get("quantity")
                with sqlite3.connect("shoppers.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE product SET quantity=? WHERE id=?", (put_data["quantity"], product_id))
                    conn.commit()
                    response['message'] = "Update was successful"
                    response['status_code'] = 200

                return response



# a route that sends an email to the user
@app.route('/send-email/<email>', methods=['GET', 'POST'])
def send_email(email):
    response = {}
    products = 'You have successfully registered an account'

    try:
        if request.method == "POST":
            with sqlite3.connect("shoppers.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM user WHERE email=?", str(email))
                receiver = cursor.fetchall()
                print(receiver)
                for data in receiver:
                    print(data)
                    msg = Message("Product received", sender="lifechoiceslotto147@gmail.com", recipients=[data[4]])
                    msg.body = products
                    mail.send(msg)
            response['status_code'] = 200
            response['message'] = "Email was sent successful"
        return response
    except SMTPRecipientsRefused:
        response["message"] = "Invalid email used"
        response["status_code"] = 400
        return response


# This statement helps run the flask app instead of using the terminal
if __name__ == '__main__':
    app.run()

