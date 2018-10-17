
import boto3
import logging


class AWS_EC2_INSTANCE(object):
    def __init__(self):
        self.name = None
        self.id = None
        self.ip_public = None
        self.ip_private = None
        self.type = None
        self.state = None

    def parser(self, raw_data):
        self.id = raw_data[0]['InstanceId']
        if 'PublicIpAddress' in raw_data[0]:
            self.ip_public = raw_data[0]['PublicIpAddress']
        else:
            self.ip_public = "-"

        self.ip_private = raw_data[0]['PrivateIpAddress']
        self.state = raw_data[0]['State']['Name']
        self.type = raw_data[0]['InstanceType']

        for t in raw_data[0]['Tags']:
            if t['Key'] == 'Name':
                self.name = t['Value']


class AWS_EC2_INSTANCES(object):
    def __init__(self):
        self.instances = []

    def insert(self, instance):
        self.instances.append(instance)

    def dump_to_csv(self):
        csv_raw = "instance_id;name;state;ip_private;ip_public\n"
        for i in self.instances:
            i_line = "{};{};{};{};{};{}".format(i.type,
                    i.id, i.name, i.state, i.ip_private,
                    i.ip_public)
            csv_raw = "{}{}\n".format(csv_raw,i_line)
        return csv_raw


def aws_ec2_instances_describe():
    """Describe all instances according main attrs """
    instances = AWS_EC2_INSTANCES()
    ec2_client = boto3.client('ec2')
    ec2_client_instances = ec2_client.describe_instances()

    if 'Reservations' in ec2_client_instances:
        for r in ec2_client_instances['Reservations']:
            ec2_i = AWS_EC2_INSTANCE()
            ec2_i.parser(r['Instances'])
            instances.insert(ec2_i)

    return instances
