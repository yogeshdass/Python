#!/usr/bin/env python3.7

from boto3 import client
from json import dumps, load

def get_azes(region):
    __azes=list()
    for i in client('ec2', region_name=region).describe_availability_zones()['AvailabilityZones']:
        __azes.append(i["ZoneName"])
    return __azes
    
def initalize_datasource(region):
    exports_list = dict()
    response = client('cloudformation', region_name=region).list_exports()['Exports']
    for _ in response:
        exports_list.update({F"{_['Name']}" : F"{_['Value']}"})
    with open("datasource","w+") as datasource:
        datasource.write(dumps(exports_list))

def get_export(name):
    with open("datasource","r+") as d:
        return load(d)[name]

def waste_allocation_load_lifter():
    from os import remove
    remove("datasource")

