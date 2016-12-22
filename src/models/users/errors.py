__author__ = 'Timur'

class UserNotExistError(Exception):
    # This call will contain exceptions in server-side
    # server-side can raise an exception, which will be pass on
    # to client-side, which will see the exception message
    # (e.g. user does not exist message)
    def __init__(self, message):
        self.message = message

class IncorrectPasswordError(Exception):
    def __init__(self, message):
        self.message = message