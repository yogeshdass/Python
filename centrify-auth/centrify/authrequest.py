'''
Created on Aug 24, 2016

@author: shashank_dixit
'''
import json
import logging

class AuthRequest(object):
    '''
    Message body required for Authentication requests
    '''
    def __init__(self, tenantid, username, version, password=''):
        self.tenantid = tenantid
        self.username = username
        self.version = version
        
    def get_start_auth_json(self):
        message={}
        if (self.tenantid):
            message['TenantId']=self.tenantid
        message['User']=self.username
        message['Version']=self.version
        json_body=json.dumps(message)
        logging.info('--------- Body of Start Authentication Request --------------')
        logging.info(json_body)
        return json_body
    
