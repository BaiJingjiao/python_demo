#!D:\xCloud_ECS\executor\Python27
#-*- coding: utf-8 -*-

import argparse
import subprocess
import os
import os.path
import shutil
import re
import time
from pprint import pprint
from inspect import getsourcefile
from os.path import abspath
import sys

def clearFolder(dir):
    isExists = os.path.exists(dir)
    if True == isExists:
        shutil.rmtree(dir)
    time.sleep(1)
    os.mkdir(dir)

def deleteFolder(dir):
    isExists = os.path.exists(dir)
    if True == isExists:
        shutil.rmtree(dir)
    time.sleep(1)

def getPyFileList(fileDir):
    fileList = []
    for root, dirs, files in os.walk(fileDir):
        for file in files:
            if file.endswith('.py'):
                fileList.append(file)
        return fileList

def python_call_powershell(ip, shellFile):
    try:
        args=[r"C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe","-ExecutionPolicy","Unrestricted", shellFile,ip]
        p=subprocess.Popen(args, stdout=subprocess.PIPE)
        dt=p.stdout.read()
        return dt
    except Exception,e:
        print e
    return False

def main():
    #找到MTG生成的脚本文件（py文件）
    dirUserOutput = r'C:\TestTools\MTG for EA\UserOutput'
    dirList = []
    for s in os.listdir(dirUserOutput):
        if os.path.isdir(os.path.join(dirUserOutput,s)):
            dirList.append(s)
    newestDirOfModel = [(x[0], time.ctime(x[1].st_ctime)) for x in sorted([(fn, os.stat(os.path.join(dirUserOutput, fn))) for fn in dirList], key = lambda x: x[1].st_ctime)][-1][0]
    srcDir = os.path.join(dirUserOutput, newestDirOfModel, "xCloud", "tc")
    fileList = getPyFileList(srcDir)
    
    #解析出MTG的Source_Dir和Destination_Dir并清空
    myPath = os.path.dirname(abspath(getsourcefile(lambda:0)))
    shellFile = os.path.join(myPath, 'copyAndRename.bat')
    with open(shellFile) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    regex_src = '.*Source_Dir=(.*)'
    regex_dest = '.*Destination_Dir=(.*)'
    Source_Dir_MTG = None
    Destination_Dir_MTG = None
    for line in content:
        src = re.search(regex_src, line.strip())
        dest = re.search(regex_dest, line.strip())
        if src:
            Source_Dir_MTG = src.group(1)
        if dest:
            Destination_Dir_MTG =  dest.group(1)

    clearFolder(Source_Dir_MTG)
    clearFolder(Destination_Dir_MTG)
    
    #将MTG生成的py文件copy到Source_Dir_MTG
    for file in fileList:
        theFile = os.path.join(srcDir, file)
        destfile = os.path.join(Source_Dir_MTG, os.path.basename(file))
        shutil.copyfile(theFile, destfile)
    
    #执行D:\MTG\copyAndRename.bat
    python_call_powershell('127.0.0.1', shellFile)
    
    #将Destination_Dir_MTG中的文件夹copy到xCloud的工程目录targetDir
#     xcloudDestDir = r'D:\xCloud_ECS\desktop_data\project\ECS\Mydemo'
    xcloudDestDir = os.getcwd()
    targetDir = os.path.join(xcloudDestDir, newestDirOfModel)
    deleteFolder(targetDir)
    shutil.copytree(Destination_Dir_MTG, targetDir)
    print '脚本已拷贝至'.decode('utf-8'), targetDir

if __name__ == '__main__':
    main()
