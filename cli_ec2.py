
import sys
import json
import logging
import argparse
import boto3
from aws_ec2 import aws_ec2_instances_describe

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="cli_ec2", description='AWS EC2 ')
    parser.add_argument('command', help="CLI command", )
    #parser.add_argument('--output', metavar='o', help='Output format. Default is CSV.')

    args = parser.parse_args()

    if args.command == 'describe-instances':

        ret = aws_ec2_instances_describe()

        # dump to CSV, uniq format supported:
        print(ret.dump_to_csv())

    else:
        print("Invalid command.")
