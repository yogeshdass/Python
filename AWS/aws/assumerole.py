#!/usr/bin/env python3.7
from argparse import ArgumentParser, RawTextHelpFormatter
from boto3 import client
from os.path import expanduser, exists, isfile
from configparser import ConfigParser
import json
from logging import getLogger, INFO, Formatter, StreamHandler
from sys import argv, exit, path

assume_role = client('sts').assume_role
aws_credentials = expanduser("~") + "/.aws/ycredentials"
aws_conf = expanduser("~") + "/.aws/yconfig"

logger = getLogger(__name__)
logger.setLevel(INFO)
formatter = Formatter(fmt='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s', datefmt='%d-%m-%Y %H:%M:%S')


def assume_sts_role(RoleArn, RoleSessionName, profile_name, region):
    response = assume_role(
        RoleArn=RoleArn,
        RoleSessionName=RoleSessionName)
    config = ConfigParser()
    config.read(aws_credentials)

    if not config.has_section(profile_name):
        config.add_section(profile_name)
    config.set(profile_name, 'output', 'json')
    config.set(profile_name, 'region', region)
    config.set(profile_name, 'aws_access_key_id', response['Credentials']['AccessKeyId'])
    config.set(profile_name, 'aws_secret_access_key', response['Credentials']['SecretAccessKey'])
    config.set(profile_name, 'aws_session_token', response['Credentials']['SessionToken'])
    with open(aws_credentials, 'w+') as credentials:
        config.write(credentials)

def activate_aws_profile(org, environment, profile_name):
    config = ConfigParser()
    credentials = ConfigParser()
    credentials.read(aws_credentials)
    config.read(aws_conf)
    creds = dict()
    with open('credentials.json') as creds_file:
        creds = json.load(creds_file)
    if not credentials.has_section(profile_name):
        credentials.add_section(profile_name)
    if not config.has_section(profile_name):
        config.add_section(profile_name)
    credentials.set(profile_name, 'aws_access_key_id', creds[org][environment]['aws_access_key_id'])
    credentials.set(profile_name, 'aws_secret_access_key', creds[org][environment]['aws_secret_access_key'])
    config.set(profile_name,'region', creds[org][environment]['region'])
    config.set(profile_name,'output', creds[org][environment]['op'])
    with open(aws_credentials, 'w+') as c:
        credentials.write(c)
    with open(aws_conf, 'w+') as c:
        config.write(c)

def create_profile(profile, org):
    environment = profile
    profile = "profile "+profile
    config = ConfigParser()
    config.read(aws_conf)
    creds = dict()
    with open('credentials.json') as creds_file:
        creds = json.load(creds_file)
    if not config.has_section(profile):
        config.add_section(profile)
    config.set(profile,'role_arn', creds[org][environment]['rolearn'])
    config.set(profile,'source_profile', creds[org][environment]['source_profile'])
    with open(aws_conf, 'w+') as c:
        config.write(c)

#assume_sts_role(RoleArn="arn:aws:iam::250594245224:role/lifestyle-dev-admin", RoleSessionName="temp",  profile_name = "iot_dev", region="ap-south-1") 
#activate_aws_profile(org="iot", environment="master", profile_name="default")
#create_profile(profile="dev", org="iot")


def main():
    """ Run in case of using it as Script only"""

    # create console handler which will work in case of script
    ch = StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    EPILOG = '''EXAMPLE:
        %(prog)s PROJECT ENVIRONMENT
    '''

    parser = ArgumentParser(
        epilog=EPILOG, formatter_class=RawTextHelpFormatter)
    parser.add_argument("project")
    parser.add_argument("environment", nargs='?')

    parser._positionals.title = 'Pass Project and Environment as Argument'
    parser._optionals.title = 'HELP'

    if len(argv) == 1:
        logger.info(parser.format_help())
        exit(0)
    else:
        args = parser.parse_args()
        environment = str()
        if args.environment:
            print(args.environment)
        else:
            environment = "default"
        print(environment)
        
if __name__ == "__main__":
    main()