面向对象编程
简介

面向对象编程（Object Oriented Programming，OOP，面向对象程序设计）是一种程序设计思想。以面向过程思想设计程序时，程序是一条条指令的顺序执行，当指令变得多起来时，它们被分隔成我们先前实验中讲解过的函数。而面向对象思想则是对象视为程序的组成单元，程序的执行通过调用对象提供的接口完成。

面向对象的概念不容易通过理论讲解来理解，后续项目实战中我们会大量用到面向对象的思想，本节内容为后续实战做一定的铺垫，不会涉及太深入的内容。

面向对象的 4 个核心概念：

抽象
封装
继承
多态
下面我们通过例子和代码来理解这四个概念以及如何在 Python 中运用。

知识点

面向对象编程思想
抽象
封装、类与实例
继承与方法重写
多态
私有属性和方法
静态变量与类方法
property
从面向过程说起

有这样一句话：

“有一条叫旺财的狗和一只叫 Kitty 的猫在叫，旺财发出 wang wang wang … 的叫声，Kitty 发出 miu miu miu 的叫声 …”
如果要把这句话转化为程序语言，使用面向过程的方法，可能会写出下面的代码，注意这部分示例不可以执行，只是讲解面向过程的编程方法：

main() {
    dog_name = '旺财';
    dog_sound = 'wang wang wang...';
    cat_name = 'Kitty';
    cat_sound = 'miu miu miu...';
    print(dag_name + ' is making sound ' + dog_sound);
    print(cat_name + ' is making sound ' + cat_sound);
}
执行结果会是：

旺财 is making sound wang wang wang...
Kitty is making sound miu miu miu...
这基本上就是面向过程的代码风格。

抽象

如何以面向对象的思想来写上面的程序呢？首先要做抽象。抽象就是对特定实例抽取共同的特征及行为形成一种抽象类型的过程。

在上面的程序中，“旺财”是狗的一种，它有一个名字，它可以“wang wang wang…” 的叫，我们可以抽象出这样一种类型，狗：

dog {
  name(特征)
  bark()(行为)
}
同理，对于 Kitty，可以抽象为猫，猫也有名字，不过它的行为（叫声）和狗不同：

cat {
  name(特征)
  mew()(行为)
}
特征和行为在程序语言中通常被称为属性（Attribute）和方法（Method)。

封装、类与实例

在面向对象的语言中，封装就是用类将数据和基于数据的操作封装在一起，隐藏内部数据，对外提供公共的访问接口。

将上面的抽象转化为 Python 程序：

class Dog(object):
    def __init__(self, name):
        self._name = name
    def get_name(self):
        return self._name
    def set_name(self, value):
        self._name = value
    def bark(self):
        print(self.get_name() + 'is making sound wang wang wang...')

class Cat(object):
    def __init__(self, name):
        self._name = name
    def get_name(self):
        return self._name
    def set_name(self, value):
        self._name = value
    def mew(self):
        print(self.get_name() + 'is making sound miu miu miu...')
object 是 Python 中所有对象的祖先，它是所有类的基类。类需要一个初始化方法，__init__ 是 Python 的初始化方法，注意前后各有两个下划线 _，self指代当前的对象。

类是一个抽象的概念，而实例是一个具体的对象。比如说狗是一个抽象的概念，因为狗有很多种，而那个正在 wang wang 叫的叫旺财的狗是一个实例。

面向对象风格的主程序就变成这样：

# 在 Python 实例化一个对象
dog = Dog('旺财')
cat = Cat('Kitty')
dog.bark()
cat.mew()
Dog 类中的 bark 方法实现了狗叫的信息输出，但使用这个方法需要先用 Dog() 创建一个对象。

隐藏数据访问有什么好处呢？最大的好处就是提供访问控制。比如在 Cat 类中，用户输入名的可能有小写，有大写，而我们希望对外提供的名词都是首字母大写，其余字母小写，那么我们就可以在 get_name 方法中做访问控制：

def get_name(self):
    return self._name.lower().capitalize()
封装成类操作视频：

您还没有安装flash播放器，请点击这里安装
安装后重启浏览器即可播放视频

This is a modal window.No compatible source was found for this media.
注意：视频中有一部分描述不准确，在 Python 的类中，__init__() 函数是在对象创建中执行的，并不是用来创建对象的必备函数，创建对象的实际函数是 __new__()，而 __new__() 是继承自 object 类所具备的函数，此处可以不必重新实现，并且在 __new__() 中甚至可以指定是否执行 __init__()。

继承与方法重写

将“旺财”抽象为狗，“Kitty”抽象为猫，这是显而易见的，以至于你可能都没察觉到已经完成了一层抽象。对狗和猫还可以做进一步的抽象：它们都是动物，它们都有一个名字，它们都能发出叫声，只是叫声不同。这样我们就形成了一个抽象类：

class Animal(object):
    def __init__(self, name):
        self._name = name
    def get_name(self):
        return self._name
    def set_name(self, value):
        self._name = value
    def make_sound(self):
        pass
因为每一种动物发出的声音不同，所以在抽象类中并没有实现 make_sound 方法，使用 pass 直接略过这个函数，不做任何事情。

狗和猫都是动物，它们之间就形成了一种继承关系，用 Python 语言表示出来就是：

class Dog(Animal):
    def make_sound(self):
        print(self.get_name() + ' is making sound wang wang wang...')


class Cat(Animal):
    def make_sound(self):
        print(self.get_name() + ' is making sound miu miu miu...')
Dog 和 Cat 继承了父类 Animal 的初始化方法，get_name 和 set_name 方法，并重写了父类的 make_sound 方法。

现在主程序变成：

dog = Dog('旺财')
cat = Cat('Kitty')
dog.make_sound()
cat.make_sound()
继承操作视频：

您还没有安装flash播放器，请点击这里安装
安装后重启浏览器即可播放视频

This is a modal window.No compatible source was found for this media.
多态

简单的说，多态就是使用同一方法对不同对象可以产生不同的结果。

下面我们通过一个例子来说明，为了方便说明，假设我们在使用的是一门类似 Java 的强类型语言，使用变量前必须声明类型。

假设现在又来了一只叫“来福”的狗和一只叫“Betty”的猫，它们也在叫，那么我们可能会写出这样的代码：

# 伪代码
Dog dog1 = new Cat('旺财');
Cat cat1 = new Cat('Kitty');
Dog dog2 = new Dog('来福');
Dog cat2 = new Cat('Betty');
dog1.make_sound();
cat1.make_sound();
dog2.make_sound();
cat2.make_sound();
Dog 和 Cat 都继承自 Animal，并且实现了自己的 make_sound 方法，那么借助强类型语言父类引用可以指向子类对象这一特性，我们可以写出多态的代码：

# 伪代码
Set animals = [new Dog('旺财'), new Cat('Kitty'), new Dog('来福'), new Cat('Betty')];
Animal animal;
for (i = 0; i <= animals.lenth(); i++) {
    # 父类引用指向子类对象
    animal = animals[i];
      # 多态
    animal.make_sound();
}
在 Python 这种动态类型的语言中可能没有那么明显的体现多态的威力，因为在 Python 中，你可以用任意变量指向任意类型的值。上面过程用 Python 来写的话会非常简单：

animals = [Dog('旺财'), Cat('Kitty'), Dog('来福'), Cat('Betty')]
for animal in animals:
    animal.make_sound()
可以看到不管 animal 具体是 Dog 还是 Cat，都可以在 for 循环中执行 make_sound 这个方法。这就是面向对象的多态性特征。

多态示例操作视频：

您还没有安装flash播放器，请点击这里安装
安装后重启浏览器即可播放视频

This is a modal window.No compatible source was found for this media.
私有属性和方法

在 Java 和 C++ 中，可以用 private 和 protected关键字修饰属性和方法，它们控制属性和方法能否被外部或者子类访问，在 Python 中约定在属性方法名前添加 __ （两个下划线 _）来拒绝外部的访问。

>>> class Shiyanlou:                                                                                                                                                                                                
...   __private_name = 'shiyanlou'                                                                                                                                                                                
...   def __get_private_name(self):                                                                                   
...     return self.__private_name                                                                                    
...                                                                                                                   
>>> s = Shiyanlou()                                                                                                                                                                                                                
>>> s.__private_name                                                                                                  
Traceback (most recent call last):                                                                                    
  File "<stdin>", line 1, in <module>                                                                                 
AttributeError: 'Shiyanlou' object has no attribute '__private_name'                                                                                                                                                               
>>> s.__get_private_name()                                                                                            
Traceback (most recent call last):                                                                                    
  File "<stdin>", line 1, in <module>                                                                                 
AttributeError: 'Shiyanlou' object has no attribute '__get_private_name'
为什么说是“约定”，因为 Python 中不是绝对的私有，还是通过 obj._Classname__privateAttributeOrMethod 来访问：

>>> s._Shiyanlou__private_name                                                                                        
'shiyanlou'
>>> s._Shiyanlou__get_private_name()                                                                                  
'shiyanlou'
所以说 __ 只是约定，告诉外部使用者不要直接使用这个属性和方法。

静态变量和类方法

静态变量和类方法是可以直接从类访问，不需要实例化对象就能访问。假设上面例子中的动物它们都是 Jack 养的，那么就可以在 Animal 类中用一个静态变量表示，一般声明在 __init__ 前面：

class Animal(object):
    owner = 'jack'
    def __init__(self, name):
        self._name = name
现在可以通过 Animal 或者子类直接访问

print(Animal.owner)  # 'jack'
print(Cat.owner)  # 'jack'
类方法和静态变量类似，它也可以通过类名直接访问，类方法用 @classmethod 装饰，类方法中可以访问类的静态变量，下面添加了一个类方法 get_owner：

class Animal(object):
    owner = 'jack'
    def __init__(self, name):
        self._name = name
    @classmethod
    def get_owner(cls):
        return cls.owner
注意类方法的第一个参数传入的是类对象，而不是实例对象，所以是 cls。

通过类方法获取 owner:

print(Animal.get_owner())  # 'jack'
print(Cat.get_owner())  # 'jack'
静态变量和类方法操作视频：

您还没有安装flash播放器，请点击这里安装
安装后重启浏览器即可播放视频

This is a modal window.No compatible source was found for this media.
property

在 Python 中，property 可以将方法变成一个属性来使用，借助 property 可以实行 Python 风格的 getter/setter，即可以通过 property 获得和修改对象的某一个属性。

用 property 改写的 Animal 类：

class Animal(object):
    def __init__(self, name):
        self._name = name
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value
    def make_sound(self):
        pass
这样我们就能以访问属性的方式获取 name 了：

cat = Cat('Kitty')
print(cat.name)
静态方法

静态方法用 @staticmethod 装饰，和 classmethod 有点类似。staticmethod 在运行时不需要实例的参与，它被放在类下面只是因为它和类有一点关系，但并不像类方法那样需要传递一个 cls 参数。

静态方法的应用场景是当一个函数完全可以放到类外面单独实现的时候，如果这个函数和类还有一点联系，那么放入类中能更好的组织代码逻辑，那么可以考虑使用类中的静态方法。

比如说，Animal 下面有一个方法，主人 Jack 可以调用它来购买小动物的食物：

class Animal(object):
    owner = 'jack'
    def __init__(self, name):
        self._name = name

    @staticmethod
    def order_animal_food():
        print('ording...')
        print('ok')
调用静态方法的方式如下：

Animal.order_animal_food()
总结

本节实验通过几个例子学习了面向对象的 4 个核心概念：

抽象
封装
继承
多态

来源: 实验楼
链接: https://www.shiyanlou.com/courses/983
本课程内容，由作者授权实验楼发布，未经允许，禁止转载、下载及非法传播
