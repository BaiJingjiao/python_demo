import re
from HTMLParser import HTMLParser

fileName = 'escape_character_xml.xml'
htmlparser = HTMLParser()
regex = r'(&#\d+;)'

with open (fileName) as f:
    f = iter(f)
    for line in f:
        findList = re.findall(regex, line.strip())
        for item in findList:
            line = line.replace(item, htmlparser.unescape(item))
        print line
