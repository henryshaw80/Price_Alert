__author__ = 'Timur'

import os

# API Base URL
URL = os.environ.get('MAILGUN_URL')

# API Key
API_KEY = os.environ.get('MAILGUN_API_KEY')

# Default SMTP Login
FROM = os.environ.get('MAILGUN_FROM')

COLLECTION = "alerts"

ALERT_TIMEOUT = 10