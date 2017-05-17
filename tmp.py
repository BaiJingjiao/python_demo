# -*- coding:utf-8 -*-

import fileinput
import sys
import json
import os.path
from os.path import abspath
from inspect import getsourcefile
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from datetime import timedelta
import string
import random
import time

# a = {
#     'x' : 1,
#     'y' : 2,
#     'z' : 3
#     }
# b = {
#     'w' : 10,
#     'x' : 11,
#     'y' : 2
#     }

dic1 = {"result":"0","syncType":"0","stamp":"20170517160510","groupMemberList":[{"groupID":"678255","type":"0","state":"0","userAccount":"ecsautotest100","user":{"staffID":"409099","userAccount":"ecsautotest100","staffNo":"00681099","userName":"ecs自动化测试100","sex":"女","mobile":"13000000175","homePhone":"7670174","officePhone":"0571271374","otherPhone":"870175","fax":"610174","email":"ecstest100@huawei.com","addr":"杭州滨江江虹路410号","picID":"t089","zip":"430184","voIp":"1174","bindNo":"00681099","deptID":"1","state":"0","oldStaffAccount":"ecsautotest100","modifyTime":"20160706132515"},"userID":"409099"},
                                                                                {"groupID":"678255","type":"0","state":"0","userAccount":"ecsautotest98","user":{"staffID":"409097","userAccount":"ecsautotest98","staffNo":"00681097","userName":"ecs自动化测试98","sex":"男","birthday":"19950208","age":"12","mobile":"13000000173","homePhone":"0571869764","officePhone":"0571271372","otherPhone":"578645","otherPhone2":"45487","fax":"0571","email":"myemail@huawei.com","website":"mywebsite","underwrite":"hello","addr":"杭州滨江江虹路410号","picID":"ecsauto","zip":"430182","voIp":"1172","title":"mytitle","bindNo":"00681097","deptID":"1","state":"0","oldStaffAccount":"ecsautotest98","modifyTime":"20170516190901"},"userID":"409097"},
                                                                                {"groupID":"678255","type":"0","state":"0","userAccount":"ecsautotest99","user":{"staffID":"409098","userAccount":"ecsautotest99","staffNo":"00681098","userName":"ecs自动化测试99","sex":"女","mobile":"13000000174","homePhone":"7670173","officePhone":"0571271373","otherPhone":"870174","fax":"610173","email":"ecstest99@huawei.com","addr":"杭州滨江江虹路410号","picID":"t088","zip":"430183","voIp":"1173","bindNo":"00681098","deptID":"1","state":"0","oldStaffAccount":"ecsautotest99","modifyTime":"20160706132515"},"userID":"409098"}],"isExist":"0","sno":"1493276324206087"}
dic2 = {"result":"0","syncType":"0","groupMemberList":[{"groupID":"678255","user":{"staffID":"409099","userAccount":"ecsautotest100"}},
                                                       {"groupID":"678255","user":{"staffID":"409098","userAccount":"ecsautotest99"}}
                                                       ]}
 
if dic1 == dic2:
    print 'yes'
else:
    print 'no'
 
dic3 = dict((k, dic1[k]) for k in dic2.keys())
print dic3

'''list比较顺序敏感'''
# a = ['aaa', 'bbb', 'ccc']
# b = ['aaa', 'ccc', 'bbb']
# 
# if a. == b:
#     print 'yes'
# else:
#     print 'no'


'''中文输出问题'''
# a = ['中国','浙江','杭州']
# print (json.dumps(a, encoding='utf-8', ensure_ascii=False)).decode('utf-8')

# text = 'dkdj'
# print isinstance(text, str)
# print isinstance(text, unicode)
# print isinstance(text, (str, unicode))
# print isinstance(text, basestring)

myPath = os.path.dirname(abspath(getsourcefile(lambda:0)))

# print int('0x23', 16)

# mylist = [1,2,3]
# 
# for num in mylist:
#     print num
# else:
#     print num -1

# now = datetime.today()
# print now
# print(now + timedelta(seconds=-10))
#  
# mytime = datetime.strftime(now, '%Y-%m-%d %H.%M.%S.%f')
# mytime = re.sub('000$', '', str(mytime))
# print mytime

# now = time.time()
# print now
# print '{0:.0f}'.format(now * 1000)

# groupInfo1 = {  
#         "senderAccount": 'ACCOUNT_A',  
#         "groupName": 'GROUP_NAME',  
#         "capacity": "10",  
#         "owner": 'ACCOUNT_A',  
#         "joinFlag": "0",  
#         "manifesto": "1",  
#         "desc": "1",  
#         "groupType": "0",  
#         "inviteList":   
#         [  
#             'ACCOUNT_B', 
#             'ACCOUNT_C'
#         ],  
#         "appID": "1"  
#     }
# groupInfo2 = {  
#         "senderAccount": 'ACCOUNT_A',  
#         "groupName": 'GROUP_NAME',  
#         "groupType": "0",  
#         "capacity": "10",  
#         "owner": 'ACCOUNT_A',  
#         "joinFlag": "0",  
#         "manifesto": "1",  
#         "desc": "1",  
#         "inviteList":   
#         [  
#             'ACCOUNT_B', 
#             'ACCOUNT_C'
#         ],  
#         "appID": "1"  
#     }
# 
# print(json.dumps(groupInfo2, indent=2))

# for i in range(100):
#     print '"account'+str(i+1)+'",'

# 
# chars=string.digits
# myrandom = ''.join(random.choice(chars) for _ in range(21))
# print myrandom

# ids_fromDB = [693, 694, 695, 696, 721, 85280, 245195, 405214, 565162, 725157, 802275, 846128, 851350, 878475, 885080, 885795, 889034, 890536, 916222, 925642, 1045063, 1124967, 1205007, 1250313, 1342105, 1364971, 1515276, 1521454, 1524965, 1684527, 2027344, 2035691, 2038686, 2064502, 2463605, 2463606, 2463609, 2463611, 2463612, 2463613, 2463614, 2463615, 2463616, 2463617, 2463618, 2463619, 2463620, 2463621, 2463622, 2463623, 2463624, 2463625, 2463626, 2463627, 2463628, 2463641, 2463642, 2463643, 2463644, 2463645]
# ids_total = ['1045063', '1124967', '1205007', '1250313', '1342105', '1364971', '1515276', '1521454', '1524965', '1684527', '2027344', '2035691', '2038686', '2064502', '245195', '2463605', '2463606', '2463609', '2463611', '2463612', '2463613', '2463614', '2463615', '2463616', '2463617', '2463618', '2463619', '2463620', '2463621', '2463622', '2463623', '2463624', '2463625', '2463626', '2463627', '2463628', '2463641', '2463642', '2463643', '2463644', '2463645', '405214', '565162', '693', '694', '695', '696', '721', '722', '723', '725157', '802275', '85280', '878475', '885080', '885795', '889034', '890536']
# 
# ids_fromDB = [str(i) for i in ids_fromDB]
# 
# #在ids_fromDB，不在ids_total的元素
# ret = list(set(list(ids_fromDB)).difference(set(ids_total)))
# #在ids_total，不在ids_fromDB的元素
# ret2 = list(set(list(ids_total)).difference(set(ids_fromDB)))
#                 
# print sorted(ids_fromDB)
# print sorted(ids_total)
# print ret
# print ret2

# import ftplib
# filename = "eServer.log"
# ftp = ftplib.FTP("10.174.3.1")
# ftp.login("ecs", "ecs@123")
# ftp.cwd("/home/ecs/20140925/Logs/MAA")
# ftp.retrbinary('RETR %s' % filename, open('myoutputfile.txt', 'wb').write)
# 
# ftp.storbinary('STOR %s' % 'ddd.py', open('ddd.py', 'r'), blocksize=1024)
# 
# # import base64
# import paramiko
# #     paramiko.util.log_to_file("filename.log")
# # key = paramiko.RSAKey(data=base64.b64decode(b'AAA...'))
# client = paramiko.SSHClient()
# # client.get_host_keys().add('10.174.3.1', 'ssh-rsa', key)
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# # client.connect('10.174.3.1', username='ecs', password='ecs@123')
# client.connect('3.1.133.23', 22, username='root', password='root')
# stdin, stdout, stderr = client.exec_command('ls -l')
# for line in stdout:
#     print('... ' + line.strip('\n'))
# client.close()

# p = os.path.dirname('/root/.config/xxxxx.log')
# n = os.path.basename('/root/.config/xxxxx.log')
# print p
# print n
# def getRandomNum(length):
#     chars=string.digits
#     myrandom = ''.join(random.choice(chars) for _ in range(length))
