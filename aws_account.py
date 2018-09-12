import boto3
from aws_iam import AWS_IAM_USER, AWS_IAM_USER_KEYS


class AWS_ACCOUNT(object):
    def __init__(self, account_id, alias, role_name):
        self.id = account_id
        self.alias = alias
        self.role_name = role_name
        self.role_arn = ("arn:aws:iam::{}:role/{}".format(self.id,
                            self.role_name))
        self.credentials = None
        self.iam_users = []
        self.clients = {
            "iam": None
        }

        self.load_credentials()

    def load_credentials(self):
        """
        Assume role ARN and get credentials from account ID.
        """
        sts_client = boto3.client('sts')

        # Call the assume_role method of the STSConnection object and pass the role
        # ARN and a role session name.
        assumedRoleObject = sts_client.assume_role(
            RoleArn=self.role_arn,
            RoleSessionName="AwsOrgSessionSession"+self.alias
        )

        # From the response that contains the assumed role, get the temporary
        # credentials that can be used to make subsequent API calls
        self.credentials = assumedRoleObject['Credentials']
        return

    def get_client(self, service):
        if not self.clients[service]:
            self.clients[service] = boto3.client(
                service,
                aws_access_key_id = self.credentials['AccessKeyId'],
                aws_secret_access_key = self.credentials['SecretAccessKey'],
                aws_session_token = self.credentials['SessionToken'],
            )

        return self.clients[service]

    def load_users(self):
        """
        Load all IAM users to object.
        We need the users to find the Access Key ID
        """
        client_iam = self.get_client("iam")

        resp_users = client_iam.list_users(MaxItems=200)

        if "Users" not in resp_users:
            print("Error getting users")
            return

        if len(resp_users["Users"]) < 1:
            print("No users in account")
            return

        for user in resp_users["Users"]:
            u = AWS_IAM_USER(
                user['UserName']
            )
            # self.load_user_access_keys(u)
            self.iam_users.append(u)

        return

    def load_user_access_keys(self, u):

        client_iam = self.get_client("iam")
        resp_access = client_iam.list_access_keys(
            UserName=u.username,
        )

        if 'AccessKeyMetadata' in resp_access:
            for a in resp_access['AccessKeyMetadata']:
                access = AWS_IAM_USER_KEYS(
                    access_key_id=a['AccessKeyId'],
                    status=a['Status'],
                    create_date=a['CreateDate']
                )
                u.insert_access_key(access)


    def find_iam_user_access_key(self, access_key_id):

        if len(self.iam_users) < 1:
            self.load_users()

        for u in self.iam_users:
            if len(u.access_keys) < 1:
                self.load_user_access_keys(u)

            user_key = u.find_access_key(access_key_id)
            if user_key:
                return {
                    "account_id": self.id,
                    "account_alias": self.alias,
                    "username": u.username,
                    "user_key_id": user_key.access_key_id,
                    "user_key_status": user_key.status,
                    "user_key_create_date": user_key.create_date
                }

        return {"Error": "Access Key ID not found"}
