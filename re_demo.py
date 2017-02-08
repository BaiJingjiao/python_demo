#-*- coding: utf-8 -*-
import re 

str = r'	<MAAaddress>10.177.107.43</MAAaddress>'
str2 = r'#	<MAAaddress>10.177.107.43</MAAaddress>'

regex = r'^<MAAaddress>(.*)</MAAaddress>.*'
m1 = re.search(regex,str.strip())
if m1:
	print m1.groups()[0]
else:
	print 'str not match'
m2 = re.search(regex,str2.strip())
if m2:
	print m2.groups()[0]
else:
	print 'str2 not match'
