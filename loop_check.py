def loop_check(num=4):
    def _loop_check(func):
        def __loop_check(*arg, **args):
            count = num
            result = False
            waitTime = 0.5
            while count:
                time.sleep(waitTime)
                result = func(*arg, **args)
                if False != result:
                    return result                            
                else:
                    count -= 1
            else:
                print('wait timeout...')
        return __loop_check
    return _loop_check
