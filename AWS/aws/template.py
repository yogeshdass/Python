#!/usr/bin/env python3.7

class _Base(dict):
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def __getitem__(self, key):
        return dict.__getitem__(self, key)

    def __setitem__(self, key, val):
        dict.__setitem__(self, key, val)

    def __repr__(self):
        return dict.__repr__(self)

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            self[k] = v

class _Resource(_Base):
    def __init__(self, *args, **kwargs):
        self.update({kwargs['ResourceId']:{}})
        if 'Type' in kwargs:
            raise ValueError("Type cannot be initalized")
        else:
            self[kwargs['ResourceId']].update({'Type':args[0]})
        if len(kwargs) is not 1:
            if 'DependsOn'  in kwargs:
                self[kwargs['ResourceId']].update({'DependsOn':kwargs['DependsOn']})
            __properties_dict = dict()
            __restricted_attributes = set(['Type','DependsOn','ResourceId'])
            __properties_dict.update((k, v) for k, v in kwargs.items() if k not in __restricted_attributes)
            self[kwargs['ResourceId']].update({'Properties':__properties_dict})
            if 'Tags' in kwargs and isinstance(kwargs['Tags'], list):
                self[kwargs['ResourceId']]['Properties'].update({'Tags':kwargs['Tags']})

class Output(_Base):
    def __init__(self, **kwargs):
        if 'Value' in kwargs:
            self[kwargs['Name']]={"Value":kwargs['Value']}
        if 'ExportName' in kwargs:
            self[kwargs['Name']]['Export']= {"Name":kwargs['ExportName']}

class Template(_Base):
    def __init__(self):
        self.set_version("2010-09-09")

    def set_version(self, AWSTemplateFormatVersion:str):
        """ Set the template format version. Default is 2010-09-09 """
        self['AWSTemplateFormatVersion'] = AWSTemplateFormatVersion

    def set_description(self, Description:str):
        """ Set Description for the template """
        self['Description'] = Description

    def set_resource(self, Resources):
        """ Set any Resource by passing AWS Resource Objects """
        try:
            if self.__class__.set_resource.called:
                #Update Resources
                self['Resources'].update(Resources)
        except AttributeError:
            # Initialize Resources First Time
            self.update({'Resources': {}})
            self['Resources'].update(Resources)
            self.__class__.set_resource.called = True
            self.__class__.set_resource(self, Resources)

    def set_output(self, Output: dict()):
        """ Set Output or Export values for references"""
        try:
            if self.__class__.set_output.called:
                # Update Outputs
                self['Outputs'].update(Output)
        except AttributeError:
            # Initialize Outputs First Time
            self.update({'Outputs': {}})
            self['Outputs'].update(Output)
            self.__class__.set_output.called = True
            self.__class__.set_output(self, Output)
