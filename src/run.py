__author__ = 'Timur'

from src.app import app

app.run(debug=app.config['DEBUG'], port=4990)

