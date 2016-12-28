__author__ = 'Timur'

class StoreError(Exception):
    # This call will contain exceptions in server-side
    # server-side can raise an exception, which will be pass on
    # to client-side, which will see the exception message
    def __init__(self, message):
        self.message = message

class StoreNotFoundException(StoreError):
    # The init has been specified in StoreError class that inherit StoreError construct
    pass