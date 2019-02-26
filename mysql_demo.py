# -*- coding:utf-8 -*- 
'''
Windows:
    pip install mysqlclient
Ubuntu 14, Ubuntu 16, Debian 8.6 (jessie)
	sudo apt-get install python-pip python-dev libmysqlclient-dev
Fedora 24:
	sudo dnf install python python-devel mysql-devel redhat-rpm-config gcc
Mac OS
	brew install mysql-connector-c
	if that fails, try

brew install mysql
''' 
class DBHelperMySQL:

	def __init__(self):
		pass

	def connect(self, server_dict):
		"""
		mysql_server_dict = {
			'host' : '',
			'user' : 'user',
			'passwd' : 'xxxxxx',
			'db' : 'thedbname',
			'port' : 3306,
			'charset' : 'utf8'
		}

		dbhelper = DBHelperMySQL()
		conn = dbhelper.connect(mysql_server_dict)
		"""
		import MySQLdb
		conn = MySQLdb.connect(**server_dict)
		return conn

if __name__ == "__main__":

	mysql_server_dict = {
		'host' : '',
		'user' : 'sse',
		'passwd' : 'Password',
		'db' : 'dbuser',
		'port' : 3306,
		'charset' : 'utf8'
	}

	mysql_server_dict = {
		'host' : '',
		'user' : 'dbuser',
		'passwd' : 'Password',
		'db' : 'acesp',
		'port' : 3306,
		'charset' : 'utf8'
	}

	dbhelper = DBHelperMySQL()
	conn = dbhelper.connect(mysql_server_dict)

	cursor = conn.cursor() 
	# cursor.execute("")
	# cursor.execute("commit") 
	rows = cursor.fetchall() 
	resultTuple = ()#将数据存元组里 
	for row in rows: 
		resultTuple = resultTuple + row 
	
	cursor.close() 
	conn.close() 
	    
	print(tuple(resultTuple))

