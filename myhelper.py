#-*- coding: utf-8 -*-

class MyHelper:

    def get_timestamp(self, hour=0, min=0, sec=0, format=None):
        '''
        helper = MyHelper()
        helper.get_timestamp() #1513665702.0115976
        helper.get_timestamp(format='%Y-%m-%d %H:%M:%S %z') #2017-12-19 14:48:23 +0800

        '''
        seconds = time.time()
        new_seconds = seconds + (hour*3600 + min*60 + sec) 
        if format == None:
            return new_seconds
        else:
            return time.strftime(format, time.localtime(new_seconds))

    def get_combinations(self, option_values_list, num):
        import itertools

        ls = itertools.combinations(option_values_list, num)
         
        #遍历所有组合情况
        for item in ls:
            print(item)

    def get_ssh_connect(self, server_dic):
        '''
        server_dic = {
            'host':'xxx.xxx.xxx.xxx',
            'port':'22',
            'user':'xxx',
            'pwd':'xxxxxxx'
        }
        client = helper.get_ssh_connect(server_dic)
        '''
        import paramiko
        host = str(server_dic.get('host'))
        port = int(server_dic.get('port')) 
        user = str(server_dic.get('user'))
        pwd = str(server_dic.get('pwd'))
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(host, port, user, pwd, timeout=5)
        return client

    def exec_command(self, client, command):
        '''
        server_dic = {
            'host':'xxx.xxx.xxx.xxx',
            'port':'22',
            'user':'xxx',
            'pwd':'xxxxxxx'
        }
        client = helper.get_ssh_connect(server_dic)
        stdin, stdout, stderr = helper.exec_command(client, 'date')
        '''
        stdin, stdout, stderr = client.exec_command(command)
        # out = stdout.read().strip()
        # err = stderr.read().strip()
        out = stdout.readlines()
        err = stderr.readlines()
        return stdin, out, err

    def do_ftp_get(self, client, localpath, remotepath):
        '''
        server_dic = {
            'host':'xxx.xxx.xxx.xxx',
            'port':'22',
            'user':'root',
            'pwd':'xxxxxxxx'
        }
        client = helper.get_ssh_connect(server_dic)
        helper.do_ftp_get(client, 'D:\\xxx\\yyy\\zzz.log', '/opt/zzz.log')
        '''
        print('start getting file %s ...' % remotepath)
        sftp_handle = client.open_sftp()
        sftp_handle.get(remotepath, localpath)
        print('finished getting file %s, and saved it to %s' % (remotepath, localpath))

    def do_ftp_put(self, client, localpath, remotepath):
        '''
        server_dic = {
            'host':'xxx.xxx.xxx.xxx',
            'port':'22',
            'user':'root',
            'pwd':'xxxxxxxx'
        }
        client = helper.get_ssh_connect(server_dic)
        helper.do_ftp_put(client, 'D:\\xxx\\yyy\\zzz.log', '/opt/zzz.log')
        '''
        print('start uploading file: %s to %s' % (localpath, remotepath))
        sftp_handle = client.open_sftp()
        sftp_handle.put(localpath, remotepath, confirm = True)
        sftp_handle.close()
        print('uploading file: %s finished' % localpath)

    def is_windows(self):
        import platform
        sysstr = platform.system()
        if(sysstr =="Windows"):
            return True
        else:
            return False

    def mkdir_p(self, path):
        import os, errno
        try:
            os.makedirs(path)
        except OSError as exc: # Python >2.5 (except OSError, exc: for Python <2.5)
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise

    def do_character_escapes_for_regex(self, str):
        import re
        chars = [ "$", "^", "{", "{", "[", "]", "(", ")", "|", "*", "+", "?"]
        str_for_regex = str
        for char in chars:
            try:
                str_for_regex = re.sub('\\%s' % (char), '\\\\%s' % (char), str_for_regex)
            except Exception as err:
                print('char', char)
                print('str_for_regex', str_for_regex)
                raise
        return str_for_regex

    def do_ftp_getdir(self, server_dic, local_dir, remote_dir):
        """
        helper = MyHelper()
        server_dic = {
            'host':'xxx.xxx.xxx.xxx',
            'port':'22',
            'user':'xxx',
            'pwd':'yyyyyy'
        }
        helper.do_scp_getdir(server_dic, 
            "D:\\mytools\\python-things\\pydemos\\mysuite\\temp", 
            "/usr1/xxx/yyyyy/zzzz")
        """
        import paramiko
        import os
        import re

        # 递归函数遍历目录
        # shellstr = """function read_dir() { for file in `ls $1`; do if [ -d $1"/"$file ]; then read_dir $1"/"$file; else echo $1"/"$file; fi; done; }; read_dir """ + remote_dir
        
        #打印非目录类型的文件，包括链接文件等
        shellstr = "find " + remote_dir + " ! -type d"

        host = str(server_dic.get('host'))
        port = int(server_dic.get('port')) 
        user = str(server_dic.get('user'))
        pwd = str(server_dic.get('pwd'))
        port = 22

        client = self.get_ssh_connect(server_dic)
        stdin, stdout, stderr = self.exec_command(client, shellstr)

        t = paramiko.Transport((host,port))
        t.connect(username=user,password=pwd)
        sftp = paramiko.SFTPClient.from_transport(t)
        # files = sftp.listdir(remote_dir) #这个不包含子目录
        # 处理多层嵌套目录
        for f in stdout:
            remote_file = f.strip()
            filename = os.path.basename(f).strip('\n')
            regex = remote_dir+'(.*)/'+self.do_character_escapes_for_regex(filename)+'$'
            m = re.search(regex, remote_file)
            path = None
            if m:
                path = m.groups()[0]
            else:
                print('regex', regex)
                print('remote_file', remote_file)
            ld = local_dir
            for d in path.split('/'):
                ld = os.path.join(ld, d)
            self.mkdir_p(ld)
            local_file = os.path.join(ld, filename)
            sftp.get(remote_file, local_file)
        t.close()


    def do_ftp_putdir(self, server_dic, local_dir, remote_dir):
        """
        helper.do_ftp_putdir(server_dic_xxxxxx, 
            'D:\\mytools\\python-things\\pydemos\\mysuite\\temp', 
            '/usr1/xxxxxx/bjjtemp')
        """
        import paramiko
        import os
        import re

        host = str(server_dic.get('host'))
        port = int(server_dic.get('port')) 
        user = str(server_dic.get('user'))
        pwd = str(server_dic.get('pwd'))
        port = 22

        client = self.get_ssh_connect(server_dic)

        fileList = []
        self.get_all_files(local_dir, fileList)
        local_dir = re.sub(r'\\', r'/', r'%s' % (local_dir))

        t = paramiko.Transport((host,port))
        t.connect(username=user,password=pwd)
        sftp = paramiko.SFTPClient.from_transport(t)
        # 处理多层嵌套目录
        for f in fileList:
            local_file = re.sub(r'\\', r'/', r'%s' % (f))
            filename = os.path.basename(f).strip('\n')
            regex = local_dir+'(.*)/'+self.do_character_escapes_for_regex(filename)+'$'
            m = re.search(regex, r'%s' % local_file)
            path = None
            if m:
                path = m.groups()[0]
            rd = remote_dir
            for d in path.split('/'):
                rd = os.path.join(rd, d)
            rd = re.sub(r'\\', r'/', r'%s' % (rd))
            # 在远程创建目录结构
            shellstr = 'mkdir -p %s' % (rd)
            # print('shellstr', shellstr)
            stdin, stdout, stderr = self.exec_command(client, shellstr)
            remote_file = os.path.join(rd, filename)
            remote_file = re.sub(r'\\', r'/', r'%s' % (remote_file))
            sftp.put(local_file, remote_file)
        t.close()


    def get_local_hostname(self):
        '''
        helper = MyHelper()
        hostname = helper.get_local_hostname()
        '''
        import socket
        myname = socket.getfqdn(socket.gethostname())
        return myname

    def get_local_ip(self):
        '''
        helper = MyHelper()
        ip = helper.get_local_ip()
        '''
        import socket
        myname = self.get_local_hostname()
        myaddr = socket.gethostbyname(myname)
        return myaddr

    def get_all_files(self, mydir, fileList):
        """
        helper = MyHelper()
        fileList = []
        helper.get_all_files(mydir, fileList)
        """
        import os
        for root, dirs, files in os.walk(mydir):
            for file in files:
                fileList.append(os.path.join(root, file))
            for d in dirs:
                self.get_all_files(d, fileList)

    def merge_two_lists(self, list1, list2):
        '''
        helper = MyHelper()
        list1 = ['aaa', 'ddd', 'fff', 'ggg']
        list2 = ['bbb', 'ggg', 'xxx', 'hhh']
        list3 = helper.merge_two_lists(list1, list2)
        print(list3) 
        输出结果：['hhh', 'xxx', 'ddd', 'fff', 'ggg', 'aaa', 'bbb']
        '''
        list_sum = sum([list1, list2], [])
        return list(set(list_sum))

    def chmod_dir(self, mydir):
        '''
        将目录中所有文件（含子目录），都设置成可删除的权限
        '''
        import os
        for root, dirs, files in os.walk(mydir):
            for file in files:
                os.chmod(os.path.join(root, file), 420)
            for d in dirs:
                os.chmod(os.path.join(root, d), 420)
                chmodDir(d)

    def print_json(self, json_str):
        '''
        按json格式在控制台打印字符串
        '''
        import json
        print(json.dumps(json_str, indent=4))

    def get_last_modified_file(self, mydir, filenamePrefix):
        filePath = ""
        d = {}
        for root, directory, files in os.walk(mydir):
            for file in files:
                file_utf8 = file.decode(sys.stdout.encoding).encode('utf8')
                if file_utf8.startswith(filenamePrefix) :
                    filePath = os.path.join(mydir, file)
                    from datetime import datetime
                    modifiedTime = datetime.fromtimestamp(
                                        float(os.path.getmtime(filePath))).strftime('%Y%m%d%H%M%S')
                    d[file_utf8] = modifiedTime

        sortedList = sorted(d.items(), key=lambda x: x[1], reverse=True)
        if 0 == len(sortedList):
            return 
        return os.path.join(mydir, sortedList[0][0])


if __name__ == '__main__':
    helper = MyHelper()

    server_dic_xxxxxx = {
        'host':'xxx.xxx.xxx.xxx',
        'port':'22',
        'user':'xxxxxx',
        'pwd':'xxxxxx@123'
    }

    server_dic_mysql = {
        'host':'xxx.xxx.xxx.xxx',
        'port':'22',
        'user':'root',
        'pwd':'xxxxxx'
    }

    # helper.do_ftp_getdir(server_dic_xxxxxx, 'D:\\mytools\\python-things\\pydemos\\mysuite\\temp', '/usr1/xxxxxx/20140925/Logs')

    # helper.do_ftp_putdir(server_dic_xxxxxx, 
    #     'D:\\mytools\\python-things\\pydemos\\mysuite\\temp', 
    #     '/usr1/xxxxxx/bjjtemp')
    # import re
    # local_file = '^D:\\mytools\\python-things\\pydemos\mysuite\\temp\\AppAgent\\AppAgent.log$'
    # # local_file = 'mytools\\python-things\\pydemos\mysuite\\temp'
    # local_file_for_re = re.sub(r'\\', r'\\\\', r'%s' % (local_file))
    # print(local_file_for_re)

    # time.time()
    # # print('time.gmtime()', time.gmtime())
    # dt = "2016-05-05 20:28:54"
    # #转换成时间数组
    # timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    # #转换成时间戳
    # timestamp = time.mktime(timeArray)
    # print(timeArray)
    # print(timestamp)
    # print(time.time())
    # dt = datetime.datetime.now()
    # timestamp = pytz.timezone('Asia/Shanghai').localize(dt)
    # print(dt)
    # print(pytz.country_names)
    # for key in pytz.country_names:
    # #     print(pytz.country_names[key])
    # mydir = 'D:\\mytools\\python-things\\pydemos\\MAA业务接口' # windows中文路径编码处理
    # print(mydir)
    # helper.chmod_dir(mydir)

    # helper.do_invoke_shell(server_dic_xxxxxx)


  


