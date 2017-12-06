函数
函数概念

什么是函数

我们经常需要在同一个程序里多次复用相同的代码，函数可以很好的帮助我们完成这一点。我们在函数里写我们要重复做的事，然后我们在任何需要的时候调用它。函数有参数和返回值，在函数内部对参数进行处理，并把处理结果返回给调用者。

内置函数

内置函数就是 Python 解释器中不用引入任何包，一直可以使用的函数。我们已经在前面的实验中用到了一些内置的函数，比如 len()，type()。

Python 3 的内置函数列表及说明可以见文档 https://docs.python.org/3/library/functions.html。

在项目开发中，最常使用的仍然是自己定义的函数。

知识点

函数的概念
函数的定义与调用
变量作用域
参数传递方法
默认参数
可变长度参数
函数中修改参数值
定义和调用

我们使用关键字 def 来定义一个函数，定义函数后需要在函数名的括号中写上参数，最后加:，再换行输入函数内部的代码，注意函数内部代码的缩进：

def functionname(params):
    statement1
    statement2
我们写一个函数接受一个字符串和一个字母作为参数，并将字符串中出现的该字母的数量作为返回值，回忆下先前的知识，我们提到过字符串是一个特殊的列表，列表中可以使用 count() 函数返回指定元素的数量。

>>> def char_count(str, char):
...     return str.count(char)
...
第二行的 return 关键字，我们把 str 中包含 char 的次数返回给调用者。

如何使用函数呢，我们必须像下面这样调用这个函数。

>>> char_count('shiyanlou.com', 'o')
2
>>> result = char_count('shiyanlou.com', 's')
>>> result
1
其中，result 变量用来保存函数的返回值，传入的两个参数分别是用来检测的字符串和字母。

现在我们希望改变这个 char_count() 函数，接受一个参数，并将所有的字母及出现的频次打印出来，这个程序我们实现在一个 Python 脚本文件中。

首先使用 sublime 或 vim 等编辑器创建文件，在 Xfce 终端中输入下面的命令：

$ vim count_str.py
依此输入下面的代码：

#!/usr/bin/env python3

def char_count(str):
    char_list = set(str)
    for char in char_list:
        print(char, str.count(char))

if __name__ == '__main__':

    s = input("Enter a string: ")

    char_count(s)
输入后保存并执行程序，程序会要求你输入一个字符串，并将打印出当前字符串中所有字符出现的频次。

$ python3 count_str.py
Enter a string: shiyanlou.com
a 1
i 1
c 1
y 1
h 1
l 1
o 2
. 1
u 1
s 1
n 1
m 1
现在我们详细说下这个程序：

第一行的内容是说明需要使用 Python 3 的解释器执行当前的脚本
函数 char_count 没有返回值，就是没有 return 关键字，这是允许的，返回值和参数对于函数都是可选的
char_count 中首先使用集合获得字符串中所有不重复的字符集
然后再使用 for 对集合进行遍历，每个字符都使用上一个例子中用到的 str.count() 计算频次
最后函数中使用 print 打印字符和对应的频次
if __name__ == '__main__': 这一句相当于 C 语言的 main 函数，作为程序执行的入口，实际的作用是让这个程序 python3 count_str.py 这样执行时可以执行到 if __name__ == '__main__': 这个代码块中的内容，当通过 import count_str 作为模块导入到其他代码文件时不会执行if __name__ == '__main__':中的内容。
另外，需要注意的是这是一个效率低下的程序，你发现了吗？另外是否有改进的思路？欢迎在 QQ 群中与团队和助教讨论。这里是参考答案链接，供参考：https://www.shiyanlou.com/questions/45207。

变量作用域

我们通过几个例子来弄明白局域或全局变量，首先我们在函数内部和函数调用的代码中都使用同一个变量 a：

#!/usr/bin/env python3
def change():
    a = 90
    print(a)
a = 9
print("Before the function call ", a)
print("inside change function", end=' ')
change()
print("After the function call ", a)
运行程序：



首先我们对 a 赋值 9，然后调用更改函数，这个函数里我们对 a 赋值 90，然后打印 a 的值。调用函数后我们再次打印 a 的值。

当我们在函数里写 a = 90 时，它实际上创建了一个新的名为 a 的局部变量，这个变量只在函数里可用，并且会在函数完成时销毁。所以即使这两个变量的名字都相同，但事实上他们并不是同一个变量。

那么如果我们先定义 a，在函数中是否可以直接使用呢？现在我们使用 global 关键字，对函数中的 a 标志为全局变量，让函数内部使用全局变量的 a，那么整个程序中出现的 a 都将是这个：

#!/usr/bin/env python3
a = 9
def change():
    global a
    print(a)
print("Before the function call ", a)
print("inside change function", end=' ')
change()
print("After the function call ", a)
程序中的 end=' ' 参数表示，print 打印后的结尾不用换行，而用空格。默认情况下 print 打印后会在结尾换行。

程序执行的结果，不会报错了，因为函数体内可以访问全局的变量 a：

Before the function call  9
inside change function 9
After the function call  9
那如果在函数内使用 global 会有什么作用呢？尝试下面的代码：

#!/usr/bin/env python3
def change():
    global a
    a = 90
    print(a)
a = 9
print("Before the function call ", a)
print("inside change function", end=' ')
change()
print("After the function call ", a)
程序执行的结果：

Before the function call  9
inside change function 90
After the function call  90
这里通过关键字 global 来告诉 a 的定义是全局的，因此在函数内部更改了 a 的值，函数外 a 的值也实际上更改了。

运行程序：



变量作用域讲解视频：

您还没有安装flash播放器，请点击这里安装
安装后重启浏览器即可播放视频

This is a modal window.No compatible source was found for this media.
参数传递

Python 函数中的参数传递有几个问题必须要特别小心，这也是很容易出现 BUG 的地方：

参数的顺序，如果没有使用参数名传递参数，那么参数的顺序必须要符合函数的定义
函数调用时没有传递的参数使用默认参数值
使用参数名传递参数
可变长度的参数
函数中修改参数值
现在我们依次说明。

参数的顺序及参数名传参

这一点比较简单，函数中的参数顺序是定义的时候指定的。如果不按照顺序传参数，必须使用参数名进行传参。

参数名传参也叫关键字参数，函数可以通过关键字参数的形式调用，例如 keyword = value。

举例说明，在交互环境中，实现一个连接服务器的程序，需要给出服务器的 IP 地址和端口号作为参数：

>>> def connect(ipaddress, port):
...     print("IP: ", ipaddress)
...     print("Port: ", port)
...
>>> connect('192.168.1.1', 22)
IP:  192.168.1.1
Port:  22
>>> connect(22, '192.168.1.1')
IP:  22
Port:  192.168.1.1
>>> connect(port=22, ipaddress='192.168.1.1')
IP:  192.168.1.1
Port:  22
>>>
上面的例子中分别尝试了三次传参，第一次使用默认的顺序，第二次使用错误的顺序，第三次虽然顺序错误但使用了参数名传参。

我们也能将函数的参数标记为只允许使用参数名传递参数。用户调用函数时将只能对每一个参数使用相应的参数名，如果不使用则会抛出 TypeError：

>>> def hello(*, name='User'):
...     print("Hello", name)
...
>>> hello('shiyanlou')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: hello() takes 0 positional arguments but 1 was given
>>> hello(name='shiyanlou')
Hello shiyanlou
默认参数值

函数的参数变量可以有默认值，也就是说如果我们对指定的参数变量没有给出任何值则会赋其默认值，改变上面的程序，使用默认的端口号 22：

>>> def connect(ipaddress, port=22):
...     print("IP: ", ipaddress)
...     print("Port: ", port)
...
这表示如果调用者未给出 port 的值，那么 port 的值默认为 22。这是一个关于默认参数的非常简单的例子。

你可以通过调用函数测试代码。

>>> connect('192.168.1.1', 2022)
IP:  192.168.1.1
Port:  2022
>>> connect('192.168.1.1')
IP:  192.168.1.1
Port:  22
>>>
有两个非常重要的地方，第一个是具有默认值的参数后面不能再有普通参数，比如 f(a,b=90,c) 就是错误的。

第二个是默认值只被赋值一次，因此如果默认值是任何可变对象时会有所不同，比如列表、字典或大多数类的实例。例如，下面的函数在后续调用过程中会累积（前面）传给它的参数:

>>> def f(a, data=[]):
...     data.append(a)
...     return data
...
>>> print(f(1))
[1]
>>> print(f(2))
[1, 2]
>>> print(f(3))
[1, 2, 3]
要避免这个问题，你可以像下面这样：

>>> def f(a, data=None):
...     if data is None:
...         data = []
...     data.append(a)
...     return data
...
>>> print(f(1))
[1]
>>> print(f(2))
[2]
这里的区别体现在执行第二次的时候，如果默认 data = [] 第二次的 data 默认值会包含第一次的结果，所以造成每次默认值是不同的。而第二个函数就没有这个问题。

默认参数值讲解视频：

您还没有安装flash播放器，请点击这里安装
安装后重启浏览器即可播放视频

This is a modal window.No compatible source was found for this media.
可变长度的参数

如果一个函数传入的参数数量不固定，可能是1个也可能是N个，如何处理？

例如我们要计算传递的所有数字的和，那么传递的方法可以是直接传入一个列表或元组（此处不改变值，元组更合适），或者传递可变的多个参数。

可变参数的使用方法是在参数列表前加上 *，举例说明，我们的 connect 函数要连接目标服务器多个端口号：

>>> def connect(ipaddress, *ports):
...     print("IP: ", ipaddress)
...     for port in ports:
...         print("Port: ", port)
...
调用的时候可以传递 0 个或多个端口号做参数：

>>> connect('192.168.1.1')
IP:  192.168.1.1
>>>
>>> connect('192.168.1.1', 22, 23, 24)
IP:  192.168.1.1
Port:  22
Port:  23
Port:  24
>>> connect('192.168.1.1', 22)
IP:  192.168.1.1
Port:  22
可变长度的参数讲解视频：

您还没有安装flash播放器，请点击这里安装
安装后重启浏览器即可播放视频

This is a modal window.No compatible source was found for this media.
函数中修改参数值

在函数中是否可以改变传递的参数的值？

在 C/C++ 语言中有传值和传引用（指针）的概念，直接影响到函数是否能够改变参数的值。

函数参数传值的意思是函数调用过程中，在函数内部使用到的参数只是一个局部变量，在函数执行结束后就销毁了。不影响调用该函数的外部参数变量的值。

函数参数传引用的意思是传递给函数的参数就是外部使用的参数，函数执行过程中对该参数进行的任何修改都会保留，当函数调用结束后，这个参数被其他代码使用中都是函数修改过后的数据。

但在 Python 中情况有些不同，Python 函数的参数是没有类型的，可以传递任意类型的对象作为参数。但不同类型的参数在函数中修改的话，表现也不一样。

举例说明：

#!/usr/bin/env python3

def connect(ipaddress, ports):
    print("IP: ", ipaddress)
    print("Ports: ", ports)
    ipaddress = '10.10.10.1'
    ports.append(8080)

if __name__=="__main__":
    ipaddress = '192.168.1.1'
    ports = [22,23,24]
    print("Before connect:")
    print("IP: ", ipaddress)
    print("Ports: ", ports)
    print("In connect:")
    connect(ipaddress, ports)
    print("After connect:")
    print("IP: ", ipaddress)
    print("Ports: ", ports)
执行这个程序的输出结果：

Before connect:
IP:  192.168.1.1
Ports:  [22, 23, 24]
In connect:
IP:  192.168.1.1
Ports:  [22, 23, 24]
After connect:
IP:  192.168.1.1
Ports:  [22, 23, 24, 8080]
可以发现在函数中改变了 ipaddress 的值没有起到效果，但 ports 列表的值却改变了。

Python 中的对象有不可变对象，指的是数值、字符串、元组等，和可变对象，指的是列表、字典等。如果是不可变对象作为参数，相当于是值的传递，函数中对该参数的修改不会保留。如果是可变对象，则相当于传引用，函数中的修改会保留。

函数中修改参数值讲解视频：

您还没有安装flash播放器，请点击这里安装
安装后重启浏览器即可播放视频

This is a modal window.No compatible source was found for this media.
总结

本节实验没有需要提交到 Github 代码仓库中的代码，如果你觉得有哪些代码需要保存，可以自行提交。后续较大的示例代码、项目实验及挑战的代码我们都会要求你提交到自己的 Github 中保存。

经过本实验应当知道如何定义函数，局域变量和全局变量一定要弄清楚，参数默认值、传递参数的各种情况也需要掌握。

另外，其它高级语言常见的函数重载，Python 是没有的，这是因为 Python 有默认参数这个功能，函数重载 的功能大都可以使用默认参数达到。

来源: 实验楼
链接: https://www.shiyanlou.com/courses/983
本课程内容，由作者授权实验楼发布，未经允许，禁止转载、下载及非法传播
