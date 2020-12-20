'''
Created on Apr 6, 2017

@author: shashank_dixit
'''
import logging

class Proxy(object):

    def __init__(self, isproxy, proxy_http, proxy_https, proxy_user, proxy_password):
        self.isproxy = isproxy
        self.proxy_http = proxy_http
        self.proxy_https = proxy_https
        self.proxy_user = proxy_user
        self.proxy_password = proxy_password
        
        
    def log(self):
        logging.info('------  Proxy -------')
        logging.info(self.isproxy)
        logging.info(self.proxy_http)
        logging.info(self.proxy_https)
        logging.info(self.proxy_user)
        logging.info('********')
        
    def is_proxy(self):
        return self.isproxy
    
    def get_http(self):
        return self.proxy_http
    
    def get_https(self):
        return self.proxy_https
    
    def get_user(self):
        return self.proxy_user
    
    def get_password(self):
        return self.proxy_password