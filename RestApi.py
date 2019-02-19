#-*- coding: utf-8 -*-

import http.client
import socket
import ssl
import json
import time
import hashlib
import re
import binascii

class RestApi(http.client.HTTPSConnection):

    def __init__(self, *args, **kwargs):
        http.client.HTTPSConnection.__init__(self, *args, **kwargs)
    
    def connect(self):
        sock = socket.create_connection((self.host, self.port), self.timeout, self.source_address)
        if self._tunnel_host:
            self.sock = sock
            self._tunnel()                    
        try:
            # self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_TLSv1)
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_TLSv1_2)
        except ssl.SSLError:
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_SSLv23)

    # 生成MD5
    def generate_md5(self, str):
        # 创建md5对象
        hl = hashlib.md5()

        # 此处必须声明encode
        # 否则报错为：hl.update(str)    Unicode-objects must be encoded before hashing
        hl.update(str.encode(encoding='utf-8'))
        print('原始字符串: %s' % (str))
        print('MD5: %s' % (hl.hexdigest()))

if __name__ == '__main__':
    URL = 'https://accounts.google.com/o/oauth2/token'
    REQ_BODY = {
        'grant_type':'authorization_code',
        'code':'',
        'client_id':'',
        'client_secret':'',
        'redirect_uri':'https://www.baidu.com'
    }
    # REQ_BODY = {
    #     'grant_type':'refresh_token',
    #     'client_id':'',
    #     'client_secret':'',
    #     'refresh_token':''
    # }
    jdata = json.dumps(REQ_BODY)
    conn = RestApi('accounts.google.com:80')
    conn.set_tunnel('proxy.blabla.com','8080')
    conn.request("POST", URL, jdata)
    
    res = conn.getresponse()
    status = res.getcode()

    print('----------------------------------------------------')
    print('response: %s' % (res))
    print('status: %s' % (status))
    print('----------------------------------------------------')

    # PUSHGW_IP = ""
    # PUSHGW_PORT = ""

    # headers_pushgw_first = {
    #     'Content-Type':'application/json;charset=UTF-8',
    #     'Accept':'application/json',
    #     'Authorization':'Digest=,username=,realm=,uri=,nonce=,method=,response='
    # }

    # conn = RestApi('10.10.10.10:8888')  

    # AUTH_URL = "https://" + xxx + ':' + xxx + "/xxxx/xx"
    # SHAKEHANDS_URL = "https://" + xxxx + ':' + xxx + "/xxx/xx/xxx"
    # print(AUTH_URL)
    # print(SHAKEHANDS_URL)
    # conn.request("POST", SHAKEHANDS_URL, headers=xxxxxx)  

    # res_first = conn.getresponse()
    # status_first = res_first.getcode()
    # header_first = res_first.getheader('WWW-Authenticate')

    # print('----------------------------------------------------')
    # print('status_first: %s' % (status_first))
    # print('header_first: %s' % (header_first))
    # print('----------------------------------------------------')
