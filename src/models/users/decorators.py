__author__ = 'Timur'

from functools import wraps
from flask import session, url_for, redirect, request

# An existing function, FUNC, gets passed to requires_login decorator
# Using wrap decorator, FUNC is then being wrap again in another function, decorated_function
# This function is returning the function definition (notice no brackets)
# to substitute the whole content of FUNC with content of decorated_function.
# When we call FUNC, we are actually calling decorated_function which content
# has replaced by the content of FUNC.

def requires_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        return func(*args, **kwargs)
    return decorated_function
