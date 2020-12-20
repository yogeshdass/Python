'''
Created on Apr 6, 2017

@author: shashank_dixit
'''
import configparser
import base64
from getpass import getpass
import logging
from config import proxy
from config import environment
from config import apps

def set_logging():
    logging.basicConfig(filename='config.log', level=logging.INFO)
    logging.info('Starting App..')
    
def read_proxy():
    file_reader = configparser.ConfigParser()
    config_file = 'proxy.properties'
    file_reader.read(config_file)
    isproxy = file_reader['Proxy']['proxy']
    http_proxy = file_reader['Proxy']['http_proxy']
    https_proxy = file_reader['Proxy']['https_proxy']
    proxy_user = file_reader['Proxy']['proxy_user']
    proxy_password = file_reader['Proxy']['proxy_password']
    proxy_object = proxy.Proxy(isproxy, http_proxy, https_proxy, proxy_user, proxy_password)
    return proxy_object
    
def read_environments():
    file_reader = configparser.ConfigParser()
    config_file = 'environment.properties'
    file_reader.read(config_file)
    sections = file_reader.sections()
    environments = []
    for section in sections:
        endpoint = file_reader[section]['endpoint']
        certpath = file_reader[section]['certpath']
        debug = file_reader[section]['debug']
        environment_object = environment.Environment(str(section), endpoint, certpath, debug)
        environments.append(environment_object)
    return environments
        
def log_config(proxy, environments):
    proxy.log()
    for environment in environments:
        environment.log()
        
def read_config():
    proxy = read_proxy()
    environments = read_environments()
    log_config(proxy, environments)
    return proxy, environments
    

