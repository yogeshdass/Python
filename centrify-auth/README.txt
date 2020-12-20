V6
--
This version supports extra MFA policy added for apps. 

Properties files.
-----------------
There are only 2 properties files
1. Proxy.properties - for proxy details if any.
2. Environment.properties - 
    i> endpoint - The centrify endpoint e.g. https://instance.centrify.com
    ii> certpath - The SSL certificate path e.g. cacerts.pem
    

Running this script
------------------------
1. Run client.py 
2. User logs in.
3. Script displays the AWS apps from Centrify for the user to select.
4. User select AWS app to login by entering appropriate number.
5. User selects role (if there is only one role, the script will automatically take it)
6. AWS credentials are stored, if the app and role matches. If there is an error (mostly access denied) from AWS, then the script will display it and exit.

Logs
----
Logs will be stored in python-aws-v5.log

