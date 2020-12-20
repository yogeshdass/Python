'''
Created on May 29, 2017

@author: shashank_dixit
'''
import json
from centrify import cenrest
import logging
def get_applications(user, session, environment, proxy):
    method = "/uprest/getupdata"
    body = {}
    headers = {}
    headers['X-CENTRIFY-NATIVE-CLIENT'] = 'true'
    headers['Content-type'] = 'application/json'
    session_token = "Bearer "+session.session_token
    headers['Authorization'] = session_token
    response = cenrest.call_rest_post(session.endpoint, method, body, headers, environment.get_certpath(), proxy,environment.get_debug())
    logging.info(response.text)
    return response.json()

