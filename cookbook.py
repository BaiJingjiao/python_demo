from collections import deque
from collections import defaultdict
from collections import OrderedDict
import json

def search(lines, pattern, history=5):
    '''
    #保留最后N个元素
    '''
    previous_lines = deque(maxlen=history)
    for li in lines:
        if pattern in li:
            yield li, previous_lines
        previous_lines.append(li)

def dedupe(items, key=None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)


def manual_iter():
    	with open('D:\\mytools\\python-things\\pydemos\\demo.py') as f:
            try:
                while True:
                    line = next(f)
                    print(line, end='')
            except StopIteration:
                pass

if __name__ == '__main__':
    # manual_iter()

    #解压序列赋值给多个变量
    print('#解压序列赋值给多个变量')
    data = [1, "abc", ("2019", "1", "1")]
    index, name, date = data
    print(index)
    print(name)
    print(date)

    #星号表达式
    print('#星号表达式')
    name, age, *phone_numbers, address = ("Mike", 28, "13622234444", "0571-88888888", "HangZhou, Xihu")
    print(phone_numbers)

    #保留最后N个元素
    # print('#保留最后N个元素')
    # with open('D:/mytools/auto_suite_python/demos/demo_blabla.py') as f:
    #     for line, prevlines in search(f, 'print', 5):
    #         for pline in prevlines:
    #             print(pline, end='')
    
    #字典中映射多个值
    d = defaultdict(list) #不去重，但有顺序
    d['a'].append(1)
    d['b'].append(2)
    d['c'].append(3)
    d['a'].append(3)
    d['a'].append(3)
    print(d)

    d2 = defaultdict(set) #去重，没顺序
    d2['a'].add(1)
    d2['b'].add(2)
    d2['c'].add(3)
    d2['a'].add(3)
    d2['a'].add(3)
    print(d2)

    d3 = OrderedDict() #保留元素被插入时的顺序
    d3['a'] = 1
    d3['b'] = 2
    d3['e'] = 5
    d3['c'] = 3
    d3['d'] = 4
    print(d3)
    print(json.dumps(d3))

    #对字典进行计算
    prices = {
        'A':45.23,
        'B':102.20,
        'C':23.11,
        'D':10.75
    }
    #zip()函数创建的是一个只能使用一次的迭代器
    min_price = min(zip(prices.values(), prices.keys()))
    max_price = max(zip(prices.values(), prices.keys()))
    print(min_price)
    print(max_price)

    #对字典进行排序
    print('#对字典进行排序')
    sorted_prices = sorted(zip(prices.values(), prices.keys()))
    for item in sorted_prices:
        print(item)

    # 对字典进行交，并，差
    print('# 对字典进行交，并，差')
    a = {
        'x':1,
        'y':2,
        'z':3
    }
    
    b = {
        'w':10,
        'x':11,
        'y':2
    }

    # Find kyes in common
    print(a.keys() & b.keys())
    # Find keys in a that are not in b
    print(a.keys() - b.keys())
    # Find keys in b that are not in a
    print(b.keys() - a.keys())
    # Find (key, value) pairs in common
    print(a.items() & b.items())
    # Make a new dictionary with certain keys removed
    c = {key:a[key] for key in a.keys() - {'z'}}
    print('c', c)

    # 序列中元素为字典，去重
    print('# 序列中元素为字典，去重')
    dup_dict = [
        {'x':1, 'y':2},
        {'x':1, 'y':3},
        {'x':1, 'y':2},
        {'x':1, 'y':4}
    ]
    dedup_dict = dedupe(dup_dict, key=lambda d:(d['x'], d['y']))
    for item in dedup_dict:
        print(item)
