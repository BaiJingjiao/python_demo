# -*- coding:utf-8 -*-

import os
import re
import time
import sys
reload(sys)  
sys.setdefaultencoding('utf8')
import json

def parseLog(logfile):

    #将log内容存入logStr，变成字符串，以便之后使用正则操作
    with open(logfile) as f:
        log = f.readlines()
    logStr = ''
    for line in log:
        logStr = logStr + line   
    
    #解析logStr，得到用例名称，运行结果，及相关日志输出内容，存入reportDic
    reportDic = {}
    caseIP = ''
    caseName = ''
    caseResult = ''
    clearedLog = ''
    pIP = '.*[^\d](\d{1,3}\\.\d{1,3}\\.\d{1,3}\\.\d{1,3})_.*'
    mIP = re.search(pIP, logFile)
    if mIP:
        caseIP = mIP.groups()[0]
    p = '''Testcase <(.*)> Finished, Result is '(.*)'!'''
    m = re.search(p, logStr)
    if m:
        caseName = m.groups()[0]
        caseResult = m.groups()[1]

    clearedLog = re.sub('"linenumber":.*,"filepath":".*?",', '', logStr) 
    clearedLog = re.sub('"pathtype":".*","FragmentID":".*",', '', clearedLog)
    clearedLog = re.sub('\\\\"', '"', clearedLog)
    clearedLog = clearedLog.replace('\\/', '/')
#             self.log('clearedLog', clearedLog)
    reportDic['caseIP'] = caseIP
    reportDic['caseName'] = caseName
    reportDic['caseResult'] = caseResult
    reportDic['clearedLog'] = clearedLog
    return reportDic

def getFiles(mydir):
    sortedList = []
    for root, directory, files in os.walk(mydir):
        for file in files:
#             print(file)
            sortedList.append(file)
    sortedList = sorted(sortedList)
    return sortedList

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

def writeHtmlBeginForReport(reportName):
    html = ("<html>"
            + "<head>"
            + "<meta http-equiv=\"Content-Type\" content=\"text/html;charset=utf-8\" />"
            + "<link href=\"ecs.css\" rel=\"stylesheet\" type=\"text/css\">"
            + "</head>"
            + "<body>")
    tableHeader = ("<table class=\"resultTable\" cellspacing=\"0\">" 
            + "<tr bgcolor=\"SkyBlue\">"
            + "<th>执行机</th>" 
            + "<th>用例名称</th>" 
            + "<th>执行结果</th>" 
            + "</tr>")
    report = file(reportName, 'a+')
    report.write(html)
    report.write(tableHeader)
    report.close()

def writeHtmlBeginForExecutorInfo(executorInfoName):
    html = ("<html>"
            + "<head>"
            + "<meta http-equiv=\"Content-Type\" content=\"text/html;charset=utf-8\" />"
            + "<link href=\"ecs.css\" rel=\"stylesheet\" type=\"text/css\">"
            + "</head>"
            + "<body>")
    tableHeader = ("<table class=\"resultTable\" cellspacing=\"0\">" 
            + "<tr bgcolor=\"SkyBlue\">"
            + "<th>执行机</th>" 
            + "<th>执行用例数</th>" 
            + "</tr>")
    executorInfo = file(executorInfoName, 'a+')
    executorInfo.write(html)
    executorInfo.write(tableHeader)
    executorInfo.close()

def writeHtmlEndForReport(reportName):
    report = file(reportName, 'a+')
    endHtml = '</table></body></html>'
    report.write(endHtml)
    report.close()

def readJsonFile(jsonFile):
    f = open(jsonFile,'r')
    data = f.read()
    jsonDic = json.loads(data)
    return jsonDic

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

def ftpGet(server, localpath, remotepath):
    import paramiko
    client = sshConnect(server)
    sftp_handle = client.open_sftp()
    sftp_handle.get(remotepath, localpath)
    client.close()
    print 'get file [%s], and saved it to [%s]' % (remotepath, localpath)  

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

if __name__ == '__main__':
#     print(sys.stdout.encoding)
    #在10.171.218.107上执行/opt/mytools/create_6dian1_report.py
    #将生成的html文件从10.171.218.107传到windows本地
    server = {
          'host':'10.171.218.107',
          'port':22,
          'user':'root',
          'pwd':'huawei'
          }
    client = sshConnect(server)
    execCommand(client, 'cd /opt/mytools/;rm -rf *.html')
    execCommand(client, 'cd /opt/mytools/;python ./create_6dian1_report.py')
    stdin, ls_out, err = execCommand(client, 'cd /opt/mytools/;ls *.html')
    fileList = str(ls_out).split('\n')
    auto6dian1_report_fail = ''
    auto6dian1_report_pass = ''
    auto6dian1_executor_info = ''
    for name in fileList:
        if name.endswith('.html'):
            filename = name.encode(sys.stdout.encoding)
            localpath = 'D:\\api_automation_team\\auto6dian1_reports\\'+filename
            if filename.startswith('auto6dian1_report_fail'):
                auto6dian1_report_fail = name
            elif filename.startswith('auto6dian1_report_pass'):
                auto6dian1_report_pass = name
            else:
                auto6dian1_executor_info = name
            remotepath = '/opt/mytools/'+name
            ftpGet(server, localpath, remotepath) 
    #从auto6dian1_executor_info_xxxx-xx-xx_xx-xx-xx.html中，提取携带的数据
    from bs4 import BeautifulSoup
    mydata = ''
    with open(auto6dian1_executor_info) as f:
        lines = f.readlines()
    soup = BeautifulSoup(''.join(lines), 'lxml')
    passcount = soup.find('div', id="totalPassCases").string
    failcount = soup.find('div', id="totalFailCases").string
    svntotal = soup.find('div', id="svntotal").string
    executortotal = soup.find('div', id="executortotal").string
    executors = soup.find('div', id="executors").string
    
    #更新auto6dian1_executor_info，将svntotal和executortotal加进去
    html = open(auto6dian1_executor_info)
    soup = BeautifulSoup(html, 'html.parser')

    soup.find('th', {"id":"executors"}).string = '执行机-('+executors+')'
    soup.find('th', {"id":"cases"}).string = '执行用例数-('+executortotal+')'
    soup.find('th', {"id":"svncases"}).string = '用例列表(含SVN路径)-('+svntotal+')'
#     for i in soup.find('th', {"id":"executors"}).findChildren():
#         i.replace_with('##')
    soup.find('tr', {"class":"tabledata"})
    with open(auto6dian1_executor_info, "wb") as f_output:
        f_output.write(soup.prettify("utf-8")) 
    
    
    totalcount = int(passcount) + int(failcount)
    passrate = float(passcount)/totalcount
    passratestr = str(round(passrate*100, 2))+'%'  
    myindex = '''
                <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
                <html xmlns="http://www.w3.org/1999/xhtml">
                <head>
                    <title>基线6.1接口自动化用例执行报告</title>
                    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
                    <link href="mcr.css" rel="stylesheet" type="text/css">
                    <script type="text/javascript" src="jquery.js"></script>
                    <script type="text/javascript" src="mcr.js"></script>
                </head>
                <body>
                    <h1>基线6.1接口自动化用例执行报告(用例总数: '''+str(totalcount)+', 通过率: '+passratestr+''')</h1>
                
                <div class="tabs">
                    <ul class="tab-links">
                        <li class="active"><a id="failedli" href="#tab1">Failed('''+failcount+''')</a></li>
                        <li><a id="passedli" href="#tab3">Passed('''+passcount+''')</a></li>
                        <li><a id="allli" href="#tab4">执行机信息汇总</a></li>
                    </ul>
                
                    <div class="tab-content">
                        <div id="tab1" class="tab active">
                            <iframe id="iframe-failed" src="'''+auto6dian1_report_fail+'''"></iframe>
                        </div>
                
                        <div id="tab3" class="tab">
                            <iframe id="iframe-passed" src="'''+auto6dian1_report_pass+'''"></iframe>
                        </div>
                
                        <div id="tab4" class="tab">
                            <iframe id="iframe-all" src="'''+auto6dian1_executor_info+'''"></iframe>
                        </div>
                    </div>
                </div>
                
                </body>
                </html>
            '''
    try:
        os.remove('index.html')
    except:
        pass
    indexhtml  = file('index.html', 'a+')
    indexhtml.write(myindex)
