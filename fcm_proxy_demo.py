
import requests
from requests_html import HTMLSession

import time
import unittest
import os, sys
sys.path.append("D:\\mytools\\auto_suite_python")
import json
from helper.rest_api_helper import *

class TestStringMethods(unittest.TestCase):
     def test_restapi(self):


        proxydd={"https": "https://xxxxxxx:xxxxxx$4@proxydd.xxxxxx.com:8080"}
        s = requests.Session()
        s.proxies = {"http": proxydd , "https": proxydd}
        s.auth = requests.auth.HTTPProxyAuth('xxxxxxx', 'xxxxxx$4')

        # url_accounts_google = 'https://accounts.google.com/o/oauth2/auth?scope=https://www.googleapis.com/auth/androidpublisher&response_type=code&access_type=offline&redirect_uri=https://www.baidu.com&client_id=658822823335-qhjc827qh7ct24vq3mm7bi952ja3ivjv.apps.googleusercontent.com'
        # s_html = HTMLSession()
        # # prepared_request = s_html.prepare_request(url_accounts_google)
        # # s_html.rebuild_proxies(prepared_request, proxydd)
        # res_html = s_html.get(url_accounts_google, proxies=proxydd, verify=False)
        # print('----------------------------------------------------')
        # print(res_html)
        # print('----------------------------------------------------')
        # class GoogleAccountsPage(BasePage):
        #     url = 'https://accounts.google.com/o/oauth2/auth?scope=https://www.googleapis.com/auth/androidpublisher&response_type=code&access_type=offline&redirect_uri=https://www.baidu.com&client_id=658822823335-qhjc827qh7ct24vq3mm7bi952ja3ivjv.apps.googleusercontent.com'
        # driver = get_driver()
        # g = GoogleAccountsPage()
        # g.open()
        # print(driver.current_url)
        # r = requests.get("url_1", proxies=proxydd)
        # print(r.text)
        
        url = 'https://accounts.google.com/o/oauth2/token'
        # REQ_BODY = {
        #     'grant_type':'authorization_code',
        #     'code':'4/dQCez7DUrNZ8hrVCKYPcHyGeK04hgWv41DAq0rbWOI9-Hf39KGHTwrdC-evhxhnWbOrx58AzO2pViiQq1mEuH2A',
        #     'client_id':'658822823335-qhjc827qh7ct24vq3mm7bi952ja3ivjv.apps.googleusercontent.com',
        #     'client_secret':'MDez1Y8X0sD1jzzC86UIhfNS',
        #     'redirect_uri':'https://www.baidu.com'
        # }

        req_refresh_token_zxw = {
            'grant_type':'refresh_token',
            'client_id':'658822823335-n0lr6c6gc891mq9d2i1m3cs4qqojmej4.apps.googleusercontent.com',
            'client_secret':'de1AIn7L3C_iEEw7NxisnATq',
            'refresh_token':'1/-oj8fSogcIU_Iq_unEUCkipma-VMf5-NlsMUqez38bbQ6EvKhnPSlC0BrmdtoQX4'
        }
        res = s.post(url, req_refresh_token_zxw, proxies=proxydd, verify=False)

        print('----------------------------------------------------')
        print('response: %s' % (res))
        print(res.text)
        print('access_token: [%s]' % (json.loads(res.text).get('access_token')))
        print('----------------------------------------------------')

        
if __name__ == '__main__':
    unittest.main()
