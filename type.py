列表、元组、集合与字典
简介

本节实验将学习 Python 3 中非常常用的四种数据结构：列表、元组、集合与字典。

知识点

列表的概念与操作
元组的概念与操作
集合的概念与操作
字典的概念与操作
列表

什么是列表

list（列表）是一种有序的数据集合。

举例说明，在交互式环境中输入下面的内容，其中 courses 就是一个列表：

>>> courses = ['Linux', 'Python', 'Vim', 'C++']
>>> courses.append('PHP')
>>> courses
['Linux', 'Python', 'Vim', 'C++', 'PHP']
首先我们建立了一个列表 courses。然后调用列表的方法 courses.append('PHP') 添加元素 PHP 到列表末尾。你可以看到元素字符串 PHP 已经添加到列表的末端了。

列表中的索引类似 C 语言中数组的访问索引，可以通过索引访问到每一个列表的元素，第一个元素的索引为 0，最后一个元素的索引可以使用 -1 进行标示，这一点与上一节中的字符串的索引完全相同。

>>>
>>> courses[0]
'Linux'
>>> courses[-1]
'PHP'
>>> courses[-2]
'C++'
>>> courses[9]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: list index out of range
超出索引的最大数字范畴，会出现越界，抛出 IndexError 异常，回忆下上一节的异常的内容。

如何知道列表中元素的数量呢，可以使用 len()：

>>> len(courses)
5
列表操作

上面的例子中我们初步接触到列表的最基本操作 append()，列表是有序的，所以 append() 就是在列表的末尾添加新的元素。

有些时候我们需要将数据插入到列表的任何位置，这时我们可以使用列表的 insert() 方法。

>>> courses.insert(0, 'Java')
>>> courses
['Java', 'Linux', 'Python', 'Vim', 'C++', 'PHP']
>>> courses.insert(1, 'Ruby')
>>> courses
['Java', 'Ruby', 'Linux', 'Python', 'Vim', 'C++', 'PHP']
列表方法 count(s) 会返回列表元素中 s 的数量。我们来检查一下 Java 这个元素在列表中出现了多少次。

>>> courses.count('Java')
1
如果你想要在列表中移除任意指定值，你需要使用 remove() 方法。

>>> courses.remove('Java')
>>> courses
['Ruby', 'Linux', 'Python', 'Vim', 'C++', 'PHP']
注意：如果 Java 出现多次，则只有第一个 'Java' 元素会被清除。

另外一种删除元素的方法是使用 del 关键字，这个关键字可以删除列表指定位置的元素，需要使用到列表中要删除元素的索引：

>>> courses
['Ruby', 'Linux', 'Python', 'Vim', 'C++', 'PHP']
>>> del courses[-1]
>>> courses
['Ruby', 'Linux', 'Python', 'Vim', 'C++']
>>> courses.append('PHP')
>>> courses
['Ruby', 'Linux', 'Python', 'Vim', 'C++', 'PHP']
列表是有顺序的，我们在执行所有的列表操作的过程中都要时刻记住这一点，有序的列表可以进行反转：

>>> courses
['Ruby', 'Linux', 'Python', 'Vim', 'C++', 'PHP']
>>> courses.reverse()
>>> courses
['PHP', 'C++', 'Vim', 'Python', 'Linux', 'Ruby']
如果我们有两个列表，想合并到一起，一种方法是将其中一个列表合并到另外一个列表的末尾位置，可以使用 extend()：

>>> new_courses = ['BigData', 'Cloud']
>>> courses.extend(new_courses)
>>> courses
['PHP', 'C++', 'Vim', 'Python', 'Linux', 'Ruby', 'BigData', 'Cloud']
给列表排序，我们使用列表的 sort() 方法，排序的前提是列表的元素是可比较的，例如数字是按照大小进行排序，而字符串则会选择按照字母表的顺序进行排序，在我们的课程列表的例子中，我们先使用该函数默认的排序方法，是按照字母表顺序：

>>> courses
['PHP', 'C++', 'Vim', 'Python', 'Linux', 'Ruby', 'BigData', 'Cloud']
>>> courses.sort()
>>> courses
['BigData', 'C++', 'Cloud', 'Linux', 'PHP', 'Python', 'Ruby', 'Vim']
列表也可以使用 pop() 函数返回最后的一个元素，pop() 在返回元素的同时也会删除这个元素，传入一个参数 i 即 pop(i) 会将第 i 个元素弹出：

>>> courses
['BigData', 'C++', 'Cloud', 'Linux', 'PHP', 'Python', 'Ruby', 'Vim']
>>> c = courses.pop()
>>> c
'Vim'
>>> courses
['BigData', 'C++', 'Cloud', 'Linux', 'PHP', 'Python', 'Ruby']
>>> courses.pop()
'Ruby'
>>> courses.pop()
'Python'
>>> courses
['BigData', 'C++', 'Cloud', 'Linux', 'PHP']
>>> courses.pop(0)
'BigData'
>>> courses
['C++', 'Cloud', 'Linux', 'PHP']
列表操作视频：

您还没有安装flash播放器，请点击这里安装
安装后重启浏览器即可播放视频

This is a modal window.No compatible source was found for this media.
元组

tuple（元组）是一种特殊的列表，不同点是元组一旦创建就不能修改，上述的所有会修改列表内容的操作例如 sort()、append()等对于元组都不再适用:

>>> courses = ('C++', 'Cloud', 'Linux', 'PHP')
>>> courses
('C++', 'Cloud', 'Linux', 'PHP')
>>> courses[0]
'C++'
>>> courses.sort()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'tuple' object has no attribute 'sort'
>>> del courses[0]
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
TypeError: 'tuple' object doesn't support item deletion
在编写程序的时候，元组比列表更安全，如果是只读的数据，尽可能使用元组，另外务必在使用过程中时刻记住元组是不可修改的，但是元组中如果包含可变的数据元素，这些数据元素是可以修改的，例如元组中包含一个列表，这个列表的内容是可以修改的：

>>> new_courses = ('Linux', ['BigData1','BigData2','BigData3'], 'Vim')
>>> new_courses[1]
['BigData1', 'BigData2', 'BigData3']
>>> new_courses[1].append('BigData4')
>>> new_courses
('Linux', ['BigData1', 'BigData2', 'BigData3', 'BigData4'], 'Vim')
最后，需要提醒下如果要创建只有一个元素的元组，是不可以直接使用括号中一个元素的，需要在元素值后面跟一个逗号：

>>> courses = ('Linux')
>>> courses
'Linux'
>>> type(courses)
<class 'str'>
>>> courses = ('Linux',)
>>> courses
('Linux',)
>>> type(courses)
<class 'tuple'>
元组操作视频：

您还没有安装flash播放器，请点击这里安装
安装后重启浏览器即可播放视频

This is a modal window.No compatible source was found for this media.
集合

什么是集合

set（集合）是一个无序不重复元素的数据集，对比列表的区别首先是无序的，不可以使用索引进行顺序的访问，另外一个特点是不能够有重复的数据。

项目开发中，集合主要用在数据元素的去重和测试是否存在。集合还支持一些数学上的运算，例如：union（联合），intersection（交），difference（差）和 symmetric difference（对称差集）。

创建集合的方法比较简单，使用大括号或者 set 函数，需要注意空的集合不能够使用 {} 创建，只能使用 set 函数，因为{} 创建的是一个空的字典 ：

>>> courses = set()
>>> type(courses)
<class 'set'>
>>> courses = {'Linux', 'C++', 'Vim', 'Linux'}
>>> courses
{'Linux', 'Vim', 'C++'}
上面的代码示例中可以看到，多余的 Linux 字符串已经被自动去除。

集合还可以直接由字符串与 set 函数进行创建，会将字符串拆散为不同的字符，并去除重复的字符：

>>> nameset = set('shiyanlou.com')
>>> nameset
{'c', 'o', '.', 'm', 'u', 'h', 's', 'a', 'n', 'i', 'y', 'l'}
集合操作

上一节的例子中我们了解到集合去重的功能，如何进行测试判断是否存在呢？可以使用 in：

>>> 'Linux' in courses
True
>>> 'Python' in courses
False
>>> 'Python' not in courses
True
注意 not in 是一个判断 Python 是否不在集合中的操作。in 操作也适用于列表和元组。

可以使用 add() 向集合中增加元素，使用 remove() 从集合中删除元素，如果元素不存在则抛出 KeyError 异常：

>>> courses
{'Linux', 'Vim', 'C++'}
>>>
>>> courses.add('Python')
>>> 'Python' in courses
True
>>> courses
{'Linux', 'Python', 'Vim', 'C++'}
>>> courses.remove('Python')
>>> 'Python' in courses
False
>>> courses.remove('Python')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'Python'
现在我们尝试两个集合的运算：

>>> set1 = {1,2,3,4}
>>> set2 = {3,4,5,6}
'|' 操作，存在 set1 中或 set2 中的元素，等效于 union 操作：

>>> set1 | set2
{1, 2, 3, 4, 5, 6}
>>> set1.union(set2)
{1, 2, 3, 4, 5, 6}
& 操作，返回即在 set1 又在 set2 的元素：

>>> set1 & set2
{3, 4}
- 返回在 set1 不在 set2 的元素：

>>> set1 - set2
{1, 2}
^ 操作，返回只存在两个集合中的元素：

>>> set1 ^ set2
{1, 2, 5, 6}
集合操作视频：

您还没有安装flash播放器，请点击这里安装
安装后重启浏览器即可播放视频

This is a modal window.No compatible source was found for this media.
字典

dict（字典）是无序的键值对集合。字典中的每一个元素都是一个key 和 一个 value 的组合，key 值在字典中必须是唯一的，因此可以很方便的从字典中使用 key 获得其对应的 value 的值。

创建字典的时候使用大括号，这一点与集合相同，先前我们已经提到 {} 会创建一个空字典，如果非空字典，大括号中的每个元素都是 key:value 这样的写法，现在我们创建一个字典保存课程的ID和名称，ID 作为 key，名称为 value：

>>> coursesdict = {1:'Linux', 2:'Vim'}
>>> coursesdict
{1: 'Linux', 2: 'Vim'}
>>> coursesdict[1]
'Linux'
>>> coursesdict[2]
'Vim'
请注意，字典的 key 并不一定只有数字，可以使用各种不同的类型，例如这样的字典也是合法的：

testdict = {1:2, 'teststr':'shiyanlou.com', 9:[1,2,3]}
在 testdict 中，其中一个 key-value 对是数字1与2，另外一个是两个字符串，还有一个是数字与列表构成的 key-value 对。这些混合在一起使用，尽管看上去毫无意义，但也是可以的。

如果 key 不存在 dict[key] 则会抛出 KeyError，有的时候为了避免这种错误出现，我们会使用 get() 函数获取 key 对应的 value，如果此时 key 不存在则默认返回 None，也可以在 get() 函数中给定一个默认值，如果 key 不存在则返回默认值：

>>> coursesdict[2]
'Vim'
>>>
>>> coursesdict[4]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 4
>>>
>>> coursesdict[2]
'Vim'
>>> coursesdict.get(4)
>>> coursesdict.get(2)
'Vim'
>>> coursesdict.get(4, 'default')
'default'
同 set 一样，字典也可以使用 dict 函数进行创建，参数是一个包含若干个二元组的元组（比较绕，注意括号的数量）：

>>> dict_from_tuple = dict(((1,'Linux'), (2,'Vim')))
>>>
>>> dict_from_tuple
{1: 'Linux', 2: 'Vim'}
注意，字典也是通过 [] 的方式获取值，但与列表不同的是 [] 中的内容是 key，可以为数字或其他类型，并不是列表的索引。字典是无序的，不能够通过索引进行访问。另外还需要注意字典的 key 必须为不可变的类型，列表是不能够当作 key 的。

向字典中增加元素的方法只需要为字典中某一个 key 进行赋值，这个时候如果 key 已经存在则是更新该 key 对应的 value 值，如果不存在则表示向字典中增加该 key:value：

>>> coursesdict[5] = 'Bash'
>>> coursesdict[6] = 'Python'
>>> coursesdict
{1: 'Linux', 2: 'Vim', 5: 'Bash', 6: 'Python'}
从字典中删除一个元素，只需要使用 del 删除，如果 key 不存在则抛出 KeyError：

>>> del coursesdict[1]
>>> del coursesdict[1]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 1
字典中我们可以使用 items() 函数获取所有的字典元素，返回得到的是 dict_items 类型的对象，这个对象可以使用 for 进行遍历，遍历的每个元素都是一个二元组，输入下面的代码的时候，注意 print 前的空格需要手动输入4个，这就是前面实验提到过的Python对缩进的要求：

>>> for key,value in coursesdict.items():
...     print(key,value)
...
2 Vim
5 Bash
6 Python
>>>
此外，我们可以使用 keys() 和 values() 分别只获取字典中的所有 key 或 value 的列表：

>>> coursesdict
{2: 'Vim', 5: 'Bash', 6: 'Python'}
>>> coursesdict.keys()
dict_keys([2, 5, 6])
>>> coursesdict.values()
dict_values(['Vim', 'Bash', 'Python'])
这两个返回的类型都可以使用 for 进行遍历。

字典中也存在 pop(key) 函数，可以返回 key 对应的 value，并将该 key:value 键值对删除：

>>> coursesdict
{2: 'Vim', 5: 'Bash', 6: 'Python'}
>>> coursesdict.pop(2)
'Vim'
>>> coursesdict
{5: 'Bash', 6: 'Python'}
字典操作视频：

您还没有安装flash播放器，请点击这里安装
安装后重启浏览器即可播放视频

This is a modal window.No compatible source was found for this media.
总结

本节实验没有需要提交到 Github 代码仓库中的代码，如果你觉得有哪些代码需要保存，可以自行提交。后续较大的示例代码、项目实验及挑战的代码我们都会要求你提交到自己的 Github 中保存。

本节实验中，我们通过一系列的动手操作，熟悉了列表，元组，集合和字典四种最常用的数据集存储方式，在实际的项目开发中，这四种都非常常用。需要在大量的练习中熟悉它们之间的区别以及应用场景。

列表：可修改有序的数据集合
元组：不可修改的有序的数据集合
集合：无序的不重复的数据集合
字典：无序的存储 key:value 键值对的数据集合

来源: 实验楼
链接: https://www.shiyanlou.com/courses/983
本课程内容，由作者授权实验楼发布，未经允许，禁止转载、下载及非法传播
