常用模块
简介

本节实验将介绍 Python 中常用的模块，这些模块能够让我们更有效率的开发一个 Python 项目。这些模块在后续的项目实战中都将会用到。

实验中介绍的模块包括：

datetime：时间日期及相关计算
os：操作系统相关的操作
sys：获取 Python 解释器状态
requests：网络请求处理
base64：二进制数据编码 64 个可打印的 ASCII 字符
collections：提供一系列特殊的容器类
本节操作的内容比较简单，只需要在 Python 3 的交互式环境中尝试每个模块中的方法。

知识点

Python3 模块使用方法
datetime 模块
os 模块
sys 模块
requests 模块
base64 模块
collections 模块
datetime

datetime 模块提供了一些类用于操作日期时间及其相关的计算。比较常用三个类型：

date 封装了日期操作
datetime 封装日期+时间操作
timedelta 表示一个时间间隔，也就是日期时间的差值
导入：

>>> from datetime import date, datetime, timedelta
日期时间的获取：

>>> date.today()
datetime.date(2017, 8, 30)
>>> datetime.utcnow()
datetime.datetime(2017, 8, 30, 6, 15, 15, 931110)
>>> t = datetime.now()
>>> t
datetime.datetime(2017, 8, 30, 14, 17, 56, 887176)
>>> t.day
30
>>> t.year
2017
>>> t.minute
17
datetime 对象与字符串之间的相互转换：

>>> t
datetime.datetime(2017, 8, 30, 14, 17, 56, 887176)
>>> datetime.strftime(t, '%Y-%m-%d %H:%M:%S')
'2017-08-30 14:17:56'
>>> datetime.strptime('2017-10-01 00:00:00', '%Y-%m-%d %H:%M:%S')
datetime.datetime(2017, 10, 1, 0, 0)
用 timedelta 表示时间差值，可以精确到微秒：

timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
用 timedelta 对 datetime 进行加减操作：

>>> t
datetime.datetime(2017, 8, 30, 14, 17, 56, 887176)
>>> t + timedelta(weeks=1, days=-3, hours=3, minutes=-10)
datetime.datetime(2017, 9, 3, 17, 7, 56, 887176)
datetime 模块操作视频：

Play Video

os

os 模块提供了一些接口来获取操作系统的一些信息和使用操作系统功能。

比较常用的有：

>>> import os
# 获取当前工作目录
>>> os.getcwd()
'/home/shiyanlou/Code

# 生成 n 个字节的随机数，用于加密，比如作为 Flask 的 SECRET_KEY
>>> os.urandom(24)
b'8\xbb\x88\xfc\xf2\xe8T\x99\x99C^\xc3)\xe0\xd5#6\x9e\xa5\xe7\xfb\xa0\x07G'

# 在当前目录创建一个目录
>>> os.mkdir('web-app')

# 在当前目录创建一个 app.py 文件
>>> os.mknod(os.getcwd() + '/app.py')
sys

sys 模块可以用于获取 Python 解释器当前的一些状态变量，最常用的就是获取执行 Python 脚本时传入的参数，比如说执行 test.py时传入了一些参数：

python3 test.py arg1 arg2 arg3
那么在 Python 程序中就可以通过 sys.argv 来获取这些参数：

sys.argv  # ['test.py', 'arg1', 'arg2', 'arg3']
sys.argv 返回一个列表，第一个值执行的文件名。

requests

如果你写过爬虫，对这个库应该不陌生。在 requests 库出现之前，网络请求通常用标准库中的 urllib。requests 出现之后，它俨然已经成了 Python 事实上的网络请求标准库。

requests 的接口非常简单：

>>> r = requests.get('https://www.shiyanlou.com')
>>> r.status_code
200
>>> r.headers['content-type']
'text/html; charset=utf-8'
>>> r.text
'\n<!DOCTYPE html>\n<html lang="zh-CN">\n    <head>\n        <meta charset="utf-8">\n        <meta http-eq...'
请求 JSON 数据：

>>> r = requests.get('https://api.github.com')
>>> r.json()
{'current_user_url': 'https://api.github.com/user', ... }
json() 方法会将返回的 JSON 数据转化为一个 Python 字典。

还可以用 requests 执行 POST，DELETE 等其它的 HTTP 方法。

requests 模块操作视频：

Play Video

base64

base64 是一种编码方式，它可以将二进制数据编码 64 个可打印的 ASCII 字符。Base64要求把每三个8Bit的字节转换为四个6Bit的字节（38 = 46 = 24），然后把6Bit再添两位高位0，组成四个8Bit的字节，也就是说，转换后的字符串理论上将要比原来的长1/3。

import base64
>>> base64.b64encode(b'Hello, shiyanlou!')
b'SGVsbG8sIHNoaXlhbmxvdSE='
>>> base64.b64decode(b'SGVsbG8sIHNoaXlhbmxvdSE=')
b'Hello, shiyanlou!'
collections

collections 模块主要提供了一些特别的容器，在特定的情况下我们使用这些容器可以使问题处理更容易一些。

OrderedDict

OrderedDict 是一个特殊的字典。字典本质上是一个哈希表，其实现一般是无序的，OrderedDict 能保持元素插入的顺序：

>>> from collections import OrderedDict
>>> d = OrderedDict()
>>> d['apple'] = 1
>>> d['google'] = 2
>>> d['facebook'] = 3
>>> d['amazon'] = 4
>>> d
OrderedDict([('apple', 1), ('google', 2), ('facebook', 3), ('amazon', 4)])
OrderedDict 同样能以元素插入的顺序来进行迭代或者序列化：

>>> for key in d:
...   print(key, d[key])
...
apple 1
google 2
facebook 3
amazon 4
>>> import json
>>> json.dumps(d)
'{"apple": 1, "google": 2, "facebook": 3, "amazon": 4}'
namedtuple

使用普通的元组（tuple）存在一个问题，每次用下标去获取元素，可能会不知道你这个下标下的元素到底代表什么。namedtuple 能够用来创建类似于元组的类型，可以用索引来访问数据，能够迭代，也可以通过属性名访问数据。让你能够更方便实用的代码：

下面使用命名元组表示坐标系中的点：

>>> from collections import namedtuple
>>> Point = namedtuple('Point', ['x', 'y'])
>>> p = Point(10, 12)
>>> p.x
10
>>> p.y
12
Counter

Counter 用来统计一个可迭代对象中各个元素出现的次数，以字符串为例：

>>> from collections import Counter
>>> c = Counter('https://www.shiyanlou.com')
>>> c
Counter({'w': 3, 'h': 2, 't': 2, 's': 2, '/': 2, '.': 2, 'o': 2, 'p': 1, ':': 1, 'i': 1, 'y': 1, 'a': 1, 'n': 1, 'l': 1, 'u': 1, 'c': 1, 'm': 1})
找出出现次数最多的前 n 个元素：

>>> c.most_common(3)
[('w', 3), ('h', 2), ('t', 2)]
collections 模块操作视频：

Play Video

总结

本节实验将介绍一些在后续项目实战中会用到的常用模块：

datetime：时间日期及相关计算
os：操作系统相关的操作
sys：获取 Python 解释器状态
requests：网络请求处理
base64：二进制数据编码 64 个可打印的 ASCII 字符
collections：提供一系列特殊的容器类
Python 的模块实在是太多了，在使用中不能够靠纯粹的死记硬背，而是靠积累经验熟能生巧。一般项目开发的过程中遇到某种开发需求，首先去搜索下是否 Python 已经有现成的模块去处理这个需求了，如果有的话则直接在代码中使用就可以了，不用再自己从头开始实验。这也是 Python 高效开发的一大优势。
