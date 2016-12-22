__author__ = 'Timur'

from passlib.hash import pbkdf2_sha512

class Utils(object):

    @staticmethod
    def hash_password(password):
        """
        Hashes a password using pbkdf2_sha512
        :param password: sha512 password from the login/register form
        :return: a sha512->pbkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.encrypt(password)

        # difference between pbkdf2_sha512 vs sha512
        # pbkdf2_sha512: can be decrypted, but encryption always change
        # sha512: cannot be decrypted, but encryption always fixed

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