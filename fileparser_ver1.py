import re

with open('copyAndRename.bat') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]

Source_Dir = None
Destination_Dir = None
regex_src = '.*Source_Dir=(.*)'
regex_dest = '.*Destination_Dir=(.*)'
for line in content:
    src = re.search(regex_src, line.strip())
    dest = re.search(regex_dest, line.strip())
    if src:
        Source_Dir = src.group(1)
    if dest:
        Destination_Dir =  dest.group(1)

print 'Source_Dir:', Source_Dir
print 'Destination_Dir:', Destination_Dir
