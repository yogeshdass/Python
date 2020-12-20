'''
Created on Aug 24, 2016

@author: shashank_dixit
'''
import json
import logging

class AdvAuthRequest(object):
    '''
    Request object for advanced authentication
    '''
    def __init__(self, tenant_id, session_id, mechanism_id, password):
        self.tenant_id = tenant_id
        self.session_id = session_id
        self.mechanism_id = mechanism_id
        self.password = password
        logging.info('--------- Creating Adv Authentiation Request ----------')
        logging.info("Tenant " + tenant_id + " Session " + session_id + " Mechanism " + mechanism_id)
        
    def get_adv_auth_json_passwd(self):
        message = {}
        message['TenantId'] = self.tenant_id
        message['SessionId'] = self.session_id
        message['MechanismId'] = self.mechanism_id
        message['Action'] = "Answer"
        message['Answer'] = self.password
        json_body=json.dumps(message)
        logging.info('---------- Advance Authentication Passwd Request JSON body ------------')
        return json_body
    
    def get_adv_auth_json_startoob(self):
        message = {}
        message['TenantId'] = self.tenant_id
        message['SessionId'] = self.session_id
        message['MechanismId'] = self.mechanism_id
        message['Action'] = "StartOOB"
        json_body=json.dumps(message)
        logging.info('---------- Advance Authentication StartOOB Request JSON body ------------')
        return json_body
    
    def get_adv_auth_json_poll(self):
        message = {}
        message['TenantId'] = self.tenant_id
        message['SessionId'] = self.session_id
        message['MechanismId'] = self.mechanism_id
        message['Action'] = "Poll"
        json_body=json.dumps(message)
        logging.info('---------- Advance Authentication StartOOB Request JSON body ------------')
        return json_body
'''    
    def __str__(self, *args, **kwargs):
        return "Tenant : " + self.tenant_id + " Session : " + self.session_id + " Mechanism : " + self.mechanism_id
   
    def __repr__(self, *args, **kwargs):
        return "Tenant : " + self.tenant_id + " Session : " + self.session_id + " Mechanism : " + self.mechanism_id
'''