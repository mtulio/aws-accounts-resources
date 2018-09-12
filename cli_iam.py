
import sys
import json
import logging
import argparse
from aws_organization import AWS_ORG

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="cli_iam", description='AWS Org CLI IAM ')

    parser.add_argument('command', help="CLI command", )
    parser.add_argument('--config', metavar='C', help='JSON Config file.')
    parser.add_argument('--access-key', help="AWS IAM Access Key ID.")
    parser.add_argument('--access-keys', help="AWS IAM Access Keys ID seppareted by comma.")

    args = parser.parse_args()

    # Create Organization
    if args.config:
        org = AWS_ORG(filename=args.config)
    else:
        org = AWS_ORG()

    if args.command == 'find-access-key':
        if not args.access_key:
            print("Argument --access-key not found.")
            sys.exit(1)

        ret = org.find_access_key(args.access_key)
        print(json.dumps(ret))

    elif args.command == 'find-access-keys':
        if not args.access_keys:
            print("Argument --access-keys not found.")
            sys.exit(1)

        resp = []
        for k in args.access_keys.split(','):
            ret = org.find_access_key(k)
            resp.append(ret)

        print(json.dumps(resp))

    else:
        print("Invalid command.")
