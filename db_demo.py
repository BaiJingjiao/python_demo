from XXX.sql.oracle_fun import *
from XXX.sql.mysql_fun import *
from XXX.sql.sqlserver_fun import *

if 'oracle' == sqlType:
    class sqlOpr(oracleFun):
        def __init__(self, XXX):
            self.XXX = XXX
            self.XXX.XXX('db is oracle.')
            return
elif 'mysql' == sqlType:
    class sqlOpr(mysqlFun):
        def __init__(self, XXX):
            self.XXX = XXX
            self.XXX.XXX('db is mysql.')
            return
elif 'sqlServer' == sqlType:
    class sqlOpr(sqlServerFun):
        def __init__(self, XXX):
            self.XXX = XXX
            self.XXX.XXX('db is sqlServer.')
            return
else:
    self.XXX.XXX('todo...')
    pass
