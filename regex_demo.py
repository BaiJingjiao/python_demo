'''
#======================================================================
# @author bjj
# 去重，同一个消息体，留一个
# @LoginAck@ArrayList@--1--AppInfo##\s+appName="weixin"\s+####\s+appID="1"\s+##
# @LoginAck@ArrayList@--1--AppInfo##\s+appID="1"\s+####\s+appName="weixin"\s+##
# @LoginAck@ArrayList@--2--AppInfo##\s+appName="w3"\s+####\s+appID="4"\s+##
# @LoginAck@ArrayList@--2--AppInfo##\s+appID="4"\s+####\s+appName="w3"\s+##
#======================================================================
'''     
def getFinalItemRegexList(log, expectedDic):
    regex = ''
    stack = list()
    itemRegexList = list()
    nisList = list() # Nested Information Structure
    noDupNisList = list()
    getInitialItemRegexListWithDup(log, expectedDic, regex, stack, itemRegexList)
#     log.log('902--itemRegexList------------------------------')
#     for item in itemRegexList:
#         log.log(item)
#     log.log('905--itemRegexList------------------------------')
    mergedList = mergeItemRegexList(log, itemRegexList)
    for item in mergedList:
        m = re.search('([^##]*)##.*', item)
        nisList.append(m.groups()[0])
    for nis in nisList:
        if not nis in noDupNisList:
            noDupNisList.append(nis)
    clearedItemRegexList = list()
    for nis in noDupNisList:
        for item in mergedList:
            infoStruc = re.search('([^##]*)##.*', item).groups()[0]
            dup = False
            for c in clearedItemRegexList:
                cm = re.search('([^##]*)##.*', c) #取出结构体部分
                if cm.groups()[0] == infoStruc:
                    dup = True
                    break
            if infoStruc== nis and not(dup):
                clearedItemRegexList.append(item)
#     log.log('925--clearedItemRegexList------------------------------')
#     for item in clearedItemRegexList:
#         log.log(item)
#     log.log('928--clearedItemRegexList------------------------------')
    return clearedItemRegexList
#     return mergedList

'''
#======================================================================
# @author bjj
# 解析传入的expectedDic， 结果存入itemRegexList
#======================================================================
'''
def getInitialItemRegexListWithDup(log, expectedDic, regex, stack, itemRegexList):
    keyRegex = ''
    for key in expectedDic:
#         log.log('expectedDic[key]', expectedDic[key])
#         log.log('type(expectedDic[key])', type(expectedDic[key]))
        if type(expectedDic[key]) is dict:
            #这里要处理key带‘@’的情况---------------------------------
#             stack.append(key)
            if (re.search('^@', key)):
                stack.append(key)
            else:
                stack.append('@'+key+'=')
            getInitialItemRegexListWithDup(log, expectedDic[key], regex, stack, itemRegexList)
        elif (type(expectedDic[key]) is str and not(expectedDic[key].startswith('_')) \
              and expectedDic[key].lower() != 'null' and expectedDic[key].lower() != 'yes' and expectedDic[key].lower() != 'no' \
              and '_' != re.sub('\d+', '', expectedDic[key])) \
              or type(expectedDic[key]) is unicode:
            index = 0
            while index < len(stack):
                regex = regex + stack[index]
                index += 1
            regex = regex + '##\s+' + key + '\s*=\s*' + str('"' + expectedDic[key] + '"') + '\s+##'
            itemRegexList.append(regex)
            regex = ''
        else :
            index = 0
            while index < len(stack):
                regex = regex + stack[index]
                index += 1
            regex = regex + '##\s+' + key + '\s*=\s*' + str(expectedDic[key]) + '\s+##'
            itemRegexList.append(regex)
            regex = ''
    else:
        regex = ''
        if len(stack)>0:
            stack.pop() 

'''
#======================================================================
# @author bjj
# 将这样的
# @LoginAck@ArrayList@--1--AppInfo##\s+appName="weixin"\s+##
# @LoginAck@ArrayList@--1--AppInfo##\s+appID="1"\s+##
# @LoginAck@ArrayList@--2--AppInfo##\s+appName="w3"\s+##
# @LoginAck@ArrayList@--2--AppInfo##\s+appID="4"\s+##
# 合并成这样的（属于同一个消息体的 key：value合并在一起）， 有重复
# @LoginAck@ArrayList@--1--AppInfo##\s+appName="weixin"\s+####\s+appID="1"\s+##
# @LoginAck@ArrayList@--1--AppInfo##\s+appID="1"\s+####\s+appName="weixin"\s+##
# @LoginAck@ArrayList@--2--AppInfo##\s+appName="w3"\s+####\s+appID="4"\s+##
# @LoginAck@ArrayList@--2--AppInfo##\s+appID="4"\s+####\s+appName="w3"\s+##
#======================================================================
'''
def mergeItemRegexList(log, itemRegexList):
    itemRegexListMerged = list()
    for item in itemRegexList:
        m = re.search('(.*)(##.*##)', item)
        nis, kv = m.groups()[0], m.groups()[1]
        kvs = kv
        for item2 in itemRegexList:
            m2 = re.search('(.*)(##.*##)', item2)
            nis2, kv2 = m2.groups()[0], m2.groups()[1]
            if nis == nis2 and kv != kv2:
                kvs = kvs + kv2
        itemRegexListMerged.append(nis+kvs)
#     log.log('1002---itemRegexListMerged-----------------------------')
#     for item in itemRegexListMerged:
#         log.log(item)
#     log.log('1005---itemRegexListMerged-----------------------------')
    return itemRegexListMerged

'''
#======================================================================
# @author bjj
@LoginAck\{(?!@LoginAck).*@ArrayList\{(?!@ArrayList).*(@AppInfo\{(?!@AppInfo).*(?!@AppInfo).*\})(?!@ArrayList).*\}(?!@LoginAck).*\}
@LoginAck\{(?!@LoginAck).*@ArrayList\{(?!@ArrayList).*(@AppInfo\{(?!@AppInfo).*(?!@AppInfo).*\})(?!@ArrayList).*\}(?!@LoginAck).*\}
@LoginAck\{(?!@LoginAck).*@ArrayList\{(?!@ArrayList).*(@AppInfo\{(?!@AppInfo).*(?!@AppInfo).*\})(?!@ArrayList).*\}(?!@LoginAck).*\}
@LoginAck\{(?!@LoginAck).*@ArrayList\{(?!@ArrayList).*(@AppInfo\{(?!@AppInfo).*(?!@AppInfo).*\})(?!@ArrayList).*\}(?!@LoginAck).*\}
(@LoginAck\{(?!@LoginAck).*(?!@LoginAck).*\})
(@LoginAck\{(?!@LoginAck).*(?!@LoginAck).*\})
(@LoginAck\{(?!@LoginAck).*(?!@LoginAck).*\})
'''
def getFinalInfoRegex(log, clearedRegexItem):
    m = re.search('([^##]*)(##.*)', clearedRegexItem)
    nis, kvs = m.groups()[0], m.groups()[1]
    #去掉区分同名消息体的标记（--num--）
    nisList = re.findall('(@[^@]*)', re.sub('--\\d+--', '', nis))
    endRegexList = re.findall('(@[^@=]*)', re.sub('--\\d+--', '', nis))
    regex = ''
    regex2 = ''
    theRange = range(len(nisList))
    for i in theRange:
        if i == len(nisList) -1 and not(nisList[i].endswith('=')):
            regex = regex + '(' + nisList[i] + '\\{(?!' + nisList[i] + ').*'
            regex2 = '(' + nisList[i] + '\\{(?!' + nisList[i] + ').*'
        elif nisList[i].endswith('='):
            regex = regex + re.sub('@', '', nisList[i])#处理类似@deviceList=
            
        else:
            regex = regex + nisList[i] + '\\{(?!' + nisList[i] + ').*'

    count = len(endRegexList)
    while(count):
        count -= 1
        if count == len(endRegexList) - 1:
            #这里添加keyValueRegex
            kvs = re.sub('^##', '', kvs)
            kvs = re.sub('##$', '', kvs)
            kvs = re.sub('#+', '(?!' + endRegexList[count] + ').*', kvs)
            regex = regex + kvs + '(?!' + endRegexList[count] + ').*\\})'
            regex2 = regex2 + kvs + '(?!' + endRegexList[count] + ').*\\})'
    return regex, regex2

'''
#======================================================================
# @author bjj
clearedRegexItem:
@LoginAck@deviceList=@ArrayList@LoginDevice##\s+deviceType="PC"\s+####\s+loginTime=1488529862211\s+##
找到要校验的消息结构体列表，如：
@AppInfo{ appID="2" appName="imss" appLogo="" }
@AppInfo{ appID="4" appName="w3" appLogo="" }
@AppInfo{ appID="3" appName="isales" appLogo="" }
@AppInfo{ appID="6" appName="iSales_Man" appLogo="http://isaleslogo.huawei.com" }
@AppInfo{ appID="5" appName="icare" appLogo="" }
@AppInfo{ appID="1" appName="weixin" appLogo="" }
#======================================================================
'''
def findInfoStrucList(log, clearedRegexItem, msgList):
    infoStrucList = list()
    endRegexList = list()
    m = re.search('([^##]*)(##.*)', clearedRegexItem)
    nis = ''
    kvs = ''
    kvsList = list()
    if m:
        nis, kvs = m.groups()[0], m.groups()[1]
        kvsList = re.findall('(##[^#]*##)', kvs)
    #去掉区分同名消息体的标记（--num--）
    nisList = re.findall('(@[^@]*)', re.sub('--\\d+--', '', nis))
    for item in nisList:
        if not(item.endswith('=')):
           endRegexList.append(item) 
    regex = ''
    theRange = range(len(nisList))
    for i in theRange:
        #处理这样的结构体：@data.userdata.msg.GetRecentConversationMsgAck$RecentConversationInfo
        if re.search('\\$', nisList[i]):
            nisList[i] = re.sub('\\$', '\\\\$', nisList[i])
#             log.log('1092---nisList[i]', nisList[i])
        if i == len(nisList) -1 and not(nisList[i].endswith('=')):
            regex = regex + '(' + nisList[i] + '\\{(?!' + nisList[i] + ').*'
        elif nisList[i].endswith('='):#处理类似@deviceList=
            regex = regex + re.sub('@', '', nisList[i]) #紧跟在“=”后面的结构体名不可省略
#             regex = regex + re.sub('@', '', nisList[i]) + '(?!' + nisList[i-1] + ').*'
            
        else:
            regex = regex + nisList[i] + '\\{(?!' + nisList[i] + ').*'

    count = len(endRegexList)
    while(count):
        count -= 1
        if count == len(endRegexList) - 1:
            regex = regex + '(?!' + endRegexList[count] + ').*\\})'
        else:
            regex = regex + '(?!' + endRegexList[count] + ').*\\}'
    msgs = []#存放item.type的消息体
    dic = {}
    if len(nisList) > 0:
        itemType = nisList[0].replace('@', '')
        #@data.userdata.msg.ServiceProfileAck,解析出itemType
        if re.search('\.', itemType):
            itemType = re.search('.*\.([^\.]*)$', itemType).groups()[0]
        if 0 == len(msgList):        
            log.log('no msg.')
        else:
            for item in msgList:  
                if itemType == item.type:
                    msgs.append(str(item.msg))
        
#         log.log('msgs', msgs)
#         if 0 == len(msgs):
#             log.log('no ', itemType) #支持智能等待后，不再输出此信息
#             raise Exception('failed') #这里不再抛异常，因为支持AssertFalse

        count = 0
        for msg in msgs:
            count = count + 1
#             log.log('-----------------------------------------------------------')
#             log.log('len(msgs)', len(msgs))
            infoStrucList = list()
            #处理消息中的换行
            msg = re.sub(r'\s', '#', msg)
            msg = re.sub(r'#+', ' ', msg)
            #处理消息中=号两边的空格
            msg = re.sub(r'\s=\s', '=', msg)
#             log.log('1063---regex', regex)
#             log.log('1064---msg', msg)
            mm = re.search(regex, msg)
            tempMsg = msg
            while mm:
                infoStrucList.append(mm.groups()[0])
                tempMsg = tempMsg.replace(mm.groups()[0], '')
                mm = re.search(regex, tempMsg)
            if 0 != len(infoStrucList):
                dic[count]=infoStrucList
#             log.log('msg', msg)
#             log.log('clearedRegexItem\t', clearedRegexItem)
#             log.log('regex\t', regex)
#             log.log('---dic[msg]---infoStrucList---')
#             for item in infoStrucList:
#                 log.log(item)
#             log.log('-----------------------------------------------------------')
#             log.log('dic------------------------------------------------------------')
#             log.log('len(dic)', len(dic))
#             log.log(dic)
#             if len(dic) == 0:
#                 log.log('1083---regex', regex)
#                 log.log('1084---msg', msg)
#             for key in dic:
#                 for v in dic[key]:
#                     log.log(v)
#             log.log('dic------------------------------------------------------------')
#             log.log('kvsList------------------------------------------------------------')
#             for kvs in kvsList:
#                 log.log(kvs)
#             log.log('kvsList------------------------------------------------------------')
#             log.log('msgs------------------------------------------------------------')
#             for msg in msgs:
#                 log.log(msg)
#             log.log('msgs------------------------------------------------------------')
#         if 0 == len(dic):
#             log.log('------------------------------------------------------------')
#             log.log('在下列消息中，找不到这样的结构体：', nisList)
#             for msg in msgs:
#                 log.log(msg)
#             log.log('------------------------------------------------------------')
    return dic, kvsList, msgs, nisList


def check(log, dic, kvsList):
    for key in dic:
        flag = True
        for infoStruc in dic[key]:
            flag = True
            for kvs in kvsList:
                kvs = re.sub('#+', '', kvs) #去掉"#"标记
                if re.search('\(\?\)', kvs):
                    continue
#                 log.log('infoStruc', infoStruc)
#                 log.log('kvs', kvs)
                flag = flag and re.search(kvs, infoStruc)
            if flag:
                finalResult = True
                return True
    return False

def checkList(log, dic, index, expectedValue):
    for key in dic:
        flag = False
#         regex_ArrayList = '@java.util.ArrayList{([^@]*)}\s*' #不再包含结构体的列表
        regex_ArrayList = '@[^@]*ArrayList{([^@]*)}\s*' #不再包含结构体的列表
        for infoStruc in dic[key]:
#             log.log('1111---infoStruc', infoStruc)
#             log.log('1112---regex_ArrayList', regex_ArrayList)
            flag = False
            m = re.search(regex_ArrayList, infoStruc)
#             log.log('m', m)
            mylist = list()
            if m:
                mylist = re.findall('\d+', m.groups()[0])
                #@java.util.ArrayList{ "https://clouddrive-dr.huawei.com1" }
                #规避IndexError: list index out of range
                if len(mylist) < int(index):
                    continue
                realValue = mylist[int(index)]
#                 log.log('1118---expectedValue', expectedValue, type(expectedValue))
#                 log.log('1119---realValue', realValue, type(realValue))
                if expectedValue.strip() == realValue.strip():
#                     log.log('True')
                    return True
                else:
#                     log.log('1124---False')
#                     log.log('1125---infoStruc', infoStruc)
                    pass
    return False
'''
#=======================================================================================
#   在使用这个方法的时候expectResult必须传期望得到的结果，realResult必须传服务器实际返回的结果，顺序不能调换，
         因为通常我们不需要校验服务器返回的所有参数，期望得到的结果数会比实际返回的结果数少
#=======================================================================================
'''
def assertEqual(log, expectResult, realResult):
    if None == expectResult or type(expectResult) is str \
            or int == type(realResult) \
            or type(expectResult) is unicode\
            or type(expectResult) is bool:
    	if(expectResult == realResult):
    		result = True
    		log.SetResultPass()
    		return
    	else:
    		result = False
    		log.SetResultFailed()
    		raise Exception('Assertion Failed', 'expectedResult:', expectResult, 'realResult:', realResult) 
    
    if (type(expectResult) != type(realResult)):
    	result = False
    	log.SetResultFailed()
    	raise Exception('Assertion Failed', 'type of [', expectResult, '] and [:', realResult, '] not equal')
    
    if type(expectResult) is dict:
          import json 
          for k in expectResult.iterkeys():
              try:
                  realResult[k]
              except:
                  result = False 
                  log.SetResultFailed() 
                  log.log('=============================================================================')
                  log.log('key:[%s] is missing in realResult.' % k)             
                  log.log('expectResult\n', json.dumps(expectResult, indent=4))                
                  log.log('realResult\n', json.dumps(realResult, indent=4))   
                  log.log('=============================================================================')
                  raise Exception('Assertion Failed key error')   
    		  
              if type(expectResult[k]) is list:
                  if sorted(expectResult[k]) != sorted(realResult[k]):
                    log.log('assertEqual断言失败===========================================================')
                    log.log('【期望值】')
                    for item in expectResult[k]:
                        log.log(item)
                    log.log('【实际值】')
                    for item in realResult[k]:
                        log.log(item)
                    log.log('============================================================================')
                    result = False
                    log.SetResultFailed()
                    raise Exception('Assertion Failed.')                         
              elif expectResult[k] != realResult[k]:                   
                  result = False
                  log.SetResultFailed() 
                  log.log('=============================================================================')
                  log.log('Different value between expectResult and realResult for key[%s]' % (k))             
                  log.log('expectResult\n', json.dumps(expectResult, indent=4))                
                  log.log('realResult\n', json.dumps(realResult, indent=4))   
                  log.log('=============================================================================')
                  raise Exception('Assertion Failed','Different key:',k,'Different value:',expectResult[k],realResult[k])   
          result = True 
          log.SetResultPass() 
          return    
    else:      
    	log.log(type(expectResult))
    	log.log(type(realResult))
    	set_1 = set(repr(x) for x in expectResult)
    	set_2 = set(repr(x) for x in realResult)
    	log.log(set_1)
    	log.log(set_2)
    	if(set_1 == set_2):
    		result = True
    		log.SetResultPass()
    	else:
    		result = False
    		log.SetResultFailed()
    		raise Exception('Assertion Failed', 'expectedResult: ', expectResult, 'realResult:', realResult) 
 

    
def assertNotEqual(log, condition1, condition2):
    if type(condition1) is str or int == type(condition1) or type(condition1) is unicode:
        if(condition1 != condition2):
            result = True
            log.SetResultPass()
            return
        else:
            result = False
            log.SetResultFailed()
            raise Exception('Assertion Failed', 'expectedResult: ', expectResult, 'realResult:', realResult) 
        
    set_1 = set(repr(x) for x in condition1)
    set_2 = set(repr(x) for x in condition2)
    if(set_1 != set_2):
        result = True
        log.SetResultPass()
    else:
        result = False
        log.SetResultFailed()
        raise Exception('Assertion Failed', 'condition1: ', condition1, 'condition2:', condition1)

'''
'%Y-%m-%d %H.%M.%S'
'''                        
def getStampSpecialFormat(formatStr):
    now = datetime.today()
    mytime = datetime.strftime(now, formatStr)
    return mytime


def assertAutoWait(log, execute_or_pcResult, expectedResultDic, expectedResult=True, wait=10):
    log.log('assertAutoWait()开始执行...')
    count = wait
    msgList = execute_or_pcResult.getMsgList()
    while(count>0):
        try:
            msgList = execute_or_pcResult.getMsgList() #新测试桩，msgList不再自动更新(2017.12)
            assertBase(log, msgList, expectedResultDic, expectedResult, count, printerrmsg=False)
            break
        except:
            time.sleep(1)
            log.log('等待1秒......')
        count = count - 1
        if 0 == count:
            for item in msgList:
                log.log(item.msg)
    returnResult = assertBase(log, msgList, expectedResultDic, expectedResult)
    log.log('assertAutoWait()执行结束')
    return returnResult

'''
#======================================================================
# assertBaseAutoWait()创建于2017-5-17
# @author: bjj
# @summary: 断言智能等待
# @param wait: 超时时间，默认2秒超时
# 举例：assertBaseAutoWait(self, msgList, expectedResultDic)，不指定超时时间，默认2秒超时
# 举例：assertBaseAutoWait(self, msgList, expectedResultDic, wait=7)，指定超时时间为7秒
#======================================================================
'''
def assertBaseAutoWait(log, msgList, expectedResultDic, expectedResult=True, wait=10):
    log.log('assertBaseAutoWait()开始执行...')
    count = wait
    while(count>0):
        try:
            assertBase(log, msgList, expectedResultDic, expectedResult, count, printerrmsg=False)
            break #如断言成功则中断循环
        except:
            time.sleep(1)
            log.log('等待1秒......')
        count = count - 1
    returnResult = assertBase(log, msgList, expectedResultDic, expectedResult)
    log.log('assertBaseAutoWait()执行结束')
    return returnResult
'''
#======================================================================
# @author: bjj
# @summary: 自定义断言
#======================================================================
'''        
def assertBase(log, msgList, expectedResultDic, expectedResult=True, waiting=False, printerrmsg=True):        
    clearedRegexList = getFinalItemRegexList(log, expectedResultDic)
    finalResult = True
    expectedValue = None
    realValue = None
    for clearedRegexItem in clearedRegexList:
#         log.log('1155---assertBase---clearedRegexItem', clearedRegexItem)
        #@data.userdata.msg.ServiceProfileAck@funcIDList=@java.util.ArrayList##\s+--index--[7]\s*=\s*"67"\s+##
        m_index = re.search(r'--index--\[(\d+)\].*=[^\d]*(\d+)[^\d]*##', clearedRegexItem)
        dic, kvsList, msgs, nisList = findInfoStrucList(log, clearedRegexItem, msgList)

#         log.log('1179---len(dic)', len(dic))
#         log.log('1180---dic', dic)
        if 0 == len(dic):
            if waiting:
#                 log.log('waiting...')
                if (expectedResult):
                    raise Exception('Assertion Failed, no msg')
            else:
                if (expectedResult) and (True == printerrmsg):
                    log.log('=============================================================================')
                    log.log('在下列消息中，找不到这样的结构体：', nisList)
                    for msg in msgs:
                        log.log(msg)
                    log.log('=============================================================================')
                    result = False
                    log.SetResultFailed()
                    raise Exception('Assertion Failed, no msg')

        if (m_index):
            index = m_index.groups()[0]
            expectedValue = m_index.groups()[1]
            flag = checkList(log, dic, index, expectedValue)
#             log.log('1156---flag', flag)
            finalResult = True
            if(not(flag) and expectedResult):
                finalResult = False
            
#             if not(finalResult):
            if False == finalResult:
                if True == waiting:
#                     log.log('waiting...')
                    raise Exception('Assertion Failed, 按照【index】，找不【期望值】')
                elif True == printerrmsg:
                    log.log('=============================================================================')
                    log.log('找不到【index】', index, '【期望值】', expectedValue)
                    for key in dic:
                        total = len(dic[key])
                        remain = total - 30
                        if len(dic[key]) > 30:
                            for i in range(30):
                                log.log(dic[key][i])
                            else:
                                log.log('还有%d个条目未打印' % remain)
                                log.log('... ...')
                        else:
                            for item in dic[key]:
                                log.log(item)
                    log.log('=============================================================================')
                    result = False
                    log.SetResultFailed()
                    raise Exception('Assertion Failed, 按照【index】，找不到【期望值】')        
        else:
            #在msgList中校验传入的"字典“内容是否存在，如存在，flag=True
            flag = check(log, dic, kvsList) 
            
            #判断实际结果与期望结果是否一致
            if flag == expectedResult:
                finalResult = True #如一致，最后的断言结果为True
            else:
                finalResult = False #如不一致，最后的断言结果为False
            
            #如断言失败，在控制台打印断言内容，为排查问题提供便利
            if False == finalResult:
                if True == waiting:
#                     log.log('waiting...')
                    raise Exception('Assertion Failed, 按照【index】，找不 到【期望值】')
                elif True == printerrmsg:
                    if True == expectedResult:
                        msg = "在下面【结构列表】中找不到这些【键值对】"
                    else:
                        msg = "在下面【结构列表】中不应找到这些【键值对】"
                    log.log('=============================================================================')
                    log.log(msg)
                    kvpList = list()
                    for kv in kvsList:
                        kv = re.sub('#', '', kv)
                        kv = re.sub(r'\\s\+', '', kv)
                        kv = re.sub(r'\\s\*', '', kv)
                        kvpList.append(kv)
                    log.log('期望的【键值对】: ', kvpList)
                    for key in dic:
                        for infoStruc in dic[key]:
                            kvpList_real = list()
                            for kvp in kvpList:
                                kvp = re.search('(.*=).*', kvp).groups()[0] + '([^\s]*)'
                                m = re.search(kvp, infoStruc)
            #                     log.log('kvs', kvs)
            #                     log.log('infoStruc', infoStruc)
            #                     log.log('m', m)
                                if m:
                                    v = m.groups()[0]
                                    kvpList_real.append(re.search('(.*=).*', kvp).groups()[0] + v)
                            else:
                                log.log('实际的【键值对】: ', kvpList_real)
    #                             log = ''
    #                             for item in kvpList_real:
    #                                 log = log + '实际的【键值对】: ' + item
                                
                    log.log('【结构列表】 ')
                    for key in dic:
                        total = len(dic[key])
                        remain = total - 30
                        if len(dic[key]) > 30:
                            for i in range(30):
                                log.log(dic[key][i])
                            else:
                                log.log('还有%d个条目未打印' % remain)
                                log.log('... ...')
                        else:
                            for item in dic[key]:
                                log.log(item)
                    log.log('=============================================================================')
                    result = False
                    log.SetResultFailed()
    #                 log.log('set result=False, and SetResultFailed')
    #                 log.log('1401---result', result)
                    raise Exception('Assertion Failed, '+msg)
                else:
                    raise Exception()
    else:
        result = True
        log.SetResultPass()
        #只有在result=True时，加return语句，否则无法抛异常
        return getDataFromMsg(log, expectedResultDic, msgList)

    
'''
#======================================================================
# method: getDataFromMsg 
# return: 返回列表
#======================================================================
'''
def checkForGetDataFromMsg(log, dic, kvsList, regex, resultList):
    v = None
    for key in dic:
        flag = True
        for infoStruc in dic[key]:
            flag = True
#             log.log('infoStruc', infoStruc)
            for kvs in kvsList:
                kvs = re.sub('#+', '', kvs) #去掉"#"标记
                if re.search('\(\?\)', kvs):
#                     kvs = re.sub('\(\?\)', r'([^\s]*)', kvs)#这样处理，当值为非普通字符串时会有问题
                    kvs = re.search('(.*=).*', kvs).groups()[0] + '([^\s]*)'
#                     log.log('1424---kvs', kvs)
#                     log.log('infoStruc', infoStruc)
                    m = re.search(kvs, infoStruc)
#                     log.log('m', m)
                    if m:
#                         log.log('m.groups()', m.groups())
                        v = m.groups()[0]
                    continue #当发现是取值语句时，不做校验
                flag = flag and re.search(kvs, infoStruc)
            if flag:
                if v != None and v.startswith('"'):
                    v = re.sub('"', '', v)
                if v != None:
                    resultList.append(v)

def checkListForGetDataFromMsg(log, dic, index, expectedValue):
    for key in dic:
        flag = False
        regex_ArrayList = '@java.util.ArrayList{([^@]*)}\s+'
        for infoStruc in dic[key]:
#             log.log('infoStruc', infoStruc)
            flag = False
            m = re.search(regex_ArrayList, infoStruc)
            mylist = list()
            if m:
                mylist = re.findall('\d+', m.groups()[0])
                realValue = mylist[int(index)]
#                 log.log('expectedValue', expectedValue, type(expectedValue))
#                 log.log('realValue', realValue, type(realValue))
                if expectedValue.strip() == realValue.strip():
#                     log.log('True')
                    return True
                else:
                    log.log('1110---False')
    return False

def getDataFromMsg(log, returnDic, msgList):
    resultList = list()
    clearedItemRegexList = getFinalItemRegexList(log, returnDic)
#     for item in clearedItemRegexList:
#         log.log('1462---', item)
    
    for clearedRegexItem in clearedItemRegexList:
#         log.log('1464---clearedRegexItem', clearedRegexItem)
        m = re.search('\(\?\)', clearedRegexItem)
#         log.log('1470---m', m)
        if m: #只处理“取值”的部分
            dic, kvsList, msgs, nisList = findInfoStrucList(log, clearedRegexItem, msgList)
            regex, regex2 = getFinalInfoRegex(log, clearedRegexItem)
            regex2 = re.sub('#+', '', regex2)
            regex2 = re.sub('\(\?\)', r'([^\s]*)', regex2)
    #         log.log('1210---regex', regex)
#             log.log('1211---regex2', regex2)
            checkForGetDataFromMsg(log, dic, kvsList, regex2, resultList)
    #         for key in dic:
    #             for item in dic[key]:
    #                 log.log('1213---item', item)
    #                 resultList.append(re.search(regex2, item).groups()[1])
    #         log.log('return values', resultList)
            return resultList


'''for xxxxxx token authenticate. add by wjw 2017.5.10'''
import ssl,socket,httplib
class HTTPSConnection(httplib.HTTPSConnection):               
    def __init__(self, *args, **kwargs):
        httplib.HTTPSConnection.__init__(self, *args, **kwargs)              
    def connect(self):
        sock = socket.create_connection((self.host, self.port), self.timeout, self.source_address)
        if self._tunnel_host:
            self.sock = sock
            self._tunnel()                    
        try:
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file,
                                        ssl_version=ssl.PROTOCOL_TLSv1)
        except ssl.SSLError:
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file,
                                        ssl_version=ssl.PROTOCOL_SSLv23)
#发送https请求
def https_request(log, ip, url, reqData, headers):
    conn = HTTPSConnection(ip + ':' + '8443')  
    try:
        conn.request('POST', url, None, headers)  
        httpres = conn.getresponse() 
        status = httpres.status
        rspBody = httpres.read()  
        rspHead = httpres.getheaders() 
        authenticate= httpres.getheader('www-authenticate')
    finally:
        conn.close() 
    return authenticate, rspBody        

def get_authenticate_value(log, authenticate, key):            
    import re
    authList=re.split(',\\s{0,1}', authenticate)
    for authStr in authList:
        result = re.findall(key+'="(.*?)"', authStr)
        if 1 == len(result):
            return result[0]
    else:
        return None
    
#获取xml节点对应值    
def get_xml_node_value(log, xmlSourse, parentNode, nodeName):
    import xml.etree.ElementTree
    if os.path.isfile(xmlSourse):
        root=xml.etree.ElementTree.parse(xmlSourse)
    else:
        root = xml.etree.ElementTree.fromstring(xmlSourse)
    nodeList = root.getiterator(parentNode) 
    
    if 0 == len(nodeList):
        log.log(parentNode, ' get fail.')
        return False
    
    for node in nodeList:
        if not node.getchildren():
            log.log(parentNode, 'node has no child. value is:', node.text)
            return node.text                
        for child in node.getchildren():
            if nodeName == child.tag:                    
                log.log(nodeName, 'node value is:', child.text)
                return child.text
        else:
            log.log('get value fail.')
            return False
        
#获取token，传入账号密码
def get_xxxxxx_token(log, userName, pwd):
    xxxxxxIP = get_xml_node_value(log, os.path.dirname(os.getcwd())+r'\executor\config\cfg\UDPConfig.xml', 'xxxxxxIP', 'IP')          
    url = 'https://'+xxxxxxIP+':8443/login/sc'      
    headers = {'Content-Type':'application/json;charset=UTF-8','Accept-Language':'zh_CN',
               'Authorization':'Digest username='+ userName +', algorithm=MD5'}   
    authenticate, rspBody = https_request(log, xxxxxxIP, url, None, headers)
    nonce = get_authenticate_value(log, authenticate, 'nonce')
    realm = get_authenticate_value(log, authenticate, 'realm') 
        
    import hashlib     
    HA1Hex = hashlib.md5() 
    HA1Hex.update(userName + ":" + realm + ":" + pwd)
    HA2Hex = hashlib.md5() 
    HA2Hex.update("POST:/login/sc")
    respo = hashlib.md5()       
    respo.update(HA1Hex.hexdigest() + ":" + nonce + ":" + HA2Hex.hexdigest())
    response = respo.hexdigest()
    
    headers = {'Content-Type':'application/json;charset=UTF-8','Accept-Language':'zh_CN',
               "Authorization":"Digest username=\""+userName+"\", realm=\""+realm+",nonce=\""+nonce+"\",uri=\"/login/sc\",response=\""+response+"\""}   
    authenticate, rspBody = https_request(log, xxxxxxIP, url, None, headers)
    token = get_xml_node_value(log, rspBody, 'LoginToken', 'AccessToken')
    import base64
    token = base64.b64decode(token)
    log.log(token)
    return token
'''end'''


def findInfoStrucList_log(log, clearedRegexItem, logStr):
    infoStrucList = list()
    endRegexList = list()
    m = re.search('([^##]*)(##.*)', clearedRegexItem)
    nis = ''
    kvs = ''
    kvsList = list()
    if m:
        nis, kvs = m.groups()[0], m.groups()[1]
        kvsList = re.findall('(##[^#]*##)', kvs)
    #去掉区分同名消息体的标记（--num--）
    nisList = re.findall('(@[^@]*)', re.sub('--\\d+--', '', nis))
    for item in nisList:
        if not(item.endswith('=')):
           endRegexList.append(item) 
    regex = ''
    theRange = range(len(nisList))
    for i in theRange:
        #处理这样的结构体：@data.userdata.msg.GetRecentConversationMsgAck$RecentConversationInfo
        if re.search('\\$', nisList[i]):
            nisList[i] = re.sub('\\$', '\\\\$', nisList[i])
#             log.log('1092---nisList[i]', nisList[i])
        if i == len(nisList) -1 and not(nisList[i].endswith('=')):
            regex = regex + '(' + nisList[i] + '\\{(?!' + nisList[i] + ').*'
        elif nisList[i].endswith('='):#处理类似@deviceList=
            regex = regex + re.sub('@', '', nisList[i]) #紧跟在“=”后面的结构体名不可省略
#             regex = regex + re.sub('@', '', nisList[i]) + '(?!' + nisList[i-1] + ').*'
            
        else:
            regex = regex + nisList[i] + '\\{(?!' + nisList[i] + ').*'

    count = len(endRegexList)
    
    regex_date = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \d{3}\|'
    while(count):
        count -= 1
        if count == len(endRegexList) - 1:
            regex = regex + '(?!' + endRegexList[count] + ').*\\})'
        else:
            regex = regex + '(?!' + endRegexList[count] + ').*\\}'  
#     regex = regex + '(?!' + regex_date + ').*'+ regex_date +'.*'
#     regex = "(@message.Chat\{(?!@message.Chat).*(?!@message.Chat).*\})\s*\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \d{3}\|.*"
#     log.log('1720---regex', regex)
    msgs = []#存放item.type的消息体
    dic = {}
    if len(nisList) > 0:
        itemType = nisList[0].replace('@', '')
        #@data.userdata.msg.ServiceProfileAck,解析出itemType
        if re.search('\.', itemType):
            itemType = re.search('.*\.([^\.]*)$', itemType).groups()[0]
        if 0 == len(logStr):        
            log.log('logStr为空.')
        else:
#             for item in msgList:
#                 if itemType == item.type:
#                     msgs.append(str(item.msg))
            all = re.findall(regex, logStr)
            msgs = all
                    
        
#         log.log('msgs', msgs)
#         if 0 == len(msgs):
#             log.log('no ', itemType) #支持智能等待后，不再输出此信息
#             raise Exception('failed') #这里不再抛异常，因为支持AssertFalse

        count = 0
        for msg in msgs:
            count = count + 1
#             log.log('-----------------------------------------------------------')
#             log.log('len(msgs)', len(msgs))
            infoStrucList = list()
            #处理消息中的换行
            msg = re.sub(r'\s', '#', msg)
            msg = re.sub(r'#+', ' ', msg)
            #处理消息中=号两边的空格
            msg = re.sub(r'\s=\s', '=', msg)
#             log.log('1753---regex', regex)
#             log.log('1754---msg', msg)
            mm = re.search(regex, msg)
            tempMsg = msg
            while mm:
                infoStrucList.append(mm.groups()[0])
                tempMsg = tempMsg.replace(mm.groups()[0], '')
                mm = re.search(regex, tempMsg)
            if 0 != len(infoStrucList):
                dic[count]=infoStrucList
#             log.log('msg', msg)
#             log.log('clearedRegexItem\t', clearedRegexItem)
#             log.log('regex\t', regex)
#             log.log('---dic[msg]---infoStrucList---')
#             for item in infoStrucList:
#                 log.log(item)
#             log.log('-----------------------------------------------------------')
#             log.log('dic------------------------------------------------------------')
#             log.log('len(dic)', len(dic))
#             log.log(dic)
#             if len(dic) == 0:
#                 log.log('1083---regex', regex)
#                 log.log('1084---msg', msg)
#             for key in dic:
#                 for v in dic[key]:
#                     log.log(v)
#             log.log('dic------------------------------------------------------------')
#             log.log('kvsList------------------------------------------------------------')
#             for kvs in kvsList:
#                 log.log(kvs)
#             log.log('kvsList------------------------------------------------------------')
#             log.log('msgs------------------------------------------------------------')
#             for msg in msgs:
#                 log.log(msg)
#             log.log('msgs------------------------------------------------------------')
#         if 0 == len(dic):
#             log.log('------------------------------------------------------------')
#             log.log('在下列消息中，找不到这样的结构体：', nisList)
#             for msg in msgs:
#                 log.log(msg)
#             log.log('------------------------------------------------------------')
    return dic, kvsList, msgs, nisList

def assertBase_log(log, logStr, expectedResultDic, expectedResult=True, waiting=False):        
    clearedRegexList = getFinalItemRegexList(log, expectedResultDic)
    finalResult = True
    expectedValue = None
    realValue = None
    for clearedRegexItem in clearedRegexList:
#         log.log('1155---assertBase---clearedRegexItem', clearedRegexItem)
        #@data.userdata.msg.ServiceProfileAck@funcIDList=@java.util.ArrayList##\s+--index--[7]\s*=\s*"67"\s+##
        m_index = re.search(r'--index--\[(\d+)\].*=[^\d]*(\d+)[^\d]*##', clearedRegexItem)
        dic, kvsList, msgs, nisList = findInfoStrucList_log(log, clearedRegexItem, logStr)

#         log.log('1179---len(dic)', len(dic))
#         log.log('1180---dic', dic)
        if 0 == len(dic):
            if waiting:
#                 log.log('waiting...')
                if (expectedResult):
                    raise Exception('Assertion Failed, no msg')
            else:
                if (expectedResult):
                    log.log('=============================================================================')
                    log.log('在下列消息中，找不到这样的结构体：', nisList)
                    for msg in msgs:
                        log.log(msg)
                    log.log('=============================================================================')
                    result = False
                    log.SetResultFailed()
                    raise Exception('Assertion Failed, no msg')

        if (m_index):
            index = m_index.groups()[0]
            expectedValue = m_index.groups()[1]
            flag = checkList(log, dic, index, expectedValue)
#             log.log('1156---flag', flag)
            finalResult = True
            if(not(flag) and expectedResult):
                finalResult = False
            
            if not(finalResult):
                if waiting:
#                     log.log('waiting...')
                    raise Exception('Assertion Failed, 按照【index】，找不【期望值】')
                else:
                    log.log('=============================================================================')
                    log.log('找不到【index】', index, '【期望值】', expectedValue)
                    for key in dic:
                        total = len(dic[key])
                        remain = total - 30
                        if len(dic[key]) > 30:
                            for i in range(30):
                                log.log(dic[key][i])
                            else:
                                log.log('还有%d个条目未打印' % remain)
                                log.log('... ...')
                        else:
                            for item in dic[key]:
                                log.log(item)
                    log.log('=============================================================================')
                    result = False
                    log.SetResultFailed()
                    raise Exception('Assertion Failed, 按照【index】，找不到【期望值】')        
        else:
            flag = check(log, dic, kvsList)
            
            finalResult = True
            if(not(flag) and expectedResult):
                finalResult = False
                    
            if not(finalResult):
                if waiting:
#                     log.log('waiting...')
                    raise Exception('Assertion Failed, 按照【index】，找不 到【期望值】')
                else:
                    log.log('=============================================================================')
                    log.log("在下面【结构列表】中找不到这些【键值对】")
                    kvpList = list()
                    for kv in kvsList:
                        kv = re.sub('#', '', kv)
                        kv = re.sub(r'\\s\+', '', kv)
                        kv = re.sub(r'\\s\*', '', kv)
                        kvpList.append(kv)
                    log.log('期望的【键值对】: ', kvpList)
                    for key in dic:
                        for infoStruc in dic[key]:
                            kvpList_real = list()
                            for kvp in kvpList:
                                kvp = re.search('(.*=).*', kvp).groups()[0] + '([^\s]*)'
                                m = re.search(kvp, infoStruc)
            #                     log.log('kvs', kvs)
            #                     log.log('infoStruc', infoStruc)
            #                     log.log('m', m)
                                if m:
                                    v = m.groups()[0]
                                    kvpList_real.append(re.search('(.*=).*', kvp).groups()[0] + v)
                            else:
                                log.log('实际的【键值对】: ', kvpList_real)
    #                             log = ''
    #                             for item in kvpList_real:
    #                                 log = log + '实际的【键值对】: ' + item
                                
                    log.log('【结构列表】 ')
                    for key in dic:
                        total = len(dic[key])
                        remain = total - 30
                        if len(dic[key]) > 30:
                            for i in range(30):
                                log.log(dic[key][i])
                            else:
                                log.log('还有%d个条目未打印' % remain)
                                log.log('... ...')
                        else:
                            for item in dic[key]:
                                log.log(item)
                    log.log('=============================================================================')
                    result = False
                    log.SetResultFailed()
    #                 log.log('set result=False, and SetResultFailed')
    #                 log.log('1401---result', result)
                    raise Exception('Assertion Failed, 在【结构列表】中找不到【键值对】')
    else:
        result = True
        log.SetResultPass()
        #只有在result=True时，加return语句，否则无法抛异常
        return getDataFromMsg_log(log, expectedResultDic, logStr)

def getDataFromMsg_log(log, returnDic, logStr):
    resultList = list()
    clearedItemRegexList = getFinalItemRegexList(log, returnDic)
#     for item in clearedItemRegexList:
#         log.log('1462---', item)
    
    for clearedRegexItem in clearedItemRegexList:
#         log.log('1464---clearedRegexItem', clearedRegexItem)
        m = re.search('\(\?\)', clearedRegexItem)
#         log.log('1470---m', m)
        if m: #只处理“取值”的部分
            dic, kvsList, msgs, nisList = findInfoStrucList_log(log, clearedRegexItem, logStr)
            regex, regex2 = getFinalInfoRegex(log, clearedRegexItem)
            regex2 = re.sub('#+', '', regex2)
            regex2 = re.sub('\(\?\)', r'([^\s]*)', regex2)
    #         log.log('1210---regex', regex)
#             log.log('1211---regex2', regex2)
            checkForGetDataFromMsg(log, dic, kvsList, regex2, resultList)
    #         for key in dic:
    #             for item in dic[key]:
    #                 log.log('1213---item', item)
    #                 resultList.append(re.search(regex2, item).groups()[1])
    #         log.log('return values', resultList)
            return resultList

     
def loop_check(log, num=8):
    def _loop_check(func):
        def __loop_check(*arg, **args):
            count = num
            result = False
            waitTime = 0.5#每次等待时间
            while count:
                time.sleep(waitTime)
                result = func(*arg, **args)
                if False != result:
                    return result                            
                else:
                    log.log('check again..')
                    count -= 1
        return __loop_check
    return _loop_check
