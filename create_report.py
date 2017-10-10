        import os
        import re
        import time
        import sys
        reload(sys)  
        sys.setdefaultencoding('utf8')
        import socket
        import paramiko
        
        #===========================================================
        # 使用D:\xCloud_ECS\ECM\tracelog\ECM001 日志文件
        # 提取svn下载的用例及其路径信息，写入文件
        #===========================================================
        def listCases(path, date=None):
            #确保D:\\mytools存在                
            mydir = 'D:\\mytools'
            if os.path.isdir(mydir):
                self.log('%s exist!' % (mydir))
            else:
                os.makedirs(mydir)
                self.log('%s created successfully' % (mydir))
            
            dateStr = ''
            if None == date:
                #使用当天时间
                dateStr = get_time_stamp(0,0,0,'%Y-%m-%d')
            else:
                dateStr = date
                     
            with open(path) as f:
                ecm001 = f.readlines()
            
            #得到排序后的用例列表
            cases = []
            for line in ecm001:
                m = re.search(r'^\['+dateStr+r' .*\].*INFO-http.*V600R006C10B999/Cases/SDV(.*).*\[.\\DownloadFromSVN\.cpp.*\]', line)
                if m:
                    self.log(  m.group(1) )
                    cases.append(m.group(1))
            cases = sorted(cases, reverse=True)
            
            #将结果写入文件,新生成文件保存结果，并保留原结果，便于对比
            myname = socket.getfqdn(socket.gethostname())
            myaddr = socket.gethostbyname(myname)
            timeStamp = get_time_stamp(0,0,0,'%Y-%m-%d_%H-%M-%S')
            filename = myaddr+'_cases_'+timeStamp+'.txt'
            filepath = os.path.join(mydir, filename)
            f = file(filepath, 'a+')
            #添加计数器，便于对比
            count = 0
            for case in cases:
                count = count + 1
                f.write(str(count) + '---' + case + '\n')
            f.close()
            return myaddr, filepath, filename
        
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
        
        def ftpGet(server, localpath, remotepath):
            print 'start getting file %s ...' % remotepath
            import paramiko
            client = sshConnect(server)
            sftp_handle = client.open_sftp()
            sftp_handle.get(remotepath, localpath)
            client.close()
            print 'finished getting file %s, and saved it to %s' % (remotepath, localpath)    
                
        def ftpPut(server, localpath, remotepath):
            self.log(  'start uploading file: %s to %s' % (localpath.decode(sys.stdout.encoding).encode('utf8'), remotepath))
            import paramiko
            client = sshConnect(server)
            sftp_handle = client.open_sftp()
            sftp_handle.put(localpath, remotepath, confirm = True)
            sftp_handle.close()
            client.close()   
            self.log( 'uploading file: %s finished' % (localpath.decode(sys.stdout.encoding).encode('utf8')) )
        
        def getLastModifiedFile(filenamePrefix):
            mydir = r'D:\\xCloud_ECS\\log'
            mydir = os.path.join('D:\\', 'xCloud_ECS', 'log')
            self.log(mydir)
            filePath = ""
            d = {}
            for root, directory, files in os.walk(mydir):
                for file in files:
                    file_utf8 = file.decode(sys.stdout.encoding).encode('utf8')
                    if file_utf8.startswith(filenamePrefix) :
                        filePath = os.path.join(mydir, file)
                        modifiedTime = datetime.datetime.fromtimestamp(
                                            float(os.path.getmtime(filePath))).strftime('%Y%m%d%H%M%S')
                        d[file_utf8] = modifiedTime

            sortedList = sorted(d.items(), key=lambda x: x[1], reverse=True)
            if 0 == len(sortedList):
                return 
            return os.path.join(mydir, sortedList[0][0])
        
        server = {
                  'host':'10.171.218.107',
                  'port':22,
                  'user':'root',
                  'pwd':'huawei'
                  }
        
        #生成用例列表       
        dateStr = get_time_stamp(0,0,0,'%Y-%m-%d')
        dateStr = '2017-09-30'
        myaddr = '10.171.218.107'
#         myaddr, filepath, filename = listCases(r'D:\xCloud_ECS\ECM\tracelog\ECM001.log', dateStr)
#         #ftp上传到10.171.218.107，/opt/cases_on_6dian1_executors/
#         remotepath = '/opt/cases_on_6dian1_executors/'+filename
#         ftpPut(server, filepath, remotepath)
        filepath = r'D:\\mytools\\10.162.158.245_cases_2017-10-09_11-45-15.txt'
        with open(filepath) as f:
            casesFullPath = f.readlines()
        
        name = ''
        for case in casesFullPath:
            m = re.search(r'.*/(.*)$', case)
            if m:
                name = m.group(1).decode(sys.stdout.encoding).encode('utf8')
                fileNamePrefix = name.strip() + '_' + dateStr
                logFile = getLastModifiedFile(fileNamePrefix)
                n = re.search(r'.*\\(.*)$', logFile)
                remoteName = ''
                if n:
                    remoteName = m.group(1).strip().decode(sys.stdout.encoding).encode('utf8')
                if None != logFile:
                    remotePath = os.path.join('/opt/cases_on_6dian1_executors/logs/' + myaddr + '_' + remoteName + '.txt')
                    ftpPut(server, logFile.decode('utf8').encode(sys.stdout.encoding), remotePath)
