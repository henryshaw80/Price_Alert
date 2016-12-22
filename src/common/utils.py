__author__ = 'Timur'

from passlib.hash import pbkdf2_sha512

class Utils(object):

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checks that the password the user sent matches that of the database
        The database password is encrypted more than the user's password at this stage
        :param password: sha512 hashed password
        :param hashed_password:  pbkdf2_sha512 encrypted password
        :return: True if passwords match, False otherwise
        """
        return pbkdf2_sha512.verify(password, hashed_password)