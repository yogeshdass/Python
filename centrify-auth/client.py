'''
Created on Aug 28, 2016

@author: shashank_dixit
'''
from centrify import cenauth
from centrify import cenapp
from aws import assumerolesaml
import logging
from config import readconfig
from centrify import uprest
import re
import sys

def get_environment(environments):
    return environments[0]

def login_instance(proxy, environment):
    user = input('Please enter your username : ')
    version = "1.0"
    #session = cenauth.centrify_interactive_login(environment.get_endpoint(), user, version, environment.get_certpath(), proxy)
    session = cenauth.centrify_interactive_login(user, version, proxy, environment)
    return session, user

def set_logging():
    logging.basicConfig(handlers=[logging.FileHandler('python-aws-v6.log', 'w', 'utf-8')], level=logging.INFO, format='%(asctime)s %(filename)s %(funcName)s %(lineno)d %(message)s')
    logging.info('Starting App..')
    print("Logfile - python-aws-v6.log")
    

def select_app(awsapps):
    print("Select the aws app to login. Type 'quit' or 'q' to exit")
    count = 1
    for app in awsapps:
        print(str(count) + " : " + app['DisplayName'] + " | " + app['AppKey'])
        count = count+1
    return input("Enter Number : ")

def select_region():
    return input("Enter Region [default region is 'us-west-2'] : ")
                 
def client_main():
    set_logging()
    try:
        proxy_obj, environments = readconfig.read_config()
    except:
        logging.info("Either environment.properties or proxy.properties file not found. Please make sure the files are at home dir of the script.")
        print("Either environment.properties or proxy.properties file not found. Please make sure the files are at home dir of the script.")
        sys.exit()
    proxy = {}
    if proxy_obj.is_proxy() == 'yes':
        proxy={ 'http':proxy_obj.get_http(), 'https':proxy_obj.get_https(), 'username':proxy_obj.get_user(), 'password':proxy_obj.get_password() }
    environment = get_environment(environments)
    session, user = login_instance(proxy, environment)
    
    region = select_region()
    if (region == ""):
        region = "us-west-2"
    
    response = uprest.get_applications(user, session, environment, proxy)
    result = response["Result"]
    logging.info("Result " + str(result))
    apps = result["Apps"]
    logging.info("Apps : " + str(apps))
    length = len(apps)
    awsapps = [ apps[j] for j in range(length) if (("AWS" in apps[j]["TemplateName"] or "Amazon" in apps[j]["TemplateName"]) and apps[j]["WebAppType"] != 'UsernamePassword')]
    logging.info("AWSapps : " + str(awsapps))
    pattern = re.compile("[^0-9.]")
    count = 1
    while(True):
        number = select_app(awsapps)
        if (re.match(pattern, number)):
            print("Exiting..")
            break
        if (int(number) - 1 >= len(awsapps)):
            continue
        
        appkey = awsapps[int(number)-1]['AppKey']
        display_name = awsapps[int(number)-1]['DisplayName']
        print("Calling app with key : " + appkey)
        awsinputs = cenapp.call_app(session, appkey, "1.0", environment, proxy)
        assumerolesaml.assume_role_with_saml(awsinputs.role, awsinputs.provider, awsinputs.saml, count, display_name, region)
        count = count + 1
        awsapps.pop(int(number) - 1)
        if (len(awsapps) == 0):
            print("Exiting..")
            break
        
    logging.info("Done")
    logging.shutdown()
    
client_main()
