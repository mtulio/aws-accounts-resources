
import boto3
import logging


class AWS_IAM_USER_KEYS(object):
    def __init__(self, access_key_id=None,
                 status=None, create_date=None):
        self.access_key_id = access_key_id
        self.status = status
        self.create_date = str(create_date)


class AWS_IAM_USER(object):
    def __init__(self, username):
        self.username = username
        self.access_keys = []

    def insert_access_key(self, access_key):
        self.access_keys.append(access_key)

    def get_access_keys(self):
        return self.access_keys

    def find_access_key(self, access_key):
        for a in self.access_keys:
            if a.access_key_id == access_key:
                return a
        return False
