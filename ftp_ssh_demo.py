import ftplib
filename = "eServer.log"
ftp = ftplib.FTP("10.174.3.1")
ftp.login("ecs", "ecs@123")
ftp.cwd("/home/ecs/20140925/Logs/MAA")
ftp.retrbinary('RETR %s' % filename, open('myoutputfile.txt', 'wb').write)

ftp.storbinary('STOR %s' % 'ddd.py', open('ddd.py', 'r'), blocksize=1024)

# import base64
import paramiko
# key = paramiko.RSAKey(data=base64.b64decode(b'AAA...'))
client = paramiko.SSHClient()
# client.get_host_keys().add('10.174.3.1', 'ssh-rsa', key)
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('10.174.3.1', username='ecs', password='ecs@123')
stdin, stdout, stderr = client.exec_command('ls')
for line in stdout:
    print('... ' + line.strip('\n'))
client.close()
