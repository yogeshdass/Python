'''
Created on Aug 30, 2016

@author: shashank_dixit
'''

class AwsInputs(object):
    '''
    Object contains saml, selected role and the provider
    '''


    def __init__(self, role, provider, saml):
        self.role = role
        self.provider = provider
        self.saml = saml
        