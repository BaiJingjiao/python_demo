# -*- coding:utf-8 -*-
'''
instantclient-basic-win32-11.2.0.1.0.zip
将其路径加入系统变量Path
'''
import cx_Oracle
import pyodbc  

oracle_IP = '10.174.3.1'
oracle_PORT = '1521'
oracle_ACCOUNT = 'ecs_0725'
oracle_PWD = 'ecs_0725'
SID = 'eSpace' #数据库实例ora11g

#连接oracle数据库
Oracle_connect = oracle_ACCOUNT + '/'+ oracle_PWD +'@'+ oracle_IP +':' + oracle_PORT + '/' + SID
print Oracle_connect
conn = cx_Oracle.connect(Oracle_connect)

cursor = conn.cursor()
cursor.execute("select * from tbl_appid")
# cursor.execute("commit")
rows = cursor.fetchall()
resultTuple = ()#将数据存元组里
for row in rows:
    resultTuple = resultTuple + row

cursor.close()
conn.close()
    
print tuple(resultTuple) 
