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
#     clearedLog = re.sub('"module":".*","level":".*",', '', clearedLog)
    reportDic['caseIP'] = caseIP
    reportDic['caseName'] = caseName
    reportDic['caseResult'] = caseResult
    reportDic['clearedLog'] = clearedLog
    return reportDic

def getFiles(mydir):
    sortedList = []
    for root, directory, files in os.walk(mydir, topdown=False):
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

def getRandomNum(length):
    import string
    import random
    chars=string.digits
    myrandom = ''.join(random.choice(chars) for _ in range(length))
    return myrandom

def writeHtmlBeginForReport(reportName):
    html = ("<html>"
            + "<head>"
            + "<meta http-equiv=\"Content-Type\" content=\"text/html;charset=utf-8\" />"
            + "<link href=\"ecs.css\" rel=\"stylesheet\" type=\"text/css\">"
            + "</head>"
            + "<body>")
    tableHeader = ("<table class=\"resultTable\" cellspacing=\"0\" border=\"1\">" 
            + "<tr bgcolor=\"SkyBlue\">"
            + "<th>执行机</th>" 
            + "<th>用例名称</th>" 
            + "<th>执行结果</th>" 
            + "<th>控制台输出</th>" 
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
    tableHeader = ("<table class=\"resultTable\" cellspacing=\"0\" border=\"1\">" 
            + "<tr bgcolor=\"SkyBlue\" class=\"tableheader\">"
            + "<th id=\"executors\">执行机</th>" 
            + "<th id=\"cases\">执行用例数</th>" 
            + "<th id=\"svncases\">用例列表(含SVN路径)</th>" 
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
#     print 'start getting file %s ...' % remotepath
    import paramiko
    client = sshConnect(server)
    sftp_handle = client.open_sftp()
    sftp_handle.get(remotepath, localpath)
    client.close()
#     print 'finished getting file %s, and saved it to %s' % (remotepath, localpath)  

def execCommand(client, command):
    print '$ %s' % command
    with open('log_file.txt', 'a') as f:
        f.write('\n' + get_time_stamp(0,0,0,'%Y-%m-%d_%H-%M-%S') + command + '\n')
    stdin, stdout, stderr = client.exec_command(command)
    out = stdout.read().strip()
    err = stderr.read().strip()
    if 0 != len(out):
#         print out
        with open('log_file.txt', 'a') as f:
            f.write(out)
    if 0 != len(err):
#         print 'Error: ', err
        with open('log_file.txt', 'a') as f:
            f.write(err)
        stderr.flush()
    return stdin, out, err

if __name__ == '__main__':
#     #将log文件从10.171.218.107传到windows本地（耗时需一小时15分钟，太久了，放弃这样做。
#     server = {
#           'host':'10.171.218.107',
#           'port':22,
#           'user':'root',
#           'pwd':'huawei'
#           }
#     client = sshConnect(server)
#     stdin, out, err = execCommand(client, 'cd /opt/cases_on_6dian1_executors/logs;ls')
#     fileList = str(out).split('\n')
#     print len(fileList)
#     for file in fileList:
#         filename = file.encode(sys.stdout.encoding)
#         localpath = 'D:\\mytools\\logs\\'+filename
#         remotepath = '/opt/cases_on_6dian1_executors/logs/'+file
#         ftpGet(server, localpath, remotepath)
    executorCasesDic = {} #用来记录各执行机用例数，以便核对
    executorNameDic = readJsonFile('executors_6dian1.json')
    for key in executorNameDic:
        executorCasesDic[key] = 0 #初始化
    #产生运行报告名称（按时间戳）
    dateStr = get_time_stamp(0,0,0,'%Y-%m-%d_%H-%M-%S')
    reportNamePass  = 'auto6dian1_report_pass_' + dateStr + '.html'
    reportNameFail  = 'auto6dian1_report_fail_' + dateStr + '.html'
    writeHtmlBeginForReport(reportNamePass)
    writeHtmlBeginForReport(reportNameFail)
    reportPass = file(reportNamePass, 'a+') 
    reportFail = file(reportNameFail, 'a+') 
#     mydir = 'D:\\mytools\\logs'
    mydir = '/opt/cases_on_6dian1_executors/logs'
    logFiles = getFiles(mydir)
    totalCases = 0
    totalPassCases = 0
    totalFailCases = 0
    for logFile in logFiles:
        logFile = os.path.join(mydir, logFile)
        reportDic = parseLog(logFile)
        caseIPTd = '<td class="">'+executorNameDic[reportDic['caseIP']]+'-'+reportDic['caseIP']+'</td>'
        caseNameTd = '<td class="">'+reportDic['caseName']+'</td>'
        caseResultTd = '<td class="">'+reportDic['caseResult']+'</td>'
        divid = get_time_stamp(0,0,0,'%Y%m%d%H%M%S') + getRandomNum(3)
        clearedLogTd = ('<td class="">'
                        +'<a class="" href="#'+divid+'">log</a>'
                        +'<div id="'+divid+'" class="overlay">'
                        +    '<div class="popup">'
                        +        '<h2>console</h2>'
                        +        '<a class="close" href="#">&times;</a>'
                        +        '<div class="content"><pre>'+reportDic['clearedLog']+'</pre></div>'
                        +    '</div>'
                        +'</div>'
                        +'</td>')
        caseTr = ("<tr class=\"tabledata\">" 
                  + caseIPTd 
                  + caseNameTd 
                  + caseResultTd 
                  + clearedLogTd #要做成链接，点击才显示console内容
                  + "</tr>")
        if 'pass' == reportDic['caseResult']:
            reportPass.write(caseTr)
            totalPassCases += 1 #统计通过用例数
        elif 'failed' == reportDic['caseResult']: #这样顺便把空白行滤掉了
            reportFail.write(caseTr)
            totalFailCases += 1 #统计失败用例数
 
        try:
            executorCasesDic[reportDic['caseIP']] += 1
        except:
            print reportDic['caseIP']
    else:
        endHtml = '</table></body></html>'
        reportFail.write(endHtml)
        reportFail.close()
        reportPass.write(endHtml)
        reportPass.close()
        '''
#         这几句，直接在Linux上执行，没有问题，但远程调用时encode(sys.stdout.encoding)报错
#         print('用例总数: '.encode(sys.stdout.encoding) + str(totalPassCases+totalFailCases))
#         print('通过用例数: '.encode(sys.stdout.encoding) + str(totalPassCases))
#         print('失败用例数: '.encode(sys.stdout.encoding) + str(totalFailCases))
        '''
        print('total: ' + str(totalPassCases+totalFailCases))
        print('Pass: ' + str(totalPassCases))
        print('Fail: ' + str(totalFailCases))
        '''
        #统计单个执行机执行用例数，便于比对
        '''
        svnlogdir = '/opt/cases_on_6dian1_executors/'
        svnlogs = os.listdir(svnlogdir)
        ipregex = '.*[^\d](\d{1,3}\\.\d{1,3}\\.\d{1,3}\\.\d{1,3}).*'
        def findSVNLog(ip):
            logStr = ''
            svncasesnum = 0
            for svnlog in svnlogs:
                if svnlog.startswith(ip):
                    with open(os.path.join(svnlogdir, svnlog)) as f:
                        lines = f.readlines()
                    logStr = ''
                    svncasesnum = len(lines)
                    for line in lines:
                        logStr = logStr + line
                    return logStr, svncasesnum
            return logStr, svncasesnum
        
        d = {}
        for key in executorCasesDic:
            d[executorNameDic[key]+'-'+key] = executorCasesDic[key]
        sortedList = sorted(d.items(), key=lambda x: x[0], reverse=True) #对字典排序
        executorInfoName = 'auto6dian1_executor_info_' + dateStr + '.html'
        writeHtmlBeginForExecutorInfo(executorInfoName)
        executorInfo = file(executorInfoName, 'a+')
        svntotal = 0
        executortotal = 0
        for index in range(len(sortedList)):
            executorTd = '<td class="">'+str(sortedList[index][0])+'</td>'
            theip = re.search(ipregex, executorTd).groups()[0]
            svnlog, num = findSVNLog(theip)
            svntotal = svntotal + num
            if None == svnlog:
                print(theip)
                continue
            casesNumTd = '<td class="executorcases">'+str(sortedList[index][1])+'</td>'
            executortotal = executortotal + sortedList[index][1]
            dividsvnpath = get_time_stamp(0,0,0,'%Y%m%d%H%M%S') + getRandomNum(3)
            if num == sortedList[index][1]:
                svnpath = ('<td class="svncases">'
                                +'<a class="" href="#'+dividsvnpath+'">用例列表('+str(num)+')</a>'
                                +'<div id="'+dividsvnpath+'" class="overlay">'
                                +    '<div class="popup">'
                                +        '<h2>console</h2>'
                                +        '<a class="close" href="#">&times;</a>'
                                +        '<div class="content"><pre>'+svnlog.decode('cp936').encode('utf8')+'</pre></div>'
                                +    '</div>'
                                +'</div>'
                                +'</td>')
            else:
                svnpath = ('<td class="svncases">'
                                +'<a class="dupcasename" href="#'+dividsvnpath+'">用例列表('+str(num)+')</a>'
                                +'<div id="'+dividsvnpath+'" class="overlay">'
                                +    '<div class="popup">'
                                +        '<h2>console</h2>'
                                +        '<a class="close" href="#">&times;</a>'
                                +        '<div class="content"><pre>'+svnlog.decode('cp936').encode('utf8')+'</pre></div>'
                                +    '</div>'
                                +'</div>'
                                +'</td>')                
            caseTr = ("<tr class=\"tabledata\">" 
                      + executorTd 
                      + casesNumTd 
                      + svnpath 
                      + "</tr>")
            executorInfo.write(caseTr)
        else:
            executorInfo.write('</table>')
            executorInfo.write('<div id="totalPassCases" class="data" style="display:none;">'+str(totalPassCases)+'</div>')
            executorInfo.write('<div id="totalFailCases" class="data" style="display:none;">'+str(totalFailCases)+'</div>')
            executorInfo.write('<div id="svntotal" class="data" style="display:none;">'+str(svntotal)+'</div>')
            executorInfo.write('<div id="executortotal" class="data" style="display:none;">'+str(executortotal)+'</div>')
            executorInfo.write('<div id="executors" class="data" style="display:none;">'+str(len(executorNameDic))+'</div>')
            executorInfo.write('</body></html>')
            executorInfo.close()
