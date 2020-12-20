'''
Created on Apr 6, 2017

@author: shashank_dixit
'''

import logging

class Application(object):

    def __init__(self, awsenv, centrifyenv, appkey, role):
        self.awsenv = awsenv
        self.centrifyenv = centrifyenv
        self.appkey = appkey
        self.role = role
        
    def get_aws_env(self):
        return self.awsenv
    
    def get_centrify_env(self):
        return self.centrifyenv
    
    def get_appkey(self):
        return self.appkey
    
    def get_role(self):
        return self.role
    
    def log_application(self):
        logging.info('--------- Application -----------')
        logging.info(self.awsenv)
        logging.info(self.centrifyenv)
        logging.info(self.appkey)
        logging.info(self.role)
