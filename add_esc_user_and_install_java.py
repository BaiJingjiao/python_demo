#-*- coding: utf-8 -*-

'''
'''
import fileinput
import json
import os.path
import subprocess
from os.path import abspath
from inspect import getsourcefile
import re
import xml.etree.ElementTree as ET #用它修改后的xml，注释丢失
from datetime import datetime
from datetime import timedelta
import sys
reload(sys)  
sys.setdefaultencoding('utf8')

def getConfItems(confJson):
    myPath = os.path.dirname(abspath(getsourcefile(lambda:0)))
    f = open(os.path.join(myPath, 'conf', confJson),'r')
    data = f.read()
    jsonObj = json.loads(data)
    return jsonObj

def sshConnect_origin(host, port, user, pwd):
    import paramiko
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(host, port, user, pwd, timeout=10)
    return client

def sshConnect(server):
    import paramiko
    host = str(server.get('host'))
    port = int(server.get('port')) 
    user = str(server.get('user'))
    pwd = str(server.get('pwd'))
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(host, port, user, pwd, timeout=10)
    return client

def getLogStamp():
    '''
    '%Y-%m-%d %H.%M.%S.%f'
    '''
    now = datetime.today()
    mytime = datetime.strftime(now, '%Y-%m-%d %H.%M.%S')
    stamp = '['+mytime+'] '
    return stamp

def execCommand(client, command):
    print '$ %s' % command
    with open('log_file.txt', 'a') as f:
        f.write('\n' + getLogStamp() + command + '\n')
    stdin, stdout, stderr = client.exec_command(command)
    out = stdout.read().strip()
    err = stderr.read().strip()
    if 0 != len(out):
        print out
        with open('log_file.txt', 'a') as f:
            f.write(out)
    if 0 != len(err):
        print 'Error: ', err
        with open('log_file.txt', 'a') as f:
            f.write(err)
        stderr.flush()
    return stdin, out, err

def ftpGet(server, localpath, remotepath):
    print 'start getting file %s ...' % remotepath
    import paramiko
    client = sshConnect(server)
    sftp_handle = client.open_sftp()
    sftp_handle.get(remotepath, localpath)
    client.close()
    print 'finished getting file %s, and saved it to %s' % (remotepath, localpath)

def ftpPut(server, localpath, remotepath):
    print 'start uploading file: %s to %s' % (localpath, remotepath)
    import paramiko
    client = sshConnect(server)
    sftp_handle = client.open_sftp()
    sftp_handle.put(localpath, remotepath, confirm = True)
    sftp_handle.close()
    client.close()   
    print 'uploading file: %s finished' % localpath 

def getRandomNum(length):
    import string
    import random
    chars=string.digits
    myrandom = ''.join(random.choice(chars) for _ in range(length))
    return myrandom

def addUser_ecs_install_java(server):
    client = sshConnect(server)
    userhome = '/data01/home/ecs'
    execCommand(client, 'useradd ecs')
    execCommand(client, 'echo "ecs:ecs@123" | chpasswd')
    execCommand(client, 'mkdir -p '+userhome)
    execCommand(client, 'usermod -d '+userhome+' ecs')
    execCommand(client, 'chown -R ecs '+userhome)
    ftpPut(server, './files_need_upload/jdk-7u80-linux-x64.gz', userhome+'/jdk-7u80-linux-x64.gz')
    execCommand(client, 'cd '+userhome + ';tar xvf ./jdk-7u80-linux-x64.gz')
    javaHome = 'JAVA_HOME=' + userhome + '/jdk1.7.0_80;'
    javaBin = 'PATH=$JAVA_HOME/bin:$PATH;'
    javaJre = 'JRE_HOME=$JAVA_HOME/jre;'
    execCommand(client, 'echo "'+javaHome+'" >> /etc/profile')
    execCommand(client, 'echo "'+javaBin+'" >> /etc/profile')
    execCommand(client, 'echo "'+javaJre+'" >> /etc/profile')
    execCommand(client, 'source /etc/profile')
    execCommand(client, 'java -version')
    client.close()
    #验证结果
    client = sshConnect_origin(server.get('host'), int(server.get('port')), 'ecs', 'ecs@123')
    stdin, out, err = execCommand(client, 'pwd')
    if userhome != out:
        raise Exception('用户或家目录创建不成功！'.encode(sys.stdout.encoding))
    else:
        print '用户：ecs 添加成功！家目录：'.encode(sys.stdout.encoding) + userhome
    stdin, out, err = execCommand(client, 'java -version')
    #不知为何，java -version 输出到了stderr
    if 0 == err.find('java version "1.7.0_80"'):
        print 'Java 安装成功！'.encode(sys.stdout.encoding)
    else:
        raise Exception('Java安装失败！'.encode(sys.stdout.encoding))
   
if __name__ == '__main__':
    jsonObj = getConfItems('uc.json')
    for servername in jsonObj:
        print '-------------------------------------------------------------------------------'
        server = jsonObj.get(servername)
        addUser_ecs_install_java(server)

