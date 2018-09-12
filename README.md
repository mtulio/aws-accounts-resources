# aws-resources

`aws-resources` is an tool to find AWS resources on distributed accounts using
assume roles (without exporting vars for each account).

Useful for whom wants to manage multiple accounts and does not use AWS Organizations.

## Setup

Create JSON with AWS accounts config:

```json
{
  "AWS_ORGANIZATIONS": {
    "name": "My Org",
    "AWS_ACCOUNTS": [
      {
        "id": "123456789012",
        "alias": "root",
        "assume_role_name": "script-iam-role-access"
      },
      {
        "id": "123456789013",
        "alias": "prod",
        "assume_role_name": "script-iam-role-access"
      }
    ]
  }
}
```


## AWS IAM Lookup

Lookup IAM Access ID in different AWS Accounts.

* Lookup one access key ID:

`time python3 cli_iam.py find-access-key --config ${PWD}/config.json --access-key AKIAXXXXXXXXXXXXX |jq .`

* Lookup one or more access keys ID:

`time python3 cli_iam.py find-access-keys --config ${PWD}/config.json --access-keys AKIAXXXXXXXXXXXXX,AKIAYYYYYYYYY |jq .`


## SETUP

* install boto3

`pip install boto3`


## HELP

* [AWS Assume Role in Python](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-api.html)
