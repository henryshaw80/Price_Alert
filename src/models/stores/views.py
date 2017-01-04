__author__ = 'Timur'

from flask import Blueprint

# __name__ is unique to this file when the app is running
store_blueprint = Blueprint('stores', __name__)

@store_blueprint.route('/')
def index():
    return "This is the stores index"

@store_blueprint.route('/store/<string:name>')
def store_page():
    pass

