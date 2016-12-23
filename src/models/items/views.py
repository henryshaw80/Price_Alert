__author__ = 'Timur'

from flask import Blueprint

# __name__ is unique to this file when the app is running
item_blueprint = Blueprint('items', __name__)

@item_blueprint.route('/item/<string:name>')
def item_page():
    pass




