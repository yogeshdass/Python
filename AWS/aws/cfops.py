#!/usr/bin/env python3.7

from argparse import ArgumentParser, RawTextHelpFormatter
from boto3 import client
from os.path import abspath
from requests import get
from sys import argv, exit, path
from time import perf_counter, sleep
from logging import getLogger, INFO, Formatter, FileHandler, StreamHandler
from threading import Thread
from datetime import datetime

cloudformation = client('cloudformation')

logger = getLogger(__name__)
logger.setLevel(INFO)
formatter = Formatter(fmt='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s', datefmt='%d-%m-%Y %H:%M:%S')

#Send logs to a file. create a file handler
fh = FileHandler(__name__+'.log')
# create a logging format
fh.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)

def _checktemplatetype(SOURCE: str) -> str:
    """ Checks the Source fo Template and returns a template String Object.  """
    if SOURCE.startswith('file://'):
        SOURCE=abspath(SOURCE.split('file://')[1])
        with open(SOURCE) as tf:
            return tf.read()
    elif SOURCE.startswith('https://') or SOURCE.startswith('http://'):
        return get(SOURCE).text
    else:
        return SOURCE

def _get_validated_template(SOURCE: str) -> str:
    """ Validate the String Object and returns it on success. """
    try:
        TEMPLATE=_checktemplatetype(SOURCE)
        cloudformation.validate_template(
            TemplateBody = TEMPLATE
        )
        logger.info('Template is Good to GO!')
    except Exception as error:
        print(error)
    else:
        return TEMPLATE

def _stack_exists(STACK_NAME: str) -> bool:
    """ Checks if  the stack exists. """
    for _ in cloudformation.list_stacks()['StackSummaries']:
        if _['StackName'] == STACK_NAME:
            if _['StackStatus'] == 'DELETE_COMPLETE':
                return False
            else:
                return True

def _get_events(STACK_NAME):
    logger.info('{:<19s} | {:<37s} | {:<19s} | {:<19s}'.format("CF Timestamp", "ResourceType", "LogicalResourceId", "ResourceStatus"))
    logger.info('{:^93s}'.format("---------------------------------------------------------------------------------------------------"))
    tabledict = dict()
    for _ in cloudformation.describe_stack_events(StackName=STACK_NAME)['StackEvents']:
        Timestamp = str(_['Timestamp'])
        if _['LogicalResourceId'] not in tabledict:
            tabledict.update({F"{_['LogicalResourceId']}" : [F"{Timestamp.split('.')[0]}", F"{_['ResourceType']}", F"{_['ResourceStatus']}"]})
        else:
            s1 = tabledict[_['LogicalResourceId']][0]
            s2 = Timestamp.split('.')[0]
            t1 = datetime.strptime(s1, '%Y-%m-%d %H:%M:%S')
            t2 = datetime.strptime(s2, '%Y-%m-%d %H:%M:%S')
            if (t1<t2):
                tabledict.update({F"{_['LogicalResourceId']}" : [F"{Timestamp.split('.')[0]}", F"{_['ResourceStatus']}"]})
    for k,v in tabledict.items():
        logger.info('{:<19s} | {:<37s} | {:<19s} | {:<19s}'.format(v[0], v[1], k, v[2]))
        logger.info('{:^93s}'.format("---------------------------------------------------------------------------------------------------"))
    logger.info("\n")

def _waiter(command, STACK_NAME):
    wait_kwargs = {
        'StackName': STACK_NAME,
        'WaiterConfig': {
            'Delay': 5,
            'MaxAttempts': 120
        }
    }
    waiter = cloudformation.get_waiter(command)
    # Anonymus Function , created because target dont take **kwards
    wait = lambda : (waiter.wait(**wait_kwargs))
    waiterthread = Thread(target=wait)
    # Start Execution  of the thread and proceed
    waiterthread.start()
    #checks if the thread is alive and performs the action
    while waiterthread.is_alive():
        _get_events(STACK_NAME)
        sleep(5)
    # Joins the thread to the Parent process
    waiterthread.join()

def create_cf_stack(STACK_NAME: str, SOURCE: str):
    """ Create or Updates the Cloudformation Stack. """
    stack_kwargs = {
        'StackName': STACK_NAME,
        'TemplateBody': _get_validated_template(SOURCE)
    }
    StackId=str()
    try:
        if _stack_exists(STACK_NAME):
            logger.info(F"Updating {STACK_NAME}")
            StackId = cloudformation.update_stack(**stack_kwargs)['StackId']
            logger.info(StackId)
            logger.info("Waiting for Stack to be UPDATED")
            _waiter('stack_update_complete', STACK_NAME)
            logger.info("Stack has been UPDATED")
        else:
            logger.info(F"Creating {STACK_NAME}")
            StackId = cloudformation.create_stack(**stack_kwargs)['StackId']
            logger.info(StackId)
            logger.info("Waiting for Stack to be CREATED")
            _waiter('stack_create_complete', STACK_NAME)
            logger.info("Stack has been CREATED")
    except Exception as e:
        logger.exception(e)
        _get_events(STACK_NAME)
    
def list_cf_stacks():
    """ Gets all the Stacks"""
    for _ in cloudformation.describe_stacks()['Stacks']:
        logger.info(F"Name = {_['StackName']}, Status = {_['StackStatus']}\n")

def delete_cf_stack(STACK_NAME: str):
    """ Deletes the given Stack"""
    StackId=cloudformation.describe_stack_events(StackName=STACK_NAME)['StackEvents'][0]['StackId']
    cloudformation.delete_stack(StackName=StackId)
    _waiter('stack_delete_complete', StackId)
    _get_events(StackId)
    logger.info("Stack Deleted")

def main():
    """ Run in case of using it as Script only"""

    # create console handler which will work in case of script
    ch = StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    start = perf_counter()

    EPILOG = '''EXAMPLE:
    o Create a Cloudformation Stack
        1) %(prog)s create-stack --stack-name STACK_NAME --template https://example.com/vpc.json

        2) %(prog)s create-stack --stack-name STACK_NAME --template file://vpc.cf.yaml

    o Delete a Cloudformation Stack
        %(prog)s delete-stack --stack-name STACK_NAME

    o List all Stacks
        %(prog)s get-stacks
    '''

    parser = ArgumentParser(
        description='Create or Delete a CloudFormation Stack or list the stacks.',
        epilog=EPILOG, formatter_class=RawTextHelpFormatter)
    subparser = parser.add_subparsers(dest='operation')
    subparser.required = True

    parser._positionals.title = 'You can run either of these Commands'
    parser._optionals.title = 'HELP'

    parser_c = subparser.add_parser("create-stack")
    parser_c.add_argument("--stack-name", '-n', required='True')
    parser_c.add_argument("--template", '-t', required='True')

    parser_d = subparser.add_parser("delete-stack")
    parser_d.add_argument("--stack-name", '-n', required='True')

    subparser.add_parser("get-stacks")

    if len(argv) == 1:
        logger.info(parser.format_help())
        exit(0)
    else:
        args = parser.parse_args()
        if args.operation == 'create-stack':
            create_cf_stack(args.stack_name, args.template)
        elif args.operation == 'delete-stack':
            delete_cf_stack(args.stack_name)
        elif args.operation == 'get-stacks':
            list_cf_stacks()

    elapsed = perf_counter() - start
    logger.info(F"{__file__} executed in {elapsed:0.2f} seconds.")

if __name__ == "__main__":
    main()