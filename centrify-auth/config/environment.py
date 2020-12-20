'''
Created on Apr 6, 2017

@author: shashank_dixit
'''
import logging

class Environment(object):

    def __init__(self, name, endpoint, certpath, debug):
        self.name = name
        self.endpoint = endpoint
        self.certpath = certpath
        self.debug = debug
        self.applications = []
        
        
    def log(self):
        logging.info('--------- Environment -----------')
        logging.info(self.name)
        logging.info(self.endpoint)
        logging.info(self.certpath)
        for application in self.applications:
            application.log_application()
        
    def get_name(self):
        return self.name
    
    def get_endpoint(self):
        return self.endpoint
    
    def get_certpath(self):
        return self.certpath
    
    def get_debug(self):
        return self.debug
    
    def get_apps_properties(self):
        return self.apps_properties
    
    def get_applications(self):
        return self.applications
    
    def set_applications(self, applications):
        self.applications = applications