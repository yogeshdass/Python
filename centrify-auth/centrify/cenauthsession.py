'''
Created on Aug 25, 2016

@author: shashank_dixit
'''

class AuthSession(object):
    '''
    Authentication Result, which will store session id and session token (i.e. aspxauth cookie value)
    '''

    def __init__(self, endpoint, username, session_id, session_token):
        self.endpoint = endpoint
        self.username = username
        self.session_id = session_id
        self.session_token = session_token
        