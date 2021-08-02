# Class 2 Thabo Setsubi
# Flask End of Module Project
# Point of Sale API
from flask import Flask, request, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from flask_cors import CORS
import hmac
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


def init_users_table():
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


def fetch_users():
    with sqlite3.connect('shoppers.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user")
        shoppers = cursor.fetchall()

        new_data = []

        for data in shoppers:
            print(data)
            new_data.append(User(data[0], data[5], data[6]))
    return new_data


def init_products_table():
    with sqlite3.connect("shoppers.db") as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT,"
                     "name TEXT NOT NULL,"
                     "price INTEGER NOT NULL,"
                     "description TEXT NOT NULL,"
                     "type TEXT NOT NULL)")
        print("products table created successfully")


def fetch_products():
    with sqlite3.connect("shoppers.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        items = cursor.fetchall()

        new_item = []

        for data in items:
            print(data)
            new_item.append(Products(data[0], data[1], data[2], data[3], data[4]))
        return new_item


init_users_table()
init_products_table()
users = fetch_users()
products = fetch_products()

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

product_table = {p.name: p for p in products}
productid_table = {p.id: p for p in products}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and hmac.compare_digest(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)


app = Flask(__name__)
CORS(app)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)


@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity


@app.route('/user-registration/', methods=["POST"])
def user_registration():
    response = {}

    if request.method == "POST":

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

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
            response["message"] = "success"
            response["status_code"] = 201
        return response


@app.route('/view-profile/<int:user_id>')
def view_profile(user_id):
    response = {}

    with sqlite3.connect("shoppers.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE user_id=" + str(user_id))

        response["status_code"] = 200
        response["description"] = "Profile retrieved successfully"
        response["data"] = cursor.fetchone()

    return jsonify(response)


@app.route('/create-products', methods=["POST"])
def create_products():
    response = {}

    if request.method == "POST":
        name = request.form['name']
        price = request.form['price']
        desc = request.form['description']
        product_type = request.form['type']

        with sqlite3.connect("shoppers.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products("
                           "name,"
                           "price,"
                           "description,"
                           "type) VALUES (?, ?, ?, ?)",
                           (name, price, desc, product_type))
            conn.commit()
            response["status_code"] = 201
            response["description"] = "Product created successfully"
        return response


@app.route('/show-products')
def show_products():
    response = {}

    with sqlite3.connect("shoppers.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")

        response["status_code"] = 200
        response["description"] = "Displaying all products successfully"
        response["data"] = cursor.fetchall()
    return jsonify(response)


@app.route('/delete-products/<int:product_id>')
def delete_products(product_id):
    response = {}
    with sqlite3.connect("shoppers.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id=" + str(product_id))
        conn.commit()
        response['status_code'] = 200
        response['message'] = "Product successfully deleted"

    return response


if __name__ == '__main__':
    app.run()

