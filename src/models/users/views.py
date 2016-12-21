__author__ = 'Timur'

# views will be end point of API
# we will be using Blueprint

from flask import Blueprint

# __name__ is unique to this file when the app is running
user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/login')
def login_user():
    pass

@user_blueprint.route('/register')
def register_user():
    pass

@user_blueprint.route('/alerts')
def user_alerts():
    pass

@user_blueprint.route('/logout')
def logout_user():
    pass

@user_blueprint.route('/check_alerts/<string:user_id>')
def check_user_alerts(user_id):
    pass

