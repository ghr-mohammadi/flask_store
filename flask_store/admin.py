import json
from flask import Blueprint
from flask import request
from flask import render_template
from flask import current_app
from flask import url_for
from flask import redirect
from flask import session
from flask import abort
from cryptography.fernet import Fernet
from . import db
from .functions import get_categoies_list

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        with open('flask_store/static/json_folder/users.json') as user_file:
            users = json.load(user_file)
            cipher_suite = Fernet(current_app.config['CIPHER_KEY'])
            for user in users:
                unciphered_pass = (cipher_suite.decrypt(bytes(user[1], 'utf-8'))).decode("utf-8")
                if username == user[0] and password == unciphered_pass:
                    session['username'] = username
                    return redirect(url_for("admin.management"), code=307)
            return render_template("admin_panel/login.html", error="incorect username or password")
    else:
        return render_template("admin_panel/login.html", error=None)


@bp.route("/management", methods=["POST", "GET"])
def management():
    if request.method == "POST":
        return render_template("admin_panel/base_admin.html")
    else:
        abort(404)


@bp.route("/get-order", methods=["POST", "GET"])
def get_orders():
    if request.method == "POST":
        orders = {"column_names": ["_id", "user_name", "total_price", "order_time"],
                  'data': db.get_orders()}
        return orders
    else:
        abort(404)


@bp.route("/get-order-detail", methods=["POST", "GET"])
def get_order_details():
    if request.method == "POST":
        data = request.get_json()
        detail = db.get_order_details(data['order_id'])
        return detail
    else:
        abort(404)


@bp.route("/set-inventory", methods=["POST", "GET"])
def set_inventories():
    if request.method == "POST":
        data = request.get_json()
        if 'add_inventory' in data:
            db.add_inventory(data)
            return 'add_repository'
        elif 'edit_inventory' in data:
            db.edit_inventory(data)
            return 'edit_inventory'
        elif 'delete_inventory' in data:
            db.delete_inventory(data)
            return 'delete_inventory'
        else:
            return 'invalid request'
    else:
        abort(404)


@bp.route("/get-inventory", methods=["POST", "GET"])
def get_inventories():
    if request.method == "POST":
        inventories = {"column_names": ["_id", "repository_name", "commodity_name", "price", "quantity"],
                       'data': db.get_inventories()
                       }
        return inventories
    else:
        abort(404)


@bp.route("/set-repository", methods=["POST", "GET"])
def set_repositories():
    if request.method == "POST":
        data = request.get_json()
        if 'add_repository' in data:
            db.add_repositories(data)
            return 'add_repository'
        elif 'edit_repository' in data:
            db.edit_repository(data)
            return 'edit_repository'
        elif 'delete_repository' in data:
            db.delete_repositories(data)
            return 'delete_repository'
        else:
            return 'invalid request'
    else:
        abort(404)


@bp.route("/get-repository", methods=["POST", "GET"])
def get_repositories():
    if request.method == "POST":
        repositories = db.get_repositories()
        repositories = {"column_names": ["_id", "repository_name"],
                        'data': repositories}
        return repositories
    else:
        abort(404)


@bp.route("/get-category", methods=["POST", "GET"])
def get_categories():
    if request.method == "POST":

        with open('flask_store/static/json_folder/categories.json', encoding='utf-8') as categories_json:
            categories_json = json.load(categories_json)

        categories = {
            'data': get_categoies_list(categories_json)
        }
        return categories
    else:
        abort(404)


@bp.route("/set-product", methods=["POST", "GET"])
def set_products():
    if request.method == "POST":
        file = request.files.get('products_file')
        if file:
            db.add_products(file.read())
            return 'add_products'
        else:
            data = request.get_json()
            if 'delete_product' in data:
                db.delete_product(data)
                return 'delete_product'
            elif 'edit_product' in data:
                db.edit_product(data)
                return 'edit_product'
            elif 'add_product' in data:
                db.add_product(data)
                return 'add_product'
            else:
                return 'invalid request'
    else:
        abort(404)


@bp.route("/get-products", methods=["POST", "GET"])
def get_products():
    if request.method == "POST":
        products = db.get_products()
        products = {
            "column_names": ["_id", "image_link", "commodity_name", "category", "description"],
            "data": products
        }
        return products
    else:
        abort(404)
