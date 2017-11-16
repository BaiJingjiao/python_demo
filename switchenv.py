#-*- coding: utf-8 -*-

'''
#!+================================================================
#版权 (C) 2016-2017，华为技术有限公司 
#==================================================================
#   @Method:   本脚本用于使用配置文件切换自动化框架中环境相关信息
#              环境信息存放在本脚本所在目录的envs子文件夹下，以json文件存放
#              本脚本会根据envs目录下的配置文件名，自动生成菜单选项，选择要使用的配置文件即可
#   @Author:   bwx433051
#   @Date:     2017-09-29      
#   @Status:   Done 
#!!================================================================
'''
import fileinput
import json
import os
import os.path
from os.path import abspath
from inspect import getsourcefile
import re
import xml.etree.ElementTree as ET #暂时没有使用，因为用它修改后的xml，注释丢失
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

def updateAPPServer(appVarPy, jsonObj):
    # 修改appVAR.py中APP_IP配置项
    appServer = jsonObj.get('AppServer')
    if (None == appServer): 
        return
    item = 'APP_IP'
    pattern = "^" + item + "\s*=\s*'.*'" #这样可以保留注释
    repl = item + " = " + "'" + appServer + "'"
    try:
        for line in fileinput.input(appVarPy, inplace=True):
            if re.search(pattern, line.strip()):
                line = re.sub(pattern, repl, line)
            sys.stdout.write(line)
    except:
        pass

def updateBMUVarInfo(bmuVarPy, jsonObj):
    # 修改bmuVar.py中数据库配置项
    bmuVarObj = jsonObj.get('bmuVar')
    if (None == bmuVarObj): 
        return
    for item in bmuVarObj:
        pattern = "^" + item + "\s*=\s*'.*'" #这样可以保留注释
        repl = item + " = " + "'" + bmuVarObj.get(item)+ "'"
        try:
            for line in fileinput.input(bmuVarPy, inplace=True):
                if re.search(pattern, line.strip()):
                    line = re.sub(pattern, repl, line)
                sys.stdout.write(line)
        except:
            pass
                       
def updateDBInfo(varPy, jsonObj):
    # 修改VAR.py中数据库配置项
    dbObj = jsonObj.get('DB')
    for item in dbObj:
        pattern = "^" + item + "\s*=\s*'.*'" #这样可以保留注释
        repl = item + " = " + "'" + dbObj.get(item)+ "'"
        for line in fileinput.input(varPy, inplace=True):
            if re.search(pattern, line.strip()):
                line = re.sub(pattern, repl, line)
            sys.stdout.write(line)

def updateTestAccounts(varPy, jsonObj):
    # 修改VAR.py中测试账号配置项
    accountObj = jsonObj.get('ACCOUNTS')
    for item in accountObj:
        pattern = "^" + item + "\s*=\s*'.*'" #这样可以保留注释
        repl = item + " = " + "'" + accountObj.get(item) + "'"
        for line in fileinput.input(varPy, inplace=True):
            if re.search(pattern, line.strip()):
                line = re.sub(pattern, repl, line)
            sys.stdout.write(line)

def updateUserList(varPy, jsonObj):
    # 修改VAR.py中USERLIST配置项
    userListObj = jsonObj.get('USERLIST')
    if None == userListObj:
        return
    for item in userListObj:
        pattern = "^" + item + "\s*=\s*\[.*\]" #这样可以保留注释
        repl = item + ' = ' + userListObj.get(item)
        for line in fileinput.input(varPy, inplace=True):
            if re.search(pattern, line.strip()):
                line = re.sub(pattern, repl, line)
            sys.stdout.write(line)

def updateServerIPs(varPy, jsonObj): 
    # 修改VAR.py中ServerIP配置项
    serverIPObj = jsonObj.get('SERVERIPS') 
    for item in serverIPObj:
        pattern = "^" + item + "\s*=\s*\[.*\]" #这样可以保留注释
        ipList = serverIPObj.get(item)
        repl = item + " = ["
        for ip in ipList:
            repl = repl + "'" + ip + "', "
        else:
            repl = repl + "]"
        for line in fileinput.input(varPy, inplace=True):
            if re.search(pattern, line.strip()):
                line = re.sub(pattern, repl, line)
            sys.stdout.write(line)

def updateOthers(varPy, jsonObj): 
    # 修改VAR.py中其他配置项
    othersObj = jsonObj.get('OTHERS')
    if (None == othersObj): 
        return
    for item in othersObj:
        pattern = "^" + item + "\s*=.*" #这样替换后，注释就没了
        print ('type(othersObj.get(item))', type(othersObj.get(item)))
        if type(othersObj.get(item)) is int:
            repl = item + " = " + str(othersObj.get(item))
        elif type(othersObj.get(item)) is bool:
            if othersObj.get(item) == False:
                repl = item + " = " + 'False'
            else: 
                repl = item + " = " + 'True'
        elif othersObj.get(item) == None:
            repl = item + " = " + 'None'
        else:
            repl = item + " = " + "'" + othersObj.get(item) + "'"
        for line in fileinput.input(varPy, inplace=True):
            if re.search(pattern, line.strip()):
                line = re.sub(pattern, repl, line)
            sys.stdout.write(line)
            
def switchEvn(confJson):
    print '\n', u'使用的配置文件: ', confJson, '\n'
    mobileUserConf = r'D:\xCloud_ECS\executor\config\MobileUserConfig.xml'
    UDPConf = r'D:\xCloud_ECS\executor\config\cfg\UDPConfig.xml'
    varPy = r'D:\xCloud_ECS\executor\xCloudFrame\Userfiles\packages\AW\VAR.py'
    appVarPy = r'D:\xCloud_ECS\executor\xCloudFrame\Userfiles\packages\AW\appVAR.py'
    bmuVarPy = r'D:\xCloud_ECS\executor\xCloudFrame\Userfiles\packages\AW\bmuVAR.py'
    jsonObj = getConfItems(confJson)
    print json.dumps(jsonObj, indent=4)
    updateUDPConf(UDPConf, jsonObj)
    updateMobileUserConf(mobileUserConf, jsonObj)
    updateAPPServer(appVarPy, jsonObj)
    updateDBInfo(varPy, jsonObj)
    updateTestAccounts(varPy, jsonObj)
    updateServerIPs(varPy, jsonObj)
    updateUserList(varPy, jsonObj)
    updateOthers(varPy, jsonObj)
    updateBMUVarInfo(bmuVarPy, jsonObj)
    
def walkThroughDir(dir, files):
    '''
    #遍历目录，包括子目录，返回所有文件的列表
    '''
    fs_or_ds = os.listdir(dir)
    for f in fs_or_ds:
        f_or_d = os.path.join(dir, f)
        if os.path.isdir(f_or_d):
            walkThroughDir(f_or_d, files)
        else:
            files.append(f_or_d)
    return files

def getEnvJsonsDic():
    '''
    #遍历脚本所在目录的evns子文件夹，返回包含所有配置文件的字典
    '''
    myPath = os.path.dirname(abspath(getsourcefile(lambda:0)))
    envsPath = os.path.join(myPath, 'envs')
    jsonFiles = []
    jsonFiles = walkThroughDir(envsPath, jsonFiles)
    jsonDic = {}
    index = 1
    for json in jsonFiles:
        jsonDic[str(index)] = json
        index += 1
    return jsonDic
    
def printMenu():
    '''
    #打印菜单项
    '''
    myPath = os.path.dirname(abspath(getsourcefile(lambda:0)))
    jsonDic = getEnvJsonsDic()
    print 
    print u'选项 :' + '\t' + u'选项说明(要使用的配置文件)'
    print '-----------------------------------------'
    for index in range(len(jsonDic)):
        print str(index+1) + ':' + '\t' + jsonDic[str(index+1)].replace(myPath, '')
    print '\n'
    print u'exit:' + '\t' + u'退出'
    return jsonDic

if __name__ == '__main__':
    myPath = os.path.dirname(abspath(getsourcefile(lambda:0)))
    jsonDic = printMenu()
    env = raw_input(u'>>>将测试环境切换至： '.encode(sys.stdout.encoding))
    env = env.strip()
    #处理无效选项
    while(not(env in jsonDic)):
        print u'Error：无效选项', '\n'
        env = raw_input(u'>>>将测试环境切换至： '.encode(sys.stdout.encoding))
        env = env.strip()
        if 'exit' == env.lower() or 0 == len(env):
            break 
    #有效选项   
    if 'exit' == env.lower() or 0 == len(env):
        pass
    else:  
        confJson = jsonDic[env]
        switchEvn(confJson)
        print '\n', u'自动化测试环境切换完成！'    

        
    
    










