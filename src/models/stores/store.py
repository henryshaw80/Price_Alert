__author__ = 'Timur'

import uuid
from src.common.database import Database
import src.models.stores.constants as StoreConstants
import src.models.stores.errors as StoreErrors

class Store(object):
    def __init__(self, name, url_prefix, tag_name, pricequery, namequery, _id=None):
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.pricequery = pricequery
        self.namequery = namequery
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Store {}>".format(self.name)

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "pricequery": self.pricequery,
            "namequery": self.namequery
        }

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(collection=StoreConstants.COLLECTION,
                                       query={"_id":id}))

    def save_to_mongo(self):
        Database.update(StoreConstants.COLLECTION, {"_id": self._id}, self.json())

    @classmethod
    def get_by_name(cls, store_name):
        return cls(**Database.find_one(collection=StoreConstants.COLLECTION,
                                      query={'name': store_name}))

    @classmethod
    def get_by_url_prefix(cls, url_prefix):
        """
        matching url_prefix using mongodb's regex operator
        for example: http://www.john -> http://www.johnlewis.com -> Store("John Lewis")
        :param url_prefix: URL prefix
        :return: a Store class that matches with URL prefix
        """
        return cls(**Database.find_one(collection=StoreConstants.COLLECTION,
                                   query={'url_prefix': {"$regex": '^{}'.format(url_prefix)}}))

    @classmethod
    def find_by_url(cls, url):
        """
        Return a store from a url like "http://www.johnLewis.com/kin-by-john-lewis-wool-blend-peacoat-navy/p3033177"
        :param url: the item's URL
        :return: a Store, or raises a StoreNotFoundException if no store matches the URL
        """
        for i in range(0, len(url)+1):
            try:
                store = cls.get_by_url_prefix(url[:i])
                return store
            except:
                # all python method will return None if we don't specify
                # to return anything, so we can simply type pass.
                # alternatively, we can raise an exception
                raise StoreErrors.StoreNotFoundException("The URL Prefix used to find the store didn't give us any results!")

    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find(
                                        StoreConstants.COLLECTION,
                                        query={})]
    @classmethod
    def find_by_id(cls, store_id):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {'_id': store_id}))

    def delete(self):
        Database.remove(StoreConstants.COLLECTION, {'_id':self._id})