__author__ = 'Timur'

import uuid
import _datetime
from src.common.database import Database
from src.common.utils import Utils
from src.models.alerts.alert import Alert
import src.models.users.constants as UserConstants

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
        user_data = Database.find_one(UserConstants.COLLECTION, {"email":email}) #Password in pbkdf2_sha512
        if user_data is None:
            # tell user that their e-mail doesn't exist
            raise UserErrors.UserNotExistError("Your user does not exist.")
        if not Utils.check_hashed_password(password, user_data['password']):
            # tell user that their password is wrong
            raise UserErrors.IncorrectPasswordError("Your password is wrong.")

        return True

    @staticmethod
    def register_user(email, password):
        """
        This method regsters a user using email and password
        Password already comes hashed as sha-512
        :param email: user's e-mail (might be invalid)
        :param password: sha512-hashed password
        :return: True is registered successfully, or False otherwise
                (exceptions can also be raised) """
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})

        # if user is already registered
        if user_data is not None:
            # tell user they are already registered
            raise UserErrors.UserAlreadyRegisteredError("The e-mail you used to register already exist.")
        # if e-mail is invalid
        if not Utils.email_is_valid(email):
            # tell user that their e-mail is not constructed properly
            raise UserErrors.InvalidEmailError("The e-mail does not have the right format.")

        # set email and encrypted password to User attributes
        # then save to database
        User(email, Utils.hash_password(password)).save_to_db()

        return True

    def save_to_db(self):
        Database.insert(UserConstants.COLLECTION, self.json())

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    def delete_user(self):
        Database.remove(UserConstants.COLLECTION, {'_id':self._id})

    @classmethod
    def find_by_email(cls, email):
        return cls(**Database.find_one('users', {'email': email}))

    def get_alerts(self):
        return Alert.find_by_user_email(self.email)