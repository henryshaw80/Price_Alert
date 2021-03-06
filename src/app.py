__author__ = 'Timur'
# app.py stores the app but it runs from run.py

from flask import Flask, render_template
from src.common.database import Database

app = Flask(__name__)

# import config to be loaded to app
app.config.from_object('src.config')

# allow session to be secured; when a browser comes into an application
# and request of a webpage; Flask will put a cookie with a session id
# to link that browser to a specific session in our server.
# and that session in our server that contains session's email
# in order to secure those cookies, we need a secret key
app.secret_key = "123" #usually 32 random characters and numbers


# Initialize database
@app.before_first_request
def init_db():
    Database.initialize()

@app.route('/') #when we access URL with '/'
def home():
    return render_template('home.jinja2')

# import blueprints
from src.models.users.views import user_blueprint
from src.models.alerts.views import alert_blueprint
from src.models.stores.views import store_blueprint
# register the blueprints
app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(alert_blueprint, url_prefix="/alerts")
app.register_blueprint(store_blueprint, url_prefix="/stores")

