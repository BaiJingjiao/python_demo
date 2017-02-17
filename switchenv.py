#-*- coding: utf-8 -*-

import fileinput
import json
import os.path
from os.path import abspath
from inspect import getsourcefile
import re
import xml.etree.ElementTree as ET
import sys
reload(sys)  
sys.setdefaultencoding('utf8')

def getConfItems(confJson):
    myPath = os.path.dirname(abspath(getsourcefile(lambda:0)))
    f = open(os.path.join(myPath, 'envs', confJson),'r')
    data = f.read()
    jsonObj = json.loads(data)
    return jsonObj

def updateUDPConf(UDPConfFile, jsonObj):
    # 修改UDPConfig.xml中配置项
    flag_IMServer = False
    conf_IMServer = r'<IP>' + jsonObj.get('IMServer') + '</IP>'
    print conf_IMServer
    for line in fileinput.input(UDPConfFile, inplace=True):
        if line.strip().startswith(r'<IMServer>'):
            flag_IMServer = True
        if line.strip().startswith(r'<IP>') and flag_IMServer == True:
            line = line.replace(line.strip(), conf_IMServer)
        sys.stdout.write(line)

def updateMobileUserConf(mobileUserConfFile, jsonObj):
    # 修改MobileUserConfig.xml中配置项
    conf_MAAaddress = r'<MAAaddress>' + jsonObj.get('MAAaddress') + '</MAAaddress>'
    conf_ExMAAaddress = r'<ExMAAaddress>' + jsonObj.get('ExMAAaddress') + '</ExMAAaddress>'
    print conf_MAAaddress 
    print conf_ExMAAaddress
    for line in fileinput.input(mobileUserConfFile, inplace=True):
        if line.strip().startswith(r'<MAAaddress>'):
            line = line.replace(line.strip(), conf_MAAaddress)
        if line.strip().startswith(r'<ExMAAaddress>'):
            line = line.replace(line.strip(), conf_ExMAAaddress)
        sys.stdout.write(line)

def updateDBInfo(varPy, jsonObj):
    # 修改VAR.py中数据库配置项
    dbObj = jsonObj.get('DB')
    for item in dbObj:
        pattern = "^" + item + "\s*=\s*'.*'"
        repl = item + " = " + "'" + dbObj.get(item)+ "'"
#         with open(varPy) as f:
#             f = iter(f)
#             for line in f:
#                 if re.search(pattern, line.strip()):
#                     print line
#                     print re.sub(pattern, repl, line.decode('utf-8'))
        for line in fileinput.input(varPy, inplace=True):
            if re.search(pattern, line.strip()):
                line = re.sub(pattern, repl, line)
            sys.stdout.write(line)

def updateTestAccounts(varPy, jsonObj):
    # 修改VAR.py中测试账号配置项
    accountObj = jsonObj.get('ACCOUNTS')
    for item in accountObj:
        pattern = "^" + item + "\s*=\s*'.*'"
        repl = item + " = " + "'" + accountObj.get(item) + "'"
        for line in fileinput.input(varPy, inplace=True):
            if re.search(pattern, line.strip()):
                line = re.sub(pattern, repl, line)
            sys.stdout.write(line)  

def switchEvn(confJson):
    print 'using confJson: ', confJson
    mobileUserConf = r'D:\xCloud_ECS\executor\config\MobileUserConfig.xml'
    UDPConf = r'D:\xCloud_ECS\executor\config\cfg\UDPConfig.xml'
    varPy = r'D:\xCloud_ECS\executor\xCloudFrame\Userfiles\packages\AW\VAR.py'
#     mobileUserConf = r'MobileUserConfig.xml'
#     UDPConf = r'UDPConfig.xml'
#     varPy = r'VAR.py'
    jsonObj = getConfItems(confJson)
    updateUDPConf(UDPConf, jsonObj)
    updateMobileUserConf(mobileUserConf, jsonObj)
    updateDBInfo(varPy, jsonObj)
    updateTestAccounts(varPy, jsonObj)
    
def printMenu():
    print 
    print u'选项 : 选项说明'
    print '---------------------'
    print u'1    : 华为UC灰度'
    print u'2    : 深圳开发环境'
    print u'3    : 杭州开发环境'
    print u'exit : 退出'
    print

def getJsonFile(env):
    jsonFiles = {
                 '1': 'env_info_uc.json',
                 '2': 'env_info_shenzhen_dev.json',
                 '3': 'env_info_hangzhou_dev.json'
                 }
    return jsonFiles.get(env)


if __name__ == '__main__':
    printMenu()
    env = raw_input(u'将测试环境切换至： '.encode(sys.stdout.encoding))
    env = env.strip()
    if env.lower() == 'exit':
        pass
    elif env not in ['1', '2', '3']:
        print '\n', env, u' 为无效选项。'
    else:
        confJson = getJsonFile(env)
        switchEvn(confJson)
     
