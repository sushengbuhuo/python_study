Flask 入门
简介

本节实验开始的实验环境进行了一些优化，因此第一周保存的环境不能继续使用。若你保存了第一周的环境，请重新选择默认在线实验环境。
Flask 是 Python 社区比较知名的微框架。Flask 被设计成可以通过插件拓展，Flask 本身只维护一个核心。如果要和 Django 做对比的话，Django 更像一个大品牌的出的电脑整机，你不用操心使用什么配件，你需要什么 Django 全家桶都有。而 Flask 可以说是一个组装机了，更准确的说是一个设计精良的 CPU。这给了你很大的灵活性去选择需要的配件（插件）。

知识点

Flask 简介
配置方法
注册路由
模板渲染
request 对象
session
cookies
错误处理
插件
简单的例子

一个最简单的例子，创建 app.py，写入：

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
Flask 提供了一个管理 Flask 应用的命令行工具，首先要设置应用的环境变量：

export FLASK_APP=app.py
export FLASK_DEBUG=1
环境变量 FLASK_APP 是用来指向 flask run 执行的 Flask 应用代码的路径，这里是 app.py 的路径。FLASK_DEBUG=1 表示打开 DEBUG 信息，可以输出访问和出错信息，帮助我们解决代码中出现的问题，建议后续只要执行 flask run 都要打开 FLASK_DEBUG。

然后就可以这样运行 Flask 应用了：

flask run
默认地，应用运行在 localhost:5000 上。打开浏览器，访问这个地址就能看到返回的 Hello World! 了。

Flask 简单示例开发视频：

Play Video

flask shell

除了 flask run 之外，还有一个常用的命令是 flask shell，这两个命令都会自动把 FLASK_APP 环境变量中指定的代码模块进行加载，不同的是 flask run 直接进入到运行 app 的状态，而 flask shell 只加载并进入到一个 Shell 终端，在这个终端中可以执行一些代码，比如后续章节中要用到的初始化数据库，向数据库中插入一些数据等。

$ flask shell
>
配置

初始化一个 Flask app 后，可以通过 app.config 管理配置。app.config 存储的配置信息本质上是个字典，所以你可以用字典的方法添加或者更新配置。比如说，初始化 app 后，配置一个密钥：

app = Flask(__name__)
app.config.update({
      'SECRET_KEY': 'a random string' 
})
所有的配置选项需要用大写，多个单词间用下划线 _连接。大型项目中，配置通常写在一个单独的 config.py 文件中，这时候就可以用 app.config 提供的特有方法来更新 config，参数是配置文件 config.py 的路径：

app.config.from_pyfile('path/to/config.py')
其他类似的方法：

from_envvar(variable_name)：使用一个环境变量指定的配置文件更新配置
from_object(obj)：使用一个对象更新配置文件，dict 无效
from_json(filename)：使用 JSON 文件更新配置
from_mapping(*mapping, **kwargs)：类似前面的 update，不同的是，这个方法不强制使用大写字母
获得一个配置信息的方法是用字典的形式 app.config['SECRET_KEY'] 这样可以获得 SECRET_KEY 的配置值。

注册路由

Flask 使用 @app.route 装饰器来注册路由及其处理函数。在上面的例子中，就用主页 / 注册一个路由，访问主页 Flask 会用 index 函数去处理。

可以在路由中传入变量，格式为 <variable_name>，比如每个用户的主页需要不同的路由，可以使用用户名作为路由的变量：

@app.route('/user/<username>')
def user_index(username):
    # 在函数中指名变量名称，这样就能获取到通过路由传入的变量值
    return 'Hello {}'.format(username)
也可以指定路由变量的类型，比如说，一个博客应用的每个博文页面可以用这篇博文的 ID 作为路由变量，ID 应该是个 int 类型的值：

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post {}'.format(post_id)
注册的路由 return 的内容会包含在返回给用户的 HTTP response 中，这两个实例都返回字符串，所以用户使用浏览器访问这两个链接地址的时候看到的就是两个字符串显示在浏览器页面上。

模板渲染

在上面的例子中，处理函数返回的都是字符串，但是在真正的项目中，需要使用 HTML 编写页面，不可能把所有的内容都写到字符串中。模板引擎的作用就是你用模板引擎规定的语法编写 HTML 页面，在处理函数中指定模板，传入相应的模板变量，Flask 就能调用模板引擎自动渲染出一个完整的 HTML 页面。

Flask 默认的模板引擎是 jinja2，理论上你是可以更换其它模板引擎的，但是 jinja2 已经足够好用。

Flask 使用 render_template 函数渲染模板，指定了一个模板名称后，Flask 会到 templates 目录下去找这个模板，然后使用传入的变量渲染模板。

如果我们用模板来改写用户主页的例子，那么处理函数可以这样写：

from flask import render_template

@app.route('/user/<username>')
def user_index(username):
    return render_template('user_index.html', username=username)
然后创建 templates 目录，目录结构变成这样：

/flask-test-app
    app.py
    /templates
        user_index.html
在 user_index.html 中：

<h1>Hello, {{ username }}!</h1>
在 jinja2 中，用 {{ }} 来渲染一个字符串变量。这里的 username 就是在 render_template 的时候传入的关键字参数 username。现在访问一个用户主页，比如说：

localhost:5000/user/shiyanlou
就能看到一个用 h1 标签包裹的 Hello, shiyanlou! 了。

另外，flask 中提供了 url_for 来根据路由的函数名称构建 URL 链接地址，提供了 redirect 来跳转到其他路由，见下面的例子：

from flask import render_template, redirect, url_for

@app.route('/')
def index():
    return redirect(url_for('user_index', username='default'))

@app.route('/user/<username>')
def user_index(username):
    return render_template('user_index.html', username=username)
这个例子中，访问 / index 页面的时候，会自动跳转到 /user/default 页面，跳转的目标页面 URL 地址是由 url_for 产生的，而跳转过程是由 redirect 函数进行的操作。

Flask 模板渲染示例开发视频：

Play Video

request 对象

Flask 通过 request 对象获取请求相关的数据，要使用它，要从 flask 导入：

from flask import request
从 request.headers 获取请求头的数据，可以把它当作字典来使用，比如要获取用户的 user-agent：

request.headers.get('User-Agent')
从 request.args 获取请求的参数，假设我们的应用是个博客应用，主页有分页功能，用 这个 URL 访问主页：

localhost:5000?page=2&per_page=10
获取 ? 后面的参数就可以这样做：

page = request.args.get('page')
per_page = request.args.get('per_page')
处理之外，可以通过 request.form 获取表单数据，通过 request.method 获取当前请求的方法。

session

HTTP 协议是无状态的，每一次请求它们的关系都是相互独立的。但是在实际的应用是，我们确实有很多数据服务器需要记住，但又不适合存放在数据库中。

比如说，一个登录页面需要在用户密码输入错误 3 次后要求输入验证码，服务器就需要一个计数器纪录错误次数，但把它放到数据库也不太合适。session 就是用来为每个用户独立存放一些数据的地方。存放在 session 里的数据可以在特定用户的多个请求之间共享。

cookies

cookies与 session 类似，只不过 cookies 是存在客户端加密信息。在 Flask 中，cookie 使用配置的 SECRET_KEY 作为签名进行加密。

比如在上面的访问用户主页的路由中，将用户名设置为一个 cookies，这样用户在此访问时，我们就能知道他是谁了：

from flask import make_response

@app.route('/user/<username>')
def user_index(username):
    resp = make_response(render_template('user_index.html', username=username))
    resp.set_cookie('username', username)
    return resp
设置 cookies后，用户访问其他页面可以从 request.cookies 获取到我们设置的 username：

from flask import request

@app.route('/')
def index():
    username = request.cookies.get('username')
    return 'Hello {}'.format(username)
Flask cookies 示例开发视频：

Play Video

错误处理

使用 app.errorhandler 装饰器可以注册错误处理函数，比如对于最常见的 404 错误，我们返回一个特定的 404.html 页面。

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
例子中也展示了使用 render_template 的一个小知识点，就是可以在它后面指定本次返回的状态码。

在 flask 中还有一个经常用来处理错误的方法 abort()，使用 abort(404) 则能够直接进入到页面无法找到（HTTP 状态码404）的处理逻辑中。例子如下：

from flask import render_template, abort

@app.route('/user/<username>')
def user_index(username):
    if username == 'invalid':
        abort(404)
    return render_template('user_index.html', username=username)
当 username 为 invalid 字符串的时候，即访问 /user/invalid 地址的时候，直接返回页面无法找到。

Flask 错误处理示例开发视频：

Play Video

插件

下面列出了一些 Flask 开发中常用的插件，这些插件大多在后面的项目中会用到，因为篇幅的原因不能一一介绍。每个插件都可以在 Github 搜到，大家可以先去了解一下。

flask_sqlalchemy：ORM，封装了 sqlalchemy，使用更简单
flask-login：管理用户 session，如登入、登出，session 过期管理等等
flask_migrate：数据库版本管理
flask_wtf：封装了 wtforms 表单生成与验证工具，提供了 CSRF 支持
flask-session：flask 默认 session 基于客户端 cookie 的，这个插件方便在服务端做 session
总结

本节实验通过一些简单的开发示例学习了 Flask Web 应用开发的基础，本节的内容中包括以下的知识点：

Flask 简介
配置方法
注册路由
模板渲染
request 对象
session
cookies
错误处理
插件
实际的项目开发中，Flask 会大量应用各种插件，例如和数据库对接使用 flask_sqlalchemy，管理登录登出 session 则使用 flask-login，这些插件的使用可以极大的提高我们开发 Web 应用的效率，所以当你有任何开发需求的时候，先去搜索是否已经有现成的模块可以给我们使用了，如果有的话就可以参考使用文档直接应用。

Jinja2 模板
简介

Jinja2 是一个Python 软件包，实现了 HTML 模板语言。网页的渲染方式一般有两种，一种是后端渲染，一种是前端渲染。后端渲染时，一般都是通过 HTML 模板进行的，模板中可能包含若干逻辑，比如继承自其它基础模板。这些模板逻辑，继承功能都需要模板语言的支持，而 Jinja2 正是这样的一种语言。有了 Jinja2 以后，HTML 模板的编写将变得非常简单。在本节实验中，我们将学习 Jinja2 的方方面面，比如模板变量，循环功能，过滤器等等。

知识点

Jinja 语法；
Jinja 过滤器；
Flask 中使用 Jinja 模板
Flask 和 Jinja

模板一般和 Web 框架配合使用，Flask 的默认模板功能就是通过 Jinja2 实现的。所以通过 Flask 学习 Jinja 再好不过。

通过下面的命令创建 Flask app:

$ cd ~/Code
$ mkdir templates
$ echo "<h1>hello world</h1>" > templates/index.html
$ touch app.py
以上命令，创建了 templates 目录，Flask 默认已经整合了 Jinja, 会自动从 templates 目录加载相应的模板。接着在 app.py 中输入代码：

#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask, render_template


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def index():

    teacher = {
        'name': 'Aiden',
        'email': 'luojin@simplecloud.cn'
    }

    course = {
        'name': 'Python Basic',
        'teacher': teacher,
        'user_count': 5348,
        'price': 199.0,
        'lab': None,
        'is_private': False,
        'is_member_course': True,
        'tags': ['python', 'big data', 'Linux']
    }
    return render_template('index.html', course=course)
上面的代码中，创建了一个 Flask 应用，需要注意的是我们设置了 app.config['TEMPLATES_AUTO_RELOAD'] = True, 这使得每当模板发生改变时，会自动重新渲染模板。接着创建了 index view，其中定义了 course 字典，代表一门课程。该 view 会渲染 index.html 模板，该模板位于 ~/Code/templates/index.html，后续关于 Jinja 的演示代码都会写入 index.html 文件中，然后通过浏览器查看效果。通过以下命令启动 Flask 应用:

$ cd ~/Code
$ FLASK_DEBUG=1 FLASK_APP=app.py flask run
* Serving Flask app "app"
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
启动应用时，通过环境变量 FLASK_DEBUG=1 设置 Flask 启动在 debug 模式。启动成功后，可以通过浏览器访问 http://127.0.0.1:5000/，效果如下：



Flask 与 Jinja 结合开发视频：


Jinja 基础

Jinja2 的语法中，使用一些特殊字符包含需要解析执行的代码，没有被这些特殊字符包含的代码则不进行解析处理。主要以下几种特殊字符 (... 字符代表省略的需要执行的代码)：

{% ... %} 包含的代码是可以被执行的语句，比如循环语句，继承语法；
{{ ... }} 包含的的 Python 对象，用于解析出这些对用的值，经常用于打印内容；
{# ... #} 用于添加注释，这些注释不会被处理，但是也不会输出到 HTML 源码中；
变量

在 Jinja2 中，变量可以通过 {{ variable }} 的形式显示，可以通过 . 访问变量的属性，如果传递给模板的变量是一个字典，也可以通过 . 访问字典的字段。在前文中，我们创建的 app.py 文件中，已经将一个 course 对象传递给了 index.html 模板，现在将 index.html 模板修改成以下内容，重新刷新浏览器就可以看到 course 的各种属性了：

<p> name: {{ course.name }}</p>
<p> user count: {{ course.user_count }}</p>
<p> teacher: {{course.teacher }} </p>
<p> is_private: {{ course.is_private }} </p>
<p> not exist: {{ course.not_exist }} </p>
效果图：



还可以发现，如果访问一个不存在的属性，则会简单的返回空值，不会发生异常，这在 Python 代码中访问不存在的属性是不一样的。

Jinja2 也支持赋值操作，有的时候执行方法可能消耗很多资源，这个时候可以将执行结果通过 set 关键字赋值给 Jinja2 变量，在后续的所有访问中，都通过该变量访问，如下代码：

{% set result = heavy_operation() %}

<p> {{ result }}</p>
逻辑比较

Jinja 中的逻辑比较可以通过 if 语句，如下代码：

{% if course.is_private %}
    <p> course {{course.name}} is private </p>
{% elif course.is_member_course %}
    <p> course {{course.name}} is member course </p>
{% else %}
    <p> course {{course.name}} is normal course </p>
{% endif %}
可以看到语法和 Python 中的 if 判断差不多，但是需要包裹在 {% %} 符号中，同时结尾需要有 endif 语句，在 index.html 中输入代码后，效果如下图：



循环

在 Jinja 中循环主要通过 for 语句完成，语法如下：

{% for tag in course.tags %}
    <span> {{ tag }} </span>
{% endfor %}
宏

在 Python 中可以定义各种函数，同样的在 Jinja2 中，可以定义宏，相当于 Python 中的函数。可以将常用的 HTML 代码写成一个宏，这样在任何地方调用宏就可以生成同样的 HTML 代码，提高了代码复用度。宏通过 macro 关键字进行定义。比如可以将渲染一门课程信息的代码写成一个宏:

{% macro course_item(course, type="bootstrap") %}
    <div>
        <p> type: {{ type }} </p>
        <p> name: {{ course.name }}</p>
        <p> user count: {{ course.user_count }}</p>
        <p> teacher: {{course.teacher }} </p>
        <p> is_private: {{ course.is_private }} </p>
    </div>
{% endmacro %}

<div> {{ course_item(course) }} </div>
<p>{{ '=' * 20 }}</p>
<div> {{ course_item(course, type="louplus") }} </div>
上面的代码中，定义了 course_item 宏，该宏有两个参数，第一个是课程，第二个是类型，且第二个参数具有默认值，和 Python 函数非常像，接着通过 {{ course_item(course) }} 方式调用了两次宏。上面代码写入 index.html, 刷新页面效果如下：



Jinja 宏使用示例视频：


模块

上文中定义的宏有可能需要被其他模板引用，好在 Jinja2 也支持模块功能。首先我们在 ~/Code/templates 目录中创建 macro.html 文件，然后将上文中定义 course_item 宏的代码写入该文件。然后就可以在 index.html 中通过 import 关键字导入宏了，如下代码：

{% from 'macro.html' import course_item %}

<div> {{ course_item(course) }} </div>
可以发现模块的导入方式和 Python 的也比较类似。

模板继承

Jinja2 同样支持模板间的继承。网页中，很多组件是共用的，比如网页的标题栏和尾部，通过继承功能可以很方面的共用组件。继承功能通过 extends, block 等关键字实现。首先在 ~/Code/templates 目录中创建 base.html 模板，然后写入以下代码：

<body>
    <div> 
        {% block header %}
            <p> this is header </p>
        {% endblock %}
    </div>
    <div>{% block content %}{% endblock %}</div>
    <div id="footer">
        {% block footer %}
        &copy; Copyright 2017 by <a href="http://www.shiyanlou.com/">shiyalou</a>.
        {% endblock %}
    </div>
</body>
上面的代码中，通过 block 定义了 header, content, footer 三个块，可以被其他模板重写，如果未被其他模板重写则显示默认内容。在 index.html 中输入以下代码：

{% extends "base.html" %}
{% from 'macro.html' import course_item %}

{% block header %}
    <h1> header </h1>
{% endblock %}

{% block content %}
    {{ course_item(course) }}
{% endblock %}
上面的代码中，首先通过 extends 关键字告诉 Jinja2 模板从 base.html 继承而来，接着使用 import 关键字从上一节实验中定义的 macro.html 导入了宏 course_item。接着使用 block 关键字覆盖了 base.html 模板中定义的 header, content 块，而 footer 块将显示默认内容。刷新浏览器，效果如下图：



Jinja 模块使用视频：


过滤器

Jinja2 中还支持过滤器，过滤器通过 | 方式执行，比如 {{ var | abs }}, 通过 abs 过滤器对 var 求绝对值。 Jinja2 有很多内置的过滤器，比如:

abs 求绝对值；
capitalize 将字符传首字母变成大写，其他转换为小写；
first 获取列表的第一个元素；
int 转换为整数；
length 求列表的长度；
内置的过滤器有很多就不一一列出了。Jinja2 也支持自定义过滤器，通过 Flask 添加过滤器非常简单，修改 app.py 为如下代码：

# -*- coding:utf-8 -*-

from flask import Flask, render_template


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

def hidden_email(email):
    parts = email.split('@')
    parts[0] = '*****'
    return '@'.join(parts)

app.add_template_filter(hidden_email)

@app.route('/')
def index():

    teacher = {
        'name': 'Aiden',
        'email': 'luojin@simplecloud.cn'
    }

    course = {
        'name': 'Python Basic',
        'teacher': teacher,
        'user_count': 5348,
        'price': 199.0,
        'lab': None,
        'is_private': False,
        'is_member_course': True,
        'tags': ['python', 'big data', 'Linux']
    }
    return render_template('index.html', course=course)
以上代码，通过 app.add_template_filter 方法注册了 hidden_email 过滤器，该过滤器隐藏邮箱前缀。接着在 index.html 文件中输入下面的代码：

{% extends "base.html" %}
{% from 'macro.html' import course_item %}

{% block content %} 
    <p> teacher email: {{ course.teacher.email | hidden_email }}</p>
    <p> course tag length: {{ course.tags | length }} </p>
{% endblock %}
刷新浏览器，效果如下：



Jinja 过滤器使用视频：


url_for

还记得我们在 Flask 入门实验中学习的 url_for 来构建 URL 地址的方法吗？同样也可以在 Jinja 中使用，使用方法与 Flask 中相同，但需要在前后增加两个大括号才能在 Jinja 中解析成正确的 URL 地址：

{{ url_for('user_index', username='testuser') }}
此外，还有一个常用的 static 目录的用法，开发一个 Web 应用的时候需要将一些图片、js、css 等文件放到一个统一的 static 目录，获取这些文件的地址的方式可以用下面的方式：

{{ url_for('static', filename='css/style.css') }}
Jinja2 中默认的 static 目录是和 templates 目录同一层次的目录。只要将图片、js、css 等文件放到这个 static 目录下就可以使用这种方法获得文件的 URL 地址了。

总结

本节实验讲解了 Jinja2 的基础知识，覆盖了 Jinja2 的大部分知识点，包括：

变量处理；
逻辑判断；
循环；
宏的定义；
模板模块的使用；
模板继承功能；
url_for
在实际的项目中，以上功能都可能会被使用，所以请努力掌握相关知识点。楼+ 课程后续会有大量的 Web 开发实战，这个过程中需要写很多 Jinja 模板代码，相对于 CSS/HTML/JavaScript 部分的内容，Jinja 的语法要简单很多
