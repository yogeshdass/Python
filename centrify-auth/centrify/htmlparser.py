'''
Created on Aug 26, 2016

@author: shashank_dixit
'''

from html.parser import HTMLParser

class CentrifyHtmlParser(HTMLParser):
    '''
    Parser for HTML response received from handleAppClick method
    '''
    def __init__(self):
        super().__init__()
        self.reset()
        self.saml = ''
        
    def handle_startendtag(self, tag, attrs):
        if (tag == 'input'):
            for attr in attrs:
                if (attr[0] == 'name' and attr[1] == 'TARGET'):
                    break
                if (attr[0] == 'value'):
                    saml = attr[1]
                    self.saml = saml
        
    def get_saml(self):
        return self.saml
    
    def clean(self):
        self.saml = ''