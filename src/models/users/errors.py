__author__ = 'Timur'

class UserError(Exception):
    # This call will contain exceptions in server-side
    # server-side can raise an exception, which will be pass on
    # to client-side, which will see the exception message
    # (e.g. user does not exist message)
    def __init__(self, message):
        self.message = message

class UserNotExistError(UserError):
    # The init has been specified in UserError class that captures all exception
    pass

class IncorrectPasswordError(UserError):
    # The init has been specified in UserError class that captures all exception
    pass