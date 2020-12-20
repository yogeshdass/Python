import ops
import json
from aws.cfops import create_cf_stack
from aws.workers import initalize_datasource, get_export
from aws.assumerole import assume_sts_role

stack_properties = {"Environment": "dev", "Product": "iBc", "Service": "vpc"}

config = dict()
with open('config.json') as config_file:
    config = json.load(config_file)

create_cf_stack(F"{stack_properties['Environment']}-{stack_properties['Product']}-{stack_properties['Service']}", json.dumps(ops.create_vpc(stack_properties, config)))
