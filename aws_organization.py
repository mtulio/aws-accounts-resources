
import json
from aws_account import AWS_ACCOUNT


class AWS_ORG(object):
    """ Try to define organizations or read from config file """
    def __init__(self, name=None, filename=None):
        self.name = name
        self.accounts = []

        if filename:
            self.load_config(filename=filename)

    def load_config(self, filename=None):
        """ Load config from config.json """
        conf = {}

        if filename:
            conf_file = filename
        else:
            conf_file = './config.json'

        with open(conf_file) as data_file:
            conf = json.load(data_file)

        org = conf["AWS_ORGANIZATIONS"]
        self.name = org["name"]

        for a in org["AWS_ACCOUNTS"]:
            acc = AWS_ACCOUNT(
                account_id=a["id"],
                alias=a["alias"],
                role_name=a["assume_role_name"],
            )
            self.accounts.append(acc)
        return

    def find_access_key(self, access_key_id):
        for a in self.accounts:
            u = a.find_iam_user_access_key(access_key_id)

            if not u:
                return "not found"

            if 'username' in u:
                return u
