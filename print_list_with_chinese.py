# -*- coding:utf-8 -*-

import fileinput
import sys
import json
import os.path
from os.path import abspath
from inspect import getsourcefile
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from datetime import timedelta
import string
import random
import time


a = ['中国','浙江','杭州']
print (json.dumps(a, encoding='utf-8', ensure_ascii=False)).decode('utf-8')
