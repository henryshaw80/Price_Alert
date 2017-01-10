__author__ = 'Timur'

from functools import wraps
from flask import session, url_for, redirect, request

def requires_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        return func(*args, **kwargs)
    return decorated_function






# my_function method gets passed to requires_login decorator
# that function is then being wrap in another function, decorated_function
# decorated_function can do something. and return the function that is being wrapped
# then the decorator is returning the function definition (notice no brackets)
# this decorated_function is substituting the content of my function.
# when we call my_function, we are actually calling decorated_function
# then content of my_function is being replaced by the content of decorated_function

def requires_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        print("Hi")
        return func(*args, **kwargs)
    return decorated_function

@requires_login
def my_function(x, y):
    return x + y

print(my_function(5, 6))
