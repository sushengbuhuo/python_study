Python 高级特性
简介

Python 语言中有很多高级的用法，这些用法比较难理解，但熟悉后可以极大的提高编程的效率和代码的质量。我们选择其中最常用的几种在本次实验中学习。

知识点

lambda 匿名函数
切片
列表解析
字典解析
迭代器
生成器
yield
装饰器
lambda

Python 通过 lambda 提供了对匿名函数的支持，使用方法很简单，看下面的例子：

>>> double = lambda x: x * 2
>>> double(5)
10
上面的例子中 double 这个变量其实就是一个匿名函数，使用的时候直接 double(x) 就会直接执行函数体内的内容，但这个例子的用法并不是 lambda 最常见的用法。

例子中使用 lambda 定义了一个匿名函数。 lambda 返回值时不需要 return 。lambda 函数通常用在需要传入一个函数作为参数，并且这个函数只在这一个地方使用的情况下，匿名函数一般会作为一个参数传递。

切片（slice)

切片用于获取一个序列（列表或元组）或者字符串的一部份，返回一个新的序列或者字符串，使用方法是中括号中指定一个列表的开始下标与结束下标，用冒号隔开，切片在先前的实验中讲解字符串的时候有介绍过，不只是字符串，列表或元组使用切片也非常常见。

以列表为例：

>>> letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
>>> letters[1:3]
['b', 'c']
下标可以是正数，也可以是负数，letters 下标的对应关系：

 0  1  2  3  4  5  6
 a  b  c  d  e  f  g
-7 -6 -5 -4 -3 -2 -1
所以也可以这样写：

>>> letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
>>> letters[1:-4]
['b', 'c']
省略 start 则默认 start 为 0，省略 end 则默认截取到最后：

>>> letters[:4]
['a', 'b', 'c', 'd']
>>> letters[4:]
['e', 'f', 'g']
可以利用切片返回新列表的特性来复制一个列表：

>>> copy = letters[:]
>>> copy
['a', 'b', 'c', 'd', 'e', 'f', 'g']
切片操作视频：


列表解析（list comprehension）

列表解析（list comprehension），也称为列表推导，是从 Python 2.0 就被添加进来的新特性，提供了一种简单优雅的方式操作列表元素，看下面一个例子：

>>> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# 获取 numbers 中的所有偶数
>>> [x for x in numbers if x % 2 == 0]
[2, 4, 6, 8, 10]
# 对 numbers 的每个数求平方
>>> [x * x for x in numbers]
[1, 4, 9, 16, 25, 36, 47, 84, 81, 100]
Python 中提供了一些高阶级函数例如 map ，filter 以及匿名函数 lambda ，高阶函数的意思是可以把函数作为参数传入，并利用传入的函数对数据进行处理的函数。

上面例子中的操作，我们同样可以借助高阶函数完成：

>>> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
>>> f = filter(lambda x: x % 2 == 0, numbers)
>>> m = map(lambda x: x * x, numbers)
对比这俩种实现，个人觉得使用列表解析更为简洁易读一点。另外，由于使用高阶函数增加了调用函数的开销，以至它的时空效率不如使用列表解析，这就难怪连 Python 的作者也推荐使用列表解析了。

列表解析操作视频：


字典解析（dict comprehension）

理解了列表解析，字典解析就很容易了，就是把列表改为字典，处理的对象是字典中的 key 和 value。直接看例子吧：

>>> d = {'a': 1, 'b': 2, 'c': 3}
>>> {k:v*v for k, v in d.items()}
{'a': 1, 'b': 4, 'c': 9}
需要注意的是字典是不能被迭代的，需要使用字典的方法 items() 把字典变成一个可迭代对象。

迭代器

如果学过设计模式中的迭代器模式，那么就能容易理解这个概念。要理解迭代器，首先明白迭代器和可迭代对象的区别。一个一个读取、操作对象称为迭代，Python 中，可迭代（Iterable）对象就是你能用 for…in 迭代它的元素，比如列表是可迭代的：

>>> letters = ['a', 'b', 'c']
>>> for letter in letters:
...     print(letter)
...
a
b
c
>>>
而迭代器是指，你能要用 next 函数不断的去获取它的下一个值，直到迭代器返回 StopIteration异常。所有的可迭代对象都可以通过 iter 函数去获取它的迭代器，比如上面的 letters 是一个可迭代对象，那么这样去迭代它：

>>> letters = ['a', 'b', 'c']
>>> it = iter(letters)
>>> next(it)
'a'
>>> next(it)
'b'
>>> next(it)
'c'
>>> next(it)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
所有的可迭代对象其实是实现了 __iter__ 和 __next__ 这俩个魔法方法，iter 与 next 函数实际上调用的是这两个魔法方法，上面的例子背后其实是这样的：

>>> letters = ['a', 'b', 'c']
>>> it = letters.__iter__()
>>> it.__next__()
'a'
>>> it.__next__()
'b'
>>> it.__next__()
'c'
>>> it.__next__()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
总结下：

能被 for 循环访问的都是可迭代的对象，能被 next() 函数获取下一个值的是迭代器。

迭代器示例视频：


生成器

上面已经介绍了可迭代对象和迭代器的概念，生成器首先它是一个迭代器，不同的是，生成器只能被迭代一次，因为每次迭代的元素不是像列表元素一样，已经在内存中，而是你每迭代一次，它生成一个元素。

创建一个生成器并迭代：

>>> g = (x**x for x in range(1, 4))
>>> g
<generator object <genexpr> at 0x10d1a5af0>
>>> for x in g:
...     print(x)
...
1
4
27
和列表解析有点像，只不过使用的是圆括号。不同于列表可以反复迭代，迭代完一次之后再迭代这个生成器，它不会打印元素，也不回报错。

使用生成器有什么好处呢？因为生成器不是把所有元素存在内存，而是动态生成的，所以当你要迭代的对象有非常多的元素时，使用生成器能为你节约很多内存，这是一个内存友好的特性。

yield

yield 的使用方法和 return 类似。不同的是，return 可以返回有效的 Python 对象，而 yield 返回的是一个生成器，函数碰到 return 就直接返回了，使用了 yield 的函数，到 yield 返回一个元素，当再次迭代生成器时，会从 yield 后面继续执行，直到遇到下一个 yield 或者函数结束退出。

下面是一个迭代斐波那次数列前 n 个元素的列子：

>>> def fib(n):
...     current = 0
...     a, b = 1, 1
...     while current < n:
...         yield a
...         a, b = b, a + b
...         current += 1
...
上面的函数使用了 yield 返回的是一个生成器。如果我们要迭代斐波那次数列的前 5 个元素，先调用函数返回的是一个生成器：

>>> f5 = fib(5)
>>> f5
<generator object fib at 0x10d1a5888>
迭代：

>>> for x in f5:
...     print(x)
...
1
1
2
3
5
装饰器

装饰器可以为函数添加额外的功能而不影响函数的主体功能。在 Python 中，函数是第一等公民，也就是说，函数可以做为参数传递给另外一个函数，一个函数可以将另一函数作为返回值，这就是装饰器实现的基础。装饰器本质上是一个函数，它接受一个函数作为参数。看一个简单的例子，也是装饰器的经典运用场景，记录函数的调用日志：

>>> from datetime import datetime
>>> def log(func):
...     def decorator(*args, **kwargs):
...         print('Function ' + func.__name__ + ' has been called at ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
...         return func(*args, **kwargs)
...     return decorator
...
>>> @log
... def add(x, y):
...     return x + y
...
>>> add(1, 2)
Function add has been called at 2017-08-29 13:11:48
3
@ 是 Python 提供的语法糖，语法糖指计算机语言中添加的某种语法，这种语法对语言的功能并没有影响，但是更方便程序员使用。

上面的代码中 *arg 和 **kwargs 都是 Python 中函数的可变参数。 *args 表示任何多个无名参数，是一个元组，**kwargs 表示关键字参数，是一个字典。这两个组合表示了函数的所有参数。如果同时使用时，*args 参数列要在 **kwargs 前。

它等价于进行了下面的操作：

>>> def add(x, y):
...     return x + y
...
>>> add = log(add)
>>> add(1, 2)
Function add has been called at 2017-08-29 13:16:02
3
也就是说，调用了 log 函数，把 add 函数作为参数，传了进去。log 函数返回了一个另外一个函数 decorator ，在这个函数中，首先打印了日志信息，然后回调了传入的 func ，也就是 `add｀ 函数。

你可能已经发现了，执行完 add = log(add) ，或者说用 @log 装饰 add 后，add 其实已经不再是原来的 add 函数了，它已经变成了log 函数返回的 decorator 函数：

>>> add.__name__
'decorator'
这也是装饰器带来的副作用，Python 提供了方法解决这个问题：

>>> from functools import wraps
>>> def log(func):
...     @wraps(func)
...     def decorator(*args, **kwargs):
...         print('Function ' + func.__name__ + ' has been called at ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
...         return func(*args, **kwargs)
...     return decorator
...
>>> @log
... def add(x, y):
...     return x + y
...
>>> add.__name__
'add'
装饰器的应用场景非常多，我们后续学习 Flask Web 开发的时候会大量使用装饰器来实现 Web 页面的路由等功能。

装饰器操作视频：


总结

本节实验中学习了 Python 编程语言的一些常用的高级用法，这些高级用法需要在项目实际开发的场景中才能够融会贯通，单纯从字面意思很难理解。实验中包括了下面知识点：

lambda：匿名函数
切片：序列和字符串的子序列
列表解析：不用 for 也能操作列表元素
字典解析：不用 for 也能操作字典元素
迭代器：一个个读取元素的对象
生成器：只能被迭代一次的迭代器
yield：返回生成器的 return
装饰器：对函数进行修饰
