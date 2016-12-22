__author__ = 'Timur'

# views will be end point of API
# we will be using Blueprint

from flask import Blueprint, request, url_for, render_template, session, redirect
from src.models.users.user import User
import src.models.users.errors as UserErrors

# __name__ is unique to this file when the app is running
user_blueprint = Blueprint('users', __name__)

# 'GET' method request data from server, give them 'login form'
# 'POST' method sending data to database or check whether login is valid
@user_blueprint.route('/login', methods=['GET','POST'])
def login_user():
    if request.method == 'POST':
        # check login is valid
        email = request.form['email']
        password = request.form['hashed']

        try:
            if User.is_login_valid(email, password):
                # put email into session (temporary storage of data)
                # when a browser arrives at our webpage, we give them
                # a unique identifier. the browser will use this identifier
                # with every request to let the webpage know that the browser
                # is related to this email.
                session['email'] = email

                return redirect(url_for(".user_alerts"))
                # url_for is getting the url for a specific method
                # redirect is '301', a HTTP status code that tells the browser
                # to change to other location (i.e. address).

        # old code: catch a unique exception then return message
        # except UserErrors.UserNotExistError as e: Catch user does not exist error
        #    return e.message
        # except UserErrors.IncorrectPasswordError as e: Catch incorrect pswd error
        #    return e.message
        # new code: remove duplication
        # we only use UserError class that captures all exceptions
        except UserErrors.UserError as e:
            return e.message

    # if request method is not 'POST', go to login page
    # if request method is 'POST AND login is invalid, go to login page again
    return render_template("users/login.html")

    # area of improvement: send the user an error if their login was invalid

@user_blueprint.route('/register')
def register_user():
    pass

@user_blueprint.route('/alerts')
def user_alerts():
    return "This is the alerts page."

@user_blueprint.route('/logout')
def logout_user():
    pass

@user_blueprint.route('/check_alerts/<string:user_id>')
def check_user_alerts(user_id):
    pass

