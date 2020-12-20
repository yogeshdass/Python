'''
Created on Aug 26, 2016

@author: shashank_dixit
'''
from centrify.htmlparser import CentrifyHtmlParser
import logging

class HtmlResponse(object):
    '''
    Html Response from handle app click which consists of SAML
    '''
    def __init__(self, html_response):
        self.html_response = html_response
        self.saml = '';
        
    
    def get_saml(self):
        htmlparser = CentrifyHtmlParser()
        htmlparser.feed(self.html_response)
        saml = htmlparser.get_saml()
        htmlparser.clean()
        logging.info("------------ SAML ---------------")
        logging.info(saml)
        return saml
        