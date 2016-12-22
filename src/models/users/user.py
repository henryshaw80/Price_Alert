__author__ = 'Timur'

import uuid
import _datetime
from src.common.database import Database

class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def is_login_valid(email, password):
        """
        This method verifies that an e-mail/password combo
        (as sent by the site form) is valid.
        Checks that e-mail exists, and that the password
        associated to that e-mail is correct.
        :param email: the user's email
        :param password: a sha512 hashed password
        :return: True if valid, False otherwise
        """
        # pull user's information from database
        user_data = Database.find_one("users", {"email":email})

        if user_data is None:
            # tell user that their e-mail doesn't exist
            pass

        if not Utils.check_hashed_password(password, user_data['password']):
            # tell user that their password is wrong
            pass

        # when email and password are valid
        return True

