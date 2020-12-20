'''
Created on Aug 23, 2016

@author: shashank_dixit
'''
import requests
import logging
    
def call_rest_post(endpoint, method, body, headers, certpath, proxy, debug='Off'):
    endpoint = endpoint+method
    if 'x-centrify-native-client' not in headers:
        headers['x-centrify-native-client'] = "true"
    if 'content-type' not in headers:
        headers['content-type'] = "application/json"
    if 'cache-control' not in headers:
        headers['cache-control'] = "no-cache"
#    logging.info("Calling " + endpoint)
#    logging.info("Method : " + method + " Request Body : " + str(body) + " Headers : " + str(headers) + " Proxy : " + str(proxy))

    logging.info("Calling " + endpoint + " with headers : " + str(headers))
    if (debug.lower() == 'on'):
        logging.info(" and data : " + str(body))
    
    response = requests.post(endpoint, headers=headers, verify=certpath, proxies=proxy, data=body)

#    Temporary Change
#    response = requests.post(endpoint, headers=headers, verify=False, proxies=proxy, data=body)
    logging.info("Received Response : " + response.text)
    return response

#Following method is not used currently. It will be used if redirects are needed.
def call_rest_post_redirect(endpoint, method, body, headers, certpath, proxy, allow_redirects=True):
    if 'x-centrify-native-client' not in headers:
        headers['x-centrify-native-client'] = "true"
    if 'content-type' not in headers:
        headers['content-type'] = "application/json"
    if 'cache-control' not in headers:
        headers['cache-control'] = "no-cache"
    endpoint = endpoint+method
    logging.info("Calling " + endpoint)
    logging.info("Method : " + method + " Request Body : " + str(body) + " Headers : " + str(headers) + " Proxy : " + str(proxy))
    logging.info("Calling " + endpoint + " with headers : " + str(headers) + " and data : " + str(body))
    response = requests.post(endpoint, headers=headers, verify=certpath, proxies=proxy, data=body)
    logging.info("Received Response : " + response.text)
    return response
    