__author__ = 'Timur'

import uuid
import _datetime
from src.common.database import Database
from src.common.utils import Utils

# import exception error classes from errors.py
# old code:
# from src.models.users.errors import UserNotExistError, IncorrectPasswordError
# new code: (put all the classes into UserErrors object)
import src.models.users.errors as UserErrors


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
        This method verifies that an e-mail/password combo (as sent by the site forms) is valid.
        Checks that the e-mail exists, and that the password associated to that e-mail is correct.
        :param email: The user's email
        :param password: A sha512 hashed password
        :return: True if valid, False otherwise
        """
        user_data = Database.find_one("users",{"email":email}) #Password in pbkdf2_sha512
        if user_data is None:
            # tell user that their e-mail doesn't exist
            raise UserErrors.UserNotExistError("Your user does not exist.")
        if not Utils.check_hashed_password(password, user_data['password']):
            # tell user that their password is wrong
            raise UserErrors.IncorrectPasswordError("Your password is wrong.")

        return True