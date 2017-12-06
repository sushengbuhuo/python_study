Python 基础语法
简介

楼+ 课程的同学技术基础不同，本周实验内容只包含 Python 最常用到的知识点，仍然是以动手实践为主，一些高级用法会在后续的项目实战中用到的时候再详细讲解。

如果先前没有 Python 基础，请务必仔细学习本周的所有实验，每个知识点都要弄懂。如果遇到无法理解的问题，欢迎随时在讨论区或 QQ 讨论组中提问及讨论。

知识点

Python 开发环境
变量与数据类型
输入与输出
运算
字符串
控制结构
异常处理
模块和包
命令行参数
__main__
Python 是什么

Python 是一种编程语言，能够快速上手并且功能强大。Python 提供了非常丰富的基础模块和第三方模块，可以直接在程序中使用，这些模块包含了数据库，Web 开发，文件操作等一系列的功能，避免了重复造轮子，提高编程的效率。本周的实验中会涉及到的 Flask Web 框架，就是一个非常强大的 Web 开发模块。

目前的 Python 版本包括 Python 2 和 Python 3，两个版本之间代码不兼容，3 比 2 有很大的改进，大部分的库都已经支持了 Python 3，所以本系列课程使用的是 Python 3 版本。如果已经有过 Python2 的编程基础，可以非常容易的转向 Python 3。

优点与缺点

人生苦短，我用 Python。

这不是一句戏言，Python 最大的优势就是简单，少量的代码实现复杂的功能。对比其他的编程语言，C 语言实现一个简单的命令行聊天室可能至少需要上千行代码，同样功能的，在 Python 中一百多行就能够解决了。并且，Python 的基础库和第三方库足够多，我们开发的时候可以利用的现成的模块非常多。这一点，能够极大提高工作效率。

缺点方面，Python 是一个解释型的编程语言，每次执行的时候会一行一行的解释执行，因此执行的性能比不上编译型的语言。性能的损失之外，Python 程序的源代码是完全开放的。因为 Python 程序是脚本，不是编译成二进制分发的，通常很难进行代码保护。

Python 的应用场景

实验楼 网站就是 Python 开发的，我们的大部分组件，例如实验环境管理模块、课程管理、Web服务等都是 Python 开发的。我们选择使用 Python 的一大因素是能够快速开发，团队学习成本低，虽然性能上有损失，但结合我们自己的业务完全可以接受。此外，国内的 豆瓣 也是 Python 开发的。

目前，Python 最主要的应用场景包括网络爬虫，Web 开发，自动化运维，数据分析等领域，这些主要领域，楼+课程中分别提供了实战项目进行学习。并在每个实战项目之后，提供了一系列功能扩展的挑战等待你自己独立思考完成。

楼+ Python 实战课程虽然不能保证你学完后就是个 Python 大牛（这仍然需要很长时间的多些代码实战练习，请不要幻想有任何不通过努力就能够技能快速成长的课程），但课程体系的设置是让你在最短的时间内能够掌握 Python 最主要的应用开发方式，遇到类似的问题能够自己使用 Python 快速解决。

开发环境

安装

实验楼提供的 Ubuntu 14.04 操作系统环境中已经安装了 Python 3.x。如果需要自己在 Linux 环境下安装 Python 也非常简单，默认的包管理都可以支持直接安装，例如 Ubuntu 下使用 apt-get 安装：

sudo apt-get update
sudo apt-get install python3
在 Mac 下可以使用 brew install python3 命令进行安装，而 Windows 下则可以在 Python 官网下载后通过图形界面一步步点击下一步进行安装。

交互式

在实验环境中，我们使用 python3 命令启动进入到 Python 3 交互式的环境中，在这个环境中输入的代码都可以立即执行并得到输出结果。交互式的环境，在开发中经常用来调试和测试代码。

点击右边桌面上的 Xfce 终端，启动 Linux 命令行终端，在终端中输入 python3 进入到 Python 交互式环境：



在这个环境中的 >>> 提示符后面输入代码，先输入 print('hello shiyanlou')，将一串字符串打印到屏幕上。

退出交互式环境的方式比较简单，可以使用 Ctrl-D 快捷键，也可以输入 exit() 代码退出。



执行脚本

最简单的 Python 程序就是一个或多个存有源代码的脚本文件，通常会以 .py 作为扩展名存储。

当完成脚本的编写后，我们使用 Python 解释器来运行 Python 脚本。

我们创建一个简单的脚本并尝试执行，脚本中只包含上一节交互式环境中的一行代码，注意 echo 命令需要在 Linux 终端的目的是创建文件并写入内容：

$ echo "print('hello shiyanlou')" > /home/shiyanlou/shiyanlou.py
直接使用 Python 3 解释器执行脚本：

$ python3 /home/shiyanlou/shiyanlou.py


基本操作视频：

您还没有安装flash播放器，请点击这里安装
安装后重启浏览器即可播放视频

This is a modal window.No compatible source was found for this media.
初次尝试

现在我们开始尝试编写第一个 Python 程序，这个程序的作用是计算一个半径为 5 的圆的面积，并输出。

在这个程序中，我们将初次接触 Python 的脚本编写与执行、模块引入和使用的概念。

选择编辑器

实验楼环境中内置了很多种代码编辑工具，可以根据自己的需求选择：

vim：程序员最喜欢的编辑工具，命令行中执行，上手比较复杂，感兴趣可以先学习下实验楼的 Vim 基础课程
gedit：类似记事本，编写的时候有代码高亮，注意保存的文件路径
sublime：又一个 Python 程序编写常用的编辑器，有很多插件可以选择，有代码高亮和提示等功能
在本课程的学习过程中，如果对 Linux 比较熟悉，推荐使用 Vim，如果不熟悉，推荐使用 sublime。下面的步骤将使用 Vim 编辑器。

打开文件

在 Xfce 终端中输入 vim circle.py 来启动 Vim 并编辑 circle.py，启动后不要乱按键。

然后按 i 键进入插入模式，此时你可以看到左下角有 “插入” 两个字，现在你可以键入下面的代码了。



第一行

第一行代码输入下面的内容：

#!/usr/bin/env python3
其中第一行的前两个字符 #! 称为 Shebang ，目的是告诉 shell 使用 Python 3 解释器执行其下面的代码。

如果有这行代码，并且给脚本通过 Linux 的 chmod a+x XXX.py 命令增加了执行权限，则可以使用 ./XXX.py 这种方式直接执行脚本，否则需要用 python3 XXX.py 这种方式执行。

模块与引入

由于要计算圆的面积，所以我们需要知道 π 值，就是 3.1415... 这个小数。我们会使用到一个基础库 math 这个基础库中包含大量常用公式和数学相关的处理函数，当然也包含我们需要的 π 值。

输入代码：

from math import pi
这句代码的意思是从 math 库中引入 pi，让当前的文件中可以使用 pi。

计算

使用引入的 π 值，计算半径 5 的圆的面积，相信你还没有忘记圆面积的计算公式，在文本中输入代码：

# calculate
result = 5 * 5 * pi
此处代码中以 # 开始的一行是程序的注释，用来帮助我们阅读和理解代码，良好的注释习惯是能够提高程序的可维护性，哪怕是写的很好的代码，如果没有注释，过一段时间连作者都很难去改动了。

后一行代码中，我们定义了一个变量 result，用来保存 5 * 5 * pi 公式计算的结果。

输出

输出的代码很简单，就是上一节中使用的 print 函数：

print(result)
所有代码

代码合并到一起：

#!/usr/bin/env python3
from math import pi
# calculate
result = 5 * 5 * pi
print(result)
保存代码

然后按 Esc 键退出插入模式，再键入 :wq 回车，Vim 就会保存文件并退出。

执行代码

执行代码有两种方式，一种是先前写的用 python3 命令指定脚本 python3 执行，一种是本节我们将要使用到的直接执行脚本。

要运行脚本文件 circle.py，还要为文件添加可执行权限：

$ chmod +x circle.py
然后执行脚本：

$ ./circle.py
执行脚本的时候前面需要输入 ./ 表示在当前目录下的脚本。

脚本执行的结果如下图所示：



注意的细节

Vim 上手比较困难，如果有难度，请直接使用 sublime 或 gedit 编写代码
Python 代码对空格很关键，这个例子中间所有的代码都要靠最左侧放置，否则就会报错
完整的一个 Python 程序编写操作视频：

您还没有安装flash播放器，请点击这里安装
安装后重启浏览器即可播放视频

This is a modal window.No compatible source was found for this media.
变量与数据类型

变量

编程语言中为了能够更好的处理数据，都需要使用一些变量。Python 语言的变量可以是各种不同的数据类型，使用变量的时候不需要声明直接使用就可以。

变量命名

Python 3 中的变量命名有一定要求，必须要字母及下划线开始，其他符号可以是数字、字母或下划线，命名区分大小写，且不能使用关键字。关键字指的是为 Python 语言预留的单词，例如 import。

可以在交互式环境下使用 keyword 模块查看关键字：



基本数据类型

Python 3 中，包括以下几种基本数据类型：

整数：例如 100，-200，0 等
布尔数：True 或 False
浮点数：小数，例如 1.5，2.5
None：空值，注意与0是不同的，可以理解为未定义的值。
除了这四种之外，还有一些其他不常用的类型，例如复数，但因为用的比较少，这里不做过多介绍。

使用变量及打印

在 XFce 终端中输入 python3，进入交互环境，尝试输入如下的代码，并理解输出的含义，注意执行后不要退出，需要继续下一节的实验内容：

>>> a = 10
>>> b = 10.6
>>> c = True
>>> d = None
>>> print(a,b,c,d)
>>> print(type(a),a)
>>> print(type(b),b)
>>> print(type(c),c)
>>> print(type(d),d)
在上述的代码中，type 是 Python 3 内置的一个函数，用来显示变量的数据类型。



运算

继续在上一节中的 python 3 的交互环境中执行下面的操作，理解 Python 3 中的数学运算：

e = a + b
print(e)
f = b/a
print(f)
g = b - a
print(g)
h = b * a
print(h)
可以看到整数和浮点数的混合计算中，整数会被转换为浮点数。



除了数学运算之外，还有 and 和 or 的逻辑运算：

True and False
True or False
c and False
c or False
and 表示与运算，只有两个运算值都是 True 才返回 True，而 or 表示或运算，有一个为 True 则返回 True。

字符串

Python 3 中的字符串可以使用双引号或单引号标示，如果字符串中出现引号，则可以使用 \ 来去除引号标示字符串的特殊作用。

几种字符串的表示方法：

str1 = "hello"
str2 = 'shiyanlou'
str3 = 'hello, \'shiyanlou\''
str4 = "hello, 'shiyanlou'"
str5 = 'hello, "shiyanlou"'
注意 str4 和 str5 都没有使用 \，但仍然可以在字符串中使用引号，相信你已经发现了原因。

如果需要输入多行字符串，又该如何处理呢？可以尝试使用 """ 三个双引号：

str6 = """ hello, 
shiyanlou """
支持使用 + 连接字符串：

str1 + ' ' + str2
字符串可以使用数字进行索引，数字0为第一个字符，依次类推。数字 -1 为最后一个字符，使用冒号进行切片：

str1
str1[0]
str1[1]
str1[-1]
str1[-2]
str1[:2]
str1[3:]
切片的位置很容易让人迷惑，所以需要多尝试一些切片的方式来理解。

Python 3 中的内置函数 len() 可以获得字符串包括的字符数量：

len(str2)


字符串中有很多常用的方法可以使用，在 Python Shell 中可以使用 help(str) 查看所有的字符串中的方法，这里介绍两个常用的，并且后面的挑战作业中会用到的。

strip()：默认情况下会删除字符串首尾的空格及换行等空白符。如果strip()函数中使用参数则会删除这些参数中的字符（仅限于出现在字符串首尾的情况），例如 str1.strip('ab') 则只会删除 str1 字符串中头尾部的 a 和 b 字符。
split()：默认情况下会用空格将字符串中进行切分得到一个列表，传入参数的时候会用传入的参数对字符串进行切分。
上述两个函数的举例：

>>> str1 = '  shiyanlou  '
>>>
>>> str2 = str1.strip()
>>> str2
'shiyanlou'
>>> str1
'  shiyanlou  '
>>>
>>>
>>> str3 = 'hello shiyanlou'
>>> list1 = str3.split()
>>> list1
['hello', 'shiyanlou']
>>> str3
'hello shiyanlou'
>>>
>>> str4 = 'hello:shiyanlou'
>>> list2 = str4.split(':')
>>> list2
['hello', 'shiyanlou']
>>> str4
'hello:shiyanlou'
>>>
控制结构

我们本节进入到 Python 3 程序的控制结构，包括两部分：选择控制和循环控制。

选择控制

非常多的编程语言都会使用 if 关键字作为流程控制，除此之外，Python 3 的流程控制还包括 elif 和 else 两个关键字，这两个在选择控制中都是可选的。elif 的意思是 else if，增加进一步的判断是否选择该路径。

举例说明，下面的代码：

>>> a = int(input("Please enter: "))
Please enter: 10
>>> if a > 10:
...     print('a > 10')
... elif a == 10:
...     print('a == 10')
... else:
...     print('a < 10')
input("Please enter: ") 这句代码是使用 input 函数获取用户输入，input 中的参数字符串将输出到屏幕上，用户输入的内容会被函数返回，返回的值为字符串。如果不输入，程序将始终阻塞等待。

int(input("Please enter: ")) 将用户的输入的字符串转成整数，并把数字赋值给变量 a。

这个例子中会根据输入的 a 的值不同选择不同的路径，可以将代码写入一个脚本文件中重复执行尝试不同的输入。

这里需要注意写 Python 语言的缩进，Python 的缩进非常严格，不像 C 语言那样使用 { 进行代码块的管理，Python 采用的方法是缩进，同样缩进的代码属于一个代码块，比如 if 或 else 下方的代码块必须保持严格的相同缩进。

缩进的时候一定不要混用空格和TAB，强烈建议只使用空格，为了保持良好的代码风格，建议使用四个空格作为缩进。

程序执行的截图：



循环控制

Python 中包含两种循环方式，一种是 for，一种是 while。

for 循环主要用在依次取出一个列表中的项目，对列表进行遍历处理。下一节中我们将详细讲解列表的数据结构，这里可以简单理解为一组值。

代码示例如下：

strlist = ['hello','shiyanlou','.com']
for s in strlist:
    print(s)


如果需要迭代一组数字列表，并且数字列表满足一定的规律，可以使用内置函数 range()：

for a in range(10):
    print(a)


range() 函数还有很多不同的使用方法，感兴趣可以查看 help 帮助文档。

另外一种循环是 while，while 不同于 for 是使用一个表达式作为判断的条件，如果条件不能够达成则停止循环。

w = 100
while w > 10:
    print(w)
    w -= 10
这里要注意 w -= 10，等同于 w = w - 10。当 w 的值小于等于 10 的时候，循环退出。



我们在循环控制中，可以使用 break 和 continue 两个关键字，break 表示停止当前循环，continue 表示跳过后当前循环轮次中后续的代码，去执行下一循环轮次。

代码示例：

for a in range(10):
    if a == 5:
        break
    print(a)
执行如下图，当 a 为 5 的时候循环退出：



w = 100
while w > 10:
    w -= 10
    if w == 50:
        continue
    print(w)
执行如下图，当 w 为 50 的时候不执行后续的 print 代码：



异常处理

什么是异常

异常处理是工作中编写代码必须要完成的内容，对于不符合预期的用户操作或数据输入，程序总会出现异常情况，而对异常情况能够妥善处理，是保证程序稳定性的关键工作之一。

异常出现的原因非常多，逻辑错误，用户输入错误都会造成异常。

举个例子，告诉我们什么是异常：

filename = input("Enter file path:")
f = open(filename)
print(f.read())
这个简单的程序中我们会用到后续章节中将详细介绍的文件操作，open() 函数打开文件，read() 函数读取文件内容。

首先 input() 函数会读取用户的输入作为文件的路径，如果用户输入的文件不存在会怎么样呢？



会出现文件不存在的异常，并且会发现 Traceback，这就是系统抛出的异常，异常的类型是 FileNotFoundError。

Python 常用的异常类有很多，我们不需要去记住，只需要在收到异常的时候能通过查询文档了解含义。这里介绍几个最常见的异常类：

NameError 访问一个未定义的变量
SyntaxError 语法错误，这个严格讲算是程序的错误
IndexError 对于一个序列，访问的索引超过了序列的范围（序列的概念会在后续实验中讲到），可以理解为我的序列里只有三个元素，但要访问第4个
KeyError 访问一个不存在的字典 Key，字典也会在下一节实验中详细讲到，Key 如果不存在字典就会抛出这个异常
ValueError 传入无效的参数
AttributeError 访问类对象中不存在的属性
异常处理

如果出现了异常，我们不可以直接将异常抛给用户，应该使用 Python 提供的异常处理方法来捕获并处理异常，处理方法为使用 try，except 和 finally 三个关键字。

其中我们把可能出现异常的代码放到 try 代码块，然后在 except 代码块中添加处理异常的方法，回到刚才的文件读取类，我们将 open 和 read 放到 try 代码块中，except 中处理。

代码格式如下：

try:
    有可能抛出异常的代码
except 异常类型名称：
    处理代码
except 异常类型名称：
    处理代码
这里需要注意的是 except 可以有多个，每个处理不同类型的异常，也可以不写任何异常类型名称，则会处理所有捕获的异常。

改进的文件读取程序为：

filename = input("Enter file path:")
try:
    f = open(filename)
    print(f.read())
    f.close()
except FileNotFoundError:
    print("File not found")
当 try 代码块中一旦出现异常，这个代码块后续的代码不会继续执行，会直接进入到 except 异常处理代码块中。

我们把这个程序写到 /home/shiyanlou/fileexc.py 中，然后执行，并输入上面例子中的不存在的文件，这个时候会被 except 捕获并处理。



finally 关键字是用来进行清理工作，经常和 except 一起使用，即无论是正常还是异常，这段代码都会执行。

如果一个文件处理的程序中异常出现在 f.write() 向文件中写入数据的时候，就无法执行 close 操作，使用 finally 可以保证无论 try 代码块中的代码是否抛出异常，都能够执行 finally 代码块里的内容，保证文件被正常关闭。

修改上述的程序如下，改为写入操作，引入 finally 保证文件可以被正常关闭：

filename = '/etc/protocols'
f = open(filename)
try:
    f.write('shiyanlou')
except:
    print("File write error")
finally:
    print("finally")
    f.close()
程序运行的结果：

File write error
finally
表示虽然异常，但仍然执行到了 finally 代码块。

这里需要说明下抛出异常的原因是以只读的模式打开了一个文件，但尝试向文件中写入内容，所以会抛出异常。另外 except: 这个语句后不写任何参数，表示将处理所有 try 代码块中抛出的异常。

抛出异常

如果我们希望在程序中抛出一些异常的时候如何操作呢，可以使用 raise 语句。

raise 异常名称
例如，我们在代码里希望抛出一个 ValueError，直接使用：

raise ValueError()
外部的代码就可以使用 except ValueError 进行捕获和处理了。

模块和包

本节介绍 Python 的模块引入方法，Python 目录和模块之间的关系。

在 Python 中我们可以使用 import XXX 或 from XXX import YYY 这样的形式来引入某个模块或者模块中的某个函数、类等内容到当前的代码文件中。那么 Python 怎么知道去哪里找这些模块呢？

Python 有一个默认的模块搜索路径，包括当前目录及系统中的一些 Python 模块的主要安装目录，可以通过下面的方法查看搜索路径：

>>> import sys
>>> sys.path
每个 XXX.py 文件都是一个 Python 模块，文件的内容会在 import XXX 的时候直接执行。对于文件夹，Python 中可以识别成一个包，前提是这个文件夹中有一个 __init__.py 文件，文件中可以不用写任何内容。例如我们创建一个目录 shiyanlou，在这个目录下有 __init__.py 和 louplus.py 两个代码文件，我们想要引入 louplus.py 文件就可以用 import shiyanlou.louplus 这种代码来引入，前提是 shiyanlou 目录已经放到了 Python 模块搜索的默认路径下了。

命令行参数

命令行参数获取方法是使用 sys 模块的 sys.argv，其中 sys.argv[0] 为脚本名称， sys.argv[1] 为第一个参数，代码示例：

#!/usr/bin/env python3

import sys
print(len(sys.argv))

for arg in sys.argv:
    print(arg)
执行这段代码的过程：

$ python3 argtest.py hello shiyanlou
3
argtest.py
hello
shiyanlou
第一个数字表示命令行参数的数量，后面循环打印每一个参数，第一个为 sys.argv[0] 就是运行的程序文件，从 sys.argv[1] 开始才是程序的参数。

__main__

我们改造上面的程序，将其中的一段for循环代码放入到 if __name__ == '__main__': 中：

#!/usr/bin/env python3

import sys
print(len(sys.argv))

if __name__ == '__main__':
    for arg in sys.argv:
        print(arg)
if __name__ == '__main__': 这一句相当于 C 语言的 main 函数，作为程序执行的入口，实际的作用是让这个程序 python3 argtest.py 这样执行时可以执行到 if __name__ == '__main__': 这个代码块中 for 循环的内容，当通过 import argtest 作为模块导入到其他代码文件时不会执行if __name__ == '__main__':中的内容。

测试刚才的代码如下，引入时显示1表示只有一个 sys.argv[0]，没有任何其他的参数：

$ vim argtest.py
$ python3
Python 3.6.0 (default, Mar  4 2017, 12:32:34)
[GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.42.1)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import argtest
1
>>>
$ python3 argtest.py hello shiyanlou
3
argtest.py
hello
shiyanlou
总结

本节实验没有需要提交到 Github 代码仓库中的代码，如果你觉得有哪些代码需要保存，可以自行提交。后续较大的示例代码、项目实验及挑战的代码我们都会要求你提交到自己的 Github 中保存。

这是楼+实验的第一节，内容比较多，也非常基础。虽然无法把 Python 语法讲解的面面俱到，但已经包含了最常用的内容：

Python 开发环境
变量与数据类型
输入与输出
运算
字符串
控制结构
异常处理
模块和包
命令行参数
__main__

来源: 实验楼
链接: https://www.shiyanlou.com/courses/983
本课程内容，由作者授权实验楼发布，未经允许，禁止转载、下载及非法传播
