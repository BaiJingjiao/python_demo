import paramiko

server = ''
user = ''
pwd = ''

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(server, username=user, password=pwd)
stdin, stdout, stderr = client.exec_command('ls -l')
# print stdin.read()
print stdout.read()
# print stderr.read()
