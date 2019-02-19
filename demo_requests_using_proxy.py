
import requests

import time
import unittest
import os, sys
sys.path.append("D:\\mytools\\auto_suite_python")
import json
from helper.rest_api_helper import *

class TestStringMethods(unittest.TestCase):
     def test_restapi(self):

        myproxy={"https": "https://xxxxxxx:mimamima$4@myproxy.xxxxxx.com:8080"}
        s = requests.Session()
        s.proxies = {"http": myproxy , "https": myproxy}
        s.auth = requests.auth.HTTPProxyAuth('xxxxxxx', 'mimamima')

        url = 'https://accounts.google.com/o/oauth2/token'
        req_refresh_token_zxw = {
            'grant_type':'refresh_token',
            'client_id':'xxxxxxxxxxxxxxx',
            'client_secret':'xxxxxxxxx',
            'refresh_token':'xxxxxxxxxxxxx'
        }
        res = s.post(url, req_refresh_token_zxw, proxies=myproxy, verify=False)

        '''
        {
        "access_token" : "xxxxxxxxxxxxxxx",
        "expires_in" : 3600,
        "scope" : "https://www.googleapis.com/auth/androidpublisher",
        "token_type" : "Bearer"
        }
        '''
        print('----------------------------------------------------')
        print('response: %s' % (res))
        print(res.text)
        print('access_token is: [%s]' % (json.loads(res.text).get('access_token')))
        print('----------------------------------------------------')

        s.close()

if __name__ == '__main__':
    unittest.main()
