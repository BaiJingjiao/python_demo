# -*- coding:utf-8 -*-
'''
#====================================================================================
#Copyright © Huawei Technologies Co., Ltd. Testing Tool Dept.
#====================================================================================
#   @Description:   Demo UseCase
#   @Author:        bwx433051 
#   @Date:  
#   @ModifyRecord:  
#====================================================================================
'''
from xCloudFrame import *
class xCloudTestCase(xCloudAutoFrame.TestCaseFrame):
    def Precondition(self):
        '''
        #====================================================================================
        #   @Method:  TestCase initialization
        #   @Param:
        #   @Return:   
        #   @ModifyRecord:  
        #====================================================================================
        '''     

        self.verificationErrors = []
        pass    


    def Procedure(self):
        '''
        #====================================================================================
        #   @Method:  Define the procedure of running TestCase in detail
        #   @Param:
        #   @Return:   
        #   @ModifyRecord:  
        #====================================================================================
        '''     
        import glob, os, stat
        import shutil
        import re
        import socket
        import time
        import sys
        reload(sys)  
        sys.setdefaultencoding('utf8')
        import paramiko
        
        def get_time_stamp(hour, min, sec, formatStr='%Y-%m-%d %X'):
            '''
                                产生自定义格式的时间戳
            %Y-%m-%d %X
            %Y/%m/%d %H:%M:%S.%f
            '''
            ISOTIMEFORMAT = formatStr        
            if 0 == hour and 0 == min and 0 == sec:
                stamp = time.strftime(ISOTIMEFORMAT)
            else:
                currentSecond = time.time() 
                newSecond = currentSecond + (hour*3600 + min*60 + sec)  
                stamp = time.strftime(ISOTIMEFORMAT, time.localtime(newSecond)) 
            return stamp
        
        def chmodDir(mydir):
            '''
            #将目录中所有文件，已经子目录含文件，都这是可删除的权限
            '''
            for root, dirs, files in os.walk(mydir):
                for file in files:
                    os.chmod(os.path.join(root, file), 420)
                for d in dirs:
                    os.chmod(os.path.join(root, d), 420)
                    chmodDir(d)
        
        def getLocalhostIP():
            myname = socket.getfqdn(socket.gethostname())
            myaddr = socket.gethostbyname(myname)
            return myaddr

        def sshConnect(server):
            host = str(server.get('host'))
            port = int(server.get('port')) 
            user = str(server.get('user'))
            pwd = str(server.get('pwd'))
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.load_system_host_keys()
            client.connect(host, port, user, pwd, timeout=10)
            return client

        def execCommand(client, command):
            print '$ %s' % command
            with open('log_file.txt', 'a') as f:
                f.write('\n' + get_time_stamp(0,0,0,'%Y-%m-%d_%H-%M-%S') + command + '\n')
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
                 
        dateStr = get_time_stamp(0,0,0,'%Y-%m-%d_%H-%M-%S')
        logDir = r'D:\\xCloud_ECS\\log' #执行结果日志目录
        ecm001Log = r'D:\xCloud_ECS\ECM\tracelog\\ECM001.log' #内含svn下载信息
        projectDir = r'D:\xCloud_ECS\Project' #工厂的用例下载目录
        bakDir = logDir + '_' + dateStr + '_bak'
        bakLog = ecm001Log + '_' + dateStr + '_bak'
        #备份D:\\xCloud_ECS\\log目录，直接重命名这个文件夹，这样新生成的log目录只包含最后一次运行结果，便于解析生成运行报告
        #备份D:\xCloud_ECS\ECM\tracelog\\ECM001.log，这样便于解析当天从svn下载执行的用例信息（含svn路径）
        #由于“失败重跑”，“一个用例跑多个环境”等因素，导致log目录下的log文件数多于实际用例数，所以还是有必要用svn下载信息来提取执行日志
        #但是用svn下载信息来提取执行日志，如果用例名称一样但路径不通，会导致提取的日志数量少（因log目录中没有路径信息）
        try:
            shutil.move(logDir, bakDir) 
            shutil.move(ecm001Log, bakLog)
        except:
            #没有相应文件就什么都不做
            pass
        #清理D:\xCloud_ECS\Project中的用例，从svn上重新checkout，保留目录内“非用例”的文件
        filesOrDirs = os.listdir(projectDir)
        for fdStr in filesOrDirs:
            fd = os.path.join(projectDir, fdStr)
            if os.path.isfile(fd):
                self.log('保留[%s]' % (fd))
            elif os.path.isdir(fd) and fdStr == '.settings':
                self.log('保留[%s]' % (fd))
            elif os.path.isdir(fd) and fdStr == 'backupLogFolder':
                pass
            else:
                chmodDir(fd)
                shutil.rmtree(fd)
        
        keepLogs = [get_time_stamp(0,0,0,'%Y-%m-%d'), 
                    get_time_stamp(-24,0,0,'%Y-%m-%d'),
                    get_time_stamp(-48,0,0,'%Y-%m-%d'),
                    get_time_stamp(-72,0,0,'%Y-%m-%d')]
        #清理D:\xCloud_ECS下面超过3天的备份log目录
        logbakDir = r'D:\\xCloud_ECS'
        logDirRegex = 'log_(\d{4}-\d{2}-\d{2}).*_bak'
        for fdStr in os.listdir(logbakDir):
            m = re.search(logDirRegex, fdStr)
            #找到所有log备份目录
            if m:
                bakDate = m.groups()[0]
                #如果不在保留目录中，删除
                if bakDate not in keepLogs:
                    dirneedremove = os.path.join(logbakDir, fdStr)
                    chmodDir(dirneedremove)
                    shutil.rmtree(dirneedremove)
                    self.log('删除备份目录[%s]' % (dirneedremove))
        #清理D:\xCloud_ECS\ECM\tracelog下面超过3天的ECM001.log备份
        ecm001Dir = r'D:\xCloud_ECS\ECM\tracelog'
        ecm001Regex = r'ECM001.*log_(\d{4}-\d{2}-\d{2}).*_bak'
        for ecm in os.listdir(ecm001Dir):
            m = re.search(ecm001Regex, ecm)
            #找到所有log备份目录
            if m:
                bakDate = m.groups()[0]
                #如果不在保留目录中，删除
                if bakDate not in keepLogs:
                    ecmneedremove = os.path.join(ecm001Dir, ecm)
                    os.chmod(ecmneedremove, 420)
                    os.remove(ecmneedremove)
                    self.log('删除备份ECM001.log[%s]' % (ecmneedremove))
        
        #清理10.171.218.107上【/opt/cases_on_6dian1_executors/logs】下的用例执行日志
        #清理10.171.218.107上【/opt/cases_on_6dian1_executors/】下的svn下载日志
        server = {
              'host':'10.171.218.107',
              'port':22,
              'user':'root',
              'pwd':'huawei'
              }
        thisIP = getLocalhostIP()
        #选了三台执行机，执行此操作（没必要每台都执行一遍，选三个是以防万一）
        if thisIP in ['10.171.217.123',  #基线6.1的执行机
                      '10.162.148.102',  #基线6.1的执行机
                      '10.162.159.168',  #基线6.1的执行机
                      '10.174.191.40',   #bwx433051的本地工作机
                      '10.186.229.158']: #bwx433051的手动执行机
            client = sshConnect(server)
            execCommand(client, 'cd /opt/cases_on_6dian1_executors/;rm -rf logs;mkdir logs')
            execCommand(client, 'cd /opt/cases_on_6dian1_executors/;rm -rf *.txt')
    
    def Postcondition(self):
        '''
        #====================================================================================
        #   @Method:  The cleanup procedure after running TestCase is finished
        #   @Param:
        #   @Return:   
        #   @ModifyRecord:  
        #====================================================================================
        '''     

        self.assertEqual([], self.verificationErrors)
        pass
    
    def Failure(self):
        '''
        #====================================================================================
        #   @Method:  The cleanup procedure after running TestCase is failure
        #   @Param:
        #   @Return:   
        #   @ModifyRecord:  
        #====================================================================================
        '''    
        pass  
