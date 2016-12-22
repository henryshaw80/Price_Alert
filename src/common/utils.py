__author__ = 'Timur'

from passlib.hash import pbkdf2_sha512

class Utils(object):

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checks that password the user sent matches that of the database
        Database password is encrypted more thatn the user's password at this stage
        :param password:  sha512 hashed password
        :param hashed_password: pbkdf2 encrypted password
        :return: True is password match, False otherwise
        """
        return pbkdf2_sha512.verify(password, hashed_password)