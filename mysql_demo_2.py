from xxx.conf.xxx import *
import MySQLdb  
import time

mysqlConn = {'host' : mysqlDic.get('dbIp'),
              'user' : mysqlDic.get('dbName'),
              'passwd' : mysqlDic.get('dbPwd'),
              'db' : mysqlDic.get('db'),
              'port' : mysqlDic.get('port'),
              'charset' : 'utf8'
              }

class mysqlFun:
    def __init__(self, XXX):
        self.XXX = XXX
        return

    def insert_data(self, sql):
        conn = MySQLdb.connect(**mysqlConn)
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            conn.commit()
        finally:            
            cursor.close()
            conn.close() 	
