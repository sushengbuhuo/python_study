Scrapy 爬虫高级应用
简介

本节内容主要介绍使用 scrapy 进阶的知识和技巧，包括页面追随，图片下载， 组成 item 的数据在多个页面，模拟登录。

知识点

页面追随
图片下载
Item 包含多个页面数据
模拟登录
页面跟随

在前面实现课程爬虫和用户爬虫中，因为实验楼的课程和用户 url 都是通过 id 来构造的，所以可以轻松构造一批顺序的 urls 给爬虫。但是在很多网站中，url 并不是那么轻松构造的，更常用的方法是从一个或者多个链接（start_urls）爬取页面后，再从页面中解析需要的链接继续爬取，不断循环。

下面是一个简单的例子，从实验楼课程编号为 63 的课程主页，从课程相关的进阶课程获取下一批要爬取的课程。用前面所学的知识就能够完成这个程序，在看下面的代码前可以思考下怎么实现。



结合前面所学的知识，你可能会写出类似这样的代码：

# -*- coding: utf-8 -*-
import scrapy


class CoursesFollowSpider(scrapy.Spider):
    name = 'courses_follow'
    start_urls = ['https://shiyanlou.com/courses/63']

    def parse(self, response):
        yield {
            'name': response.xpath('//h4[@class="course-infobox-title"]/span/text()').extract_first(),
            'author': response.xpath('//div[@class="mooc-info"]/div[@class="name"]/strong/text()').extract_first()
        }
        # 从返回的 response 解析出“进阶课程”里的课程链接，依次构造
        # 请求，再将本函数指定为回调函数，类似递归
        for url in response.xpath('//div[@class="sidebox-body course-content"]/a/@href').extract():
            # 解析出的 url 是相对 url，可以手动将它构造为全 url
            # 或者使用 response.urljoin() 函数
            yield scrapy.Request(url=response.urljoin(url), callback=self.parse)
完成页面跟随的核心就是最后 for 循环的代码。使用response.follow 函数可以对 for 循环代码做进一步简化：

# -*- coding: utf-8 -*-
import scrapy


class CoursesFollowSpider(scrapy.Spider):
    name = 'courses_follow'
    start_urls = ['https://shiyanlou.com/courses/63']

    def parse(self, response):
        yield {
            'name': response.xpath('//h4[@class="course-infobox-title"]/span/text()').extract_first(),
            'author': response.xpath('//div[@class="mooc-info"]/div[@class="name"]/strong/text()').extract_first()
        }
        # 不需要 extract 了
        for url in response.xpath('//div[@class="sidebox-body course-content"]/a/@href'):
            # 不需要构造全 url 了
            yield response.follow(url, callback=self.parse)
页面追随实现视频：


图片下载

scrapy 内部内置了下载图片的 pipeline。下面以下载实验楼课程首页每个课程的封面图片为例展示怎么使用它。

首先需要在 items.py 中定义一个 item ，它包含俩个必要的字段：

class CourseImageItem(scrapy.Item):
    # 要下载的图片 url 列表
    image_urls = scrapy.Field()
    # 下载的图片会先放着这里
    images = scrapy.Field()
运行 scrapy genspider courses_image shiyanlou.com/courses 生成一个爬虫，爬虫的核心工作就是解析所有图片的链接到 CourseImageItem 的 image_urls 中。

# -*- coding: utf-8 -*-
import scrapy

from shiyanlou.items import CourseImageItem


class CoursesImageSpider(scrapy.Spider):
    name = 'courses_image'
    start_urls = ['https://www.shiyanlou.com/courses/']

    def parse(self, response):
        item = CourseImageItem()
        ＃解析图片链接到 item
        item['image_urls'] = response.xpath('//div[@class="course-img"]/img/@src').extract()
        yield item
代码完成后需要在 settings 中启动 scrapy 内置的图片下载 pipeline，因为 ITEM_PIPELINES 里的 pipelines 会按顺序作用在每个 item 上，而我们不需要 ShiyanlouPipeline 作用在图片 item 上，所以要把它注释掉

ITEM_PIPELINES = {
    'scrapy.pipelines.images.ImagesPipeline': 100,
    # 'shiyanlou.pipelines.ShiyanlouPipeline': 300
}
还需要配置图片存储的目录：

IMAGES_STORE = 'images'
运行程序：

# 安装需要的 PIL 包
pip3 install image

# 执行图片下载爬虫
scrapy crawl courses_image
scrapy 会将图片下载到 images/full 下面，保存的文件名是对原文件进行的 hash。为什么会有一个 full 目录呢？full 目录代表下载的图片的原尺寸的，因为 scrapy 可以配置改变下载图片的尺寸，比如在 settings 中给你添加下面的配置生成小图片：

IMAGES_THUMBS = {
    'small': (50, 50)
}
图片下载实现视频：


组成 item 的数据在多个页面

在前面几节实现的爬虫中，组成 item 的数据全部都是在一个页面中获取的。但是在实际的爬虫项目中，经常会遇到从不同的页面抓取数据组成一个 item。下面通过一个例子展示怎么处理这种情况。

有一个需求，爬取实验楼课程首页所有课程的名称、封面图片链接和课程作者。课程名称和封面图片链接在课程主页就能爬到，课程作者只有点击课程，进入课程详情页面才能看到，怎么办呢？

scrapy 的解决方案是多级 request 与 parse。简单的说就是先请求课程首页，在回调函数 parse 中解析出课程名称和课程图片链接，然后在 parse 函数再构造一个请求到课程详情页面，再在处理课程详情页的回调函数中解析出课程作者。

首先在 items.py 中创建 相应的 Item 类：

class MultipageCourseItem(scrapy.Item):
    name = scrapy.Field()
    image = scrapy.Field()
    author = scrapy.Field()
运行 scrapy genspider multipage shiyanlou.com/courses 生成一个爬虫，并修改代码如下：

# -*- coding: utf-8 -*-
import scrapy
from shiyanlou.items import MultipageCourseItem


class MultipageSpider(scrapy.Spider):
    name = 'multipage'
    start_urls = ['https://www.shiyanlou.com/courses/']

    def parse(self, response):
        for course in response.css('a.course-box'):
            item = MultipageCourseItem()
            # 解析课程名称
            item['name'] = course.xpath('.//div[@class="course-name"]/text()').extract_first()
            # 解析课程图片
            item['image'] = course.xpath('.//img/@src').extract_first()
            # 构造课程详情页面的链接，爬取到的链接是相对链接，调用 urljoin 方法构造全链接
            course_url = response.urljoin(course.xpath('@href').extract_first())
            # 构造到课程详情页的请求，指定回调函数
            request = scrapy.Request(course_url, callback=self.parse_author)
            # 将未完成的 item 通过 meta 传入 parse_author
            request.meta['item'] = item
            yield request

    def parse_author(self, response):
        # 获取未完成的 item
        item = response.meta['item']
        # 解析课程作者
        item['author'] = response.xpath('//div[@class="mooc-info"]/div[@class="name"]/strong/text()').extract_first()
        # item 构造完成，生成
        yield item
关闭所有的 pipeline，运行爬虫，保存结果到文件中：

scrapy crawl multipage -o data.json
这部分的知识点不容易理解，可以参考下先前同学的一个提问来理解 https://www.shiyanlou.com/questions/50921

组成 item 的数据在多个页面操作视频：


模拟登录

有些网页中的内容需要登录后才能看到，例如实验楼用户主页的中的这个模块

，只有在你自己的用户主页才能看见。



如果想要爬取登录后才能看到的内容就需要 scrapy 模拟出登录的状态再去抓取页面，解析数据。这个实验就是要模拟登录自己的主页，然后在自己的主页爬取图片中箭头所指的数据。

通常网站都会有一个 login 页面，实验楼的 login 页面网址是：https://www.shiyanlou.com/login。打开这个网页，查看源码，可以看到里面的登录表单的相关代码。



模拟登录抓取的过程类似上面介绍的多页面抓取，只不过是将第一个页面的抓取变为提交一个登录表单，登录成功后， scrapy 会带着返回的 cookie 进行下面的抓取，这样就能抓取到登录才能看到的内容。

这个实验不要创建项目，在 Code 下面创建一个 login_spider.py 脚本就可以了。下面是程序的基本结构和流程：

# -*- coding: utf-8 -*-
import scrapy


class LoginSpiderSpider(scrapy.Spider):
    name = 'login_spider'

    start_urls = ['https://www.shiyanlou.com/login']

    def parse(self, response):
        """ 模拟登录的核心就在这里，scrapy 会下载 start_urls 里的
        登录页面，将 response 传到这里，然后调用 FormRequest
        模拟构造一个 POST 登录请求。FormRequest 继承自 Request，
        所以 Request 的参数对它适用。FormRequest 有一类方法 `from_response` 用于快速构建 FormRequest 对象。from_response 方法会从第一步返回的 response 中获取请求的 url，form 表单信息等等，我们只需要指定必要的表单数据和回调函数就可以了。
        """
        return scrapy.FormRequest.from_response(
             # 第一个参数必须传入上一步返回的 response
             response,
             # 以字典结构传入表单数据
             formdata={},
             # 指定回调函数
             callback=self.after_login
        )

    def after_login(self, response):
        """ 登录之后的代码和普通的 scrapy 爬虫一样，构造 Request，指定 callback ...
        """
        pass

    def parse_after_login(self, response):
        pass
基于这个代码结构很容易写出代码：

# -*- coding: utf-8 -*-
import scrapy


class LoginSpiderSpider(scrapy.Spider):
    name = 'login_spider'

    start_urls = ['https://www.shiyanlou.com/login']

    def parse(self, response):
        # 获取表单的 csrf_token 
        csrf_token = response.xpath('//div[@class="login-body"]//input[@id="csrf_token"]/@value').extract_first()
        self.logger.info(csrf_token)
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'csrf_token': csrf_token,
                # 这里要改为自己的邮箱和密码
                'login': 'example@email.com',
                'password': 'password',
            },
            callback=self.after_login
        )

    def after_login(self, response):
        # 登录成功后构造一个访问自己主页的 scrapy.Request
        # 记得把 url 里的 id 换成你自己的，这部分数据只能看到自己的
        return [scrapy.Request(
            url='https://www.shiyanlou.com/user/634/',
            callback=self.parse_after_login
        )]

    def parse_after_login(self, response):
        """ 解析实验次数和实验时间数据，他们都在 span.info-text 结构中。实验次数位于第 2 个，实验时间位于第 3 个。
        """
        return {
            'lab_count': response.xpath('(//span[@class="info-text"])[2]/text()').re_first('[^\d]*(\d*)[^\d*]'),
            'lab_minutes': response.xpath('(//span[@class="info-text"])[3]/text()').re_first('[^\d]*(\d*)[^\d*]')
        }
运行脚本：

scrapy runspider login_spider.py -o user.json
运行结束后，只会在登录后才能看的数据就被抓取下来并保存在 user.json 中了。

模拟登录实验楼操作视频：


总结

本节内容主要通过实验楼用户爬虫的代码实例介绍如何使用 scrapy 进阶的知识和技巧，包括页面追随，图片下载， 组成 item 的数据在多个页面，模拟登录等。

本节实验中涉及到的知识点：

页面追随
图片下载
Item 包含多个页面数据
模拟登录

Scrapy 爬取实验楼用户数据
简介

本节内容运用前俩节学到的知识，爬取实验楼的用户数据，主要是为了练习、巩固前面学习到了知识。

知识点

Scrapy 项目框架
分析网页元素字段
SQLAlchemy 定义数据模型
创建 Item
解析数据
要爬取的内容

下面是一个用户主页的截图，箭头指的是我们要爬取的内容：



要爬取的内容和字段名称定义：

用户名（name）
类型：普通用户／会员／高级会员（type）
加入实验楼的时间（join_date）
楼层数（level）
状态：在职／学生（status）
学校（如果用户是学生）（school）
职位（如果用户在职）(job）
学习记录（study_record）
定义数据模型

决定好了要爬取的内容，就可以使用 SQLAlchemy 定义数据模型了，在 models.py 中的 Course 后面定义 User 模型：

# User 表用到新类型要引入
from sqlalchemy import Date

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True)
    type = Column(String(64))
    status = Column(String(64), index=True)
    school = Column(String(64))
    job = Column(String(64))
    level = Column(Integer, index=True)
    join_date = Column(Date)
    learn_courses_num = Column(Integer)
现在可以运行程序创建 users 表了：

python3 models.py
SQLAlchemy 默认不会重新创建已经存在的表，所以不用担心 create_all 会重现创建 couses 表造成数据丢失。

定义数据模型操作视频：


创建 Item

在 items.py 中创建 UserItem，为每个要爬取的字段声明一个 Field。

class UserItem(scrapy.Item):
    name = scrapy.Field()
    type = scrapy.Field()
    status = scrapy.Field()
    job = scrapy.Field()
    school = scrapy.Field()
    level = scrapy.Field()
    join_date = scrapy.Field()
    learn_courses_num = scrapy.Field()
创建爬虫

使用 genspider 命令创建 users 爬虫：

scrapy genspider users shiyanlou.com
scrapy 为我们在 spiders 下面创建 users.py 爬虫，将它修改如下：

import scrapy

class UsersSpider(scrapy.Spider):
    name = 'users'

    @property
    def start_urls(self):
        """ 实验楼注册的用户数目前大约50几万，为了
        爬虫的效率，取 id 在 524,800~525,000 之间的
        新用户，每间隔 10 取一个，最后大概爬取 20 个
        用户的数据
        """
        return ('https://www.shiyanlou.com/user/{}/'.format(i) for i in range(525000, 524800, -10))
爬虫及Item实现视频：


解析数据

解析数据主要是编写 parse 函数。在实际编写前，最好是用 scrapy shell 对某一个用户先测，将正确的提取代码复制到 parse 函数中。

下面的几个例子是要提取的数据在文档中的结构和对应的提取器（提取器有很多种写法，可以写你自己的）

name:

# response.css('span.username::text')
<span class="username">aiden0z</span>
type:

# response.css('a.member-icon img.user-icon::attr(title)').extract_first(default='普通用户')
# 用户头像右下角有一个会员标志，用它可以判断用户类型，对于会员用户
# 可以从会员图标图片的 title 获取 type
# 非会员用户没用会员图标，可以为提取器返回一个默认值表示
 <a class="member-icon" href="/vip" target="_blank">

<img class="user-icon" src="

                https://static.shiyanlou.com/img/plus-vip-icon.png


          " title="标准会员">

        </a>
join_date：

# response.css('span.join-date::text').extract_first()
# 这样提取的值是 “2014-08-27 加入实验楼”，需要在 pipeline 中将
# 它处理为 date 对象
<span class="join-date">2014-08-27 加入实验楼</span>
依次在 scrapy shell 测试每个要爬取的数据，最后将代码整合进 users.py 中如下：

# -*- coding: utf-8 -*-
import scrapy
from shiyanlou.items import UserItem


class UsersSpider(scrapy.Spider):
    name = 'users'
    start_urls = ['']

    @property
    def start_urls(self):
        return ('https://www.shiyanlou.com/user/{}/'.format(i) for i in range(525000, 524800, -10))

    def parse(self, response):
        yield UserItem({
            'name': response.css('span.username::text').extract_first(),
            'type': response.css('a.member-icon img.user-icon::attr(title)').extract_first(default='普通用户'),
            'status': response.xpath('//div[@class="userinfo-banner-status"]/span[1]/text()').extract_first(),
            'job': response.xpath('//div[@class="userinfo-banner-status"]/span[2]/text()').extract_first(),
            'school': response.xpath('//div[@class="userinfo-banner-status"]/a/text()').extract_first(),
            'join_date': response.css('span.join-date::text').extract_first(),
            'level': response.css('span.user-level::text').extract_first(),
            'learn_courses_num': response.css('span.latest-learn-num::text').extract_first()
        })
数据解析操作视频：


pipeline

因为 pipeline 会作用在每个 item 上，当和课程爬虫共存时候，需要根据 item 类型使用不同的处理函数。

from datetime import datetime
from sqlalchemy.orm import sessionmaker
from shiyanlou.models import Course, User, engine
from shiyanlou.items import CourseItem, UserItem


class ShiyanlouPipeline(object):

    def process_item(self, item, spider):
        """ 对不同的 item 使用不同的处理函数
        """
        if isinstance(item, CourseItem):
            self._process_course_item(item)
        else:
            self._process_user_item(item)
        return item

    def _process_course_item(self, item):
        item['students'] = int(item['students'])
        self.session.add(Course(**item))

    def _process_user_item(self, item):
        # 抓取到的数据类似 'L100'，需要去掉 'L' 然后转化为 int
        item['level'] = int(item['level'][1:])
        # 抓去到的数据类似 '2017-01-01 加入实验楼'
        # 其中的把日期字符串转换为 date 对象
        item['join_date'] = datetime.strptime(item['join_date'].split()[0], '%Y-%m-%d').date()
        # 学习课程数目转化为 int
        item['learn_courses_num'] = int(item['learn_courses_num'])
        # 添加到 session
        self.session.add(User(**item))

    def open_spider(self, spider):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()
pipeline 实现视频：


运行

使用 `crawl｀ 命令启动爬虫：

scrapy crawl users
爬虫运行及结果查看视频：


总结

实验设计了一个新的实例，爬取实验楼的用户页面，在这个页面中首先需要分析页面中的各种元素，从而设计爬虫中数据提取的方式。然后把需要的数据内容通过 Scrapy 项目中的代码获取得到并解析出来，存储到数据库中。

本节实验包含以下的知识点：

Scrapy 项目框架
分析网页元素字段
SQLAlchemy 定义数据模型
创建 Item
解析数据

连接数据库的标准 Scrapy 项目
介绍

上一节中，我们只是基于 scrapy 写了一个爬虫脚本，并没有使用 scrapy 项目标准的形式。这一节我们要将脚本变成标准 scrapy 项目的形式，并将爬取到的数据存储到 MySQL 数据库中。数据库的连接和操作使用 SQLAlchemy。

知识点

连接数据库
创建 Scrapy 项目
创建爬虫
Item 容器
Item Pipeline
Models 创建表
保存 Item 到数据库
Item 过滤
连接数据库准备

本实验会将爬取的数据存入 MySQL，需要做一些准备工作。首先需要将 MySQL 的编码格式设置为 utf8，编辑配置文件：

sudo vim /etc/mysql/my.cnf
添加以下几个配置：

[client]
default-character-set = utf8

[mysqld]
character-set-server = utf8

[mysql]
default-character-set = utf8
保存后，就可以启动 mysql 了：

sudo service mysql start
以 root 身份进入 mysql，实验环境默认是没有密码的：

mysql -uroot
创建 shiyanlou 库给本实验使用：

mysql > create database shiyanlou;
完成后输入 quit 退出。

本实验使用 SQLAlchemy 这个 ORM在爬虫程序中连接和操作 mysql，先安装一下（不要忘记激活虚拟环境）：

pip3 install sqlalchemy
还需要安装 Python3 连接 MySQL 的驱动程序 mysqlclient：

sudo apt-get install libmysqlclient-dev
pip3 install mysqlclient
配置数据库和依赖包操作视频：


创建项目

使用 scrapy 提供的 startproject 命令创建一个 scrapy 项目

，需要提供一个项目名称，我们要爬取实验楼的数据，所以将 shiyanlou 作为项目名：

scrapy startproject shiyanlou
进入 shiyanlou，可以看到项目结构是这样的：

shiyanlou/
    scrapy.cfg            # 部署配置文件
    shiyanlou/            # 项目名称
        __init__.py
        items.py          # 项目 items 定义在这里
        pipelines.py      # 项目 pipelines 定义在这里
        settings.py       # 项目配置文件
        spiders/          # 所有爬虫写在这个目录下面
            __init__.py
创建 Scrapy 实验楼项目操作视频：


创建爬虫

scrapy 的 genspider 命令可以快速初始化一个爬虫模版，使用方法如下：

scrapy genspider <name> <domain>
name 这个爬虫的名称，domain 指定要爬取的网站。

进入第二个 shiyanlou 目录，运行下面的命令快速初始化一个爬虫模版：

cd /home/shiyanlou/Code/shiyanlou/shiyanlou
scrapy genspider courses shiyanlou.com
scrapy 会在 spiders 目录下新建一个 courses.py 的文件，并且在文件中为我们初始化了代码结构：

# -*- coding: utf-8 -*-
import scrapy

class CoursesSpider(scrapy.Spider):
    name = 'courses'
    allowed_domains = ['shiyanlou.com']
    start_urls = ['http://shiyanlou.com/']

    def parse(self, response):
        pass
这里面有一个新的属性 allowed_domains 是在前一节中没有介绍到的。它是干嘛的呢？allow_domains 可以是一个列表或字符串，包含这个爬虫可以爬取的域名。假设我们要爬的页面是 https://www.example.com/1.hml, 那么就把example.com 添加到 allowed_domains。这个属性是可选的，在我们的项目中并不需要使用它，所以可以删除。

除此之外 start_urls 的代码和上一节相同：

# -*- coding: utf-8 -*-
import scrapy


class CoursesSpider(scrapy.Spider):
    name = 'courses'

    @property
    def start_urls(self):
        url_tmpl = 'https://www.shiyanlou.com/courses/?category=all&course_type=all&fee=all&tag=all&page={}'
        return (url_tmpl.format(i) for i in range(1, 23))
创建 Scrapy 爬虫框架操作视频：


Item

爬虫的主要目标是从网页中提取结构化的信息，scrapy 爬虫可以将爬取到的数据作为一个 Python dict 返回，但由于 dict 的无序性，所以它不太适合存放结构性数据。scrapy 推荐使用 Item 容器来存放爬取到的数据。

所有的 items 写在 items.py 中，下面为要爬取的课程定义一个 Item：

import scrapy


class CourseItem(scrapy.Item):
      """定义 Item 非常简单，只需要继承 scrapy.Item 类，将每个要爬取
    的数据声明为 scrapy.Field()。下面的代码我们每个课程要爬取的 4 
    个数据。
    """
    name = scrapy.Field()
    description = scrapy.Field()
    type = scrapy.Field()
    students = scrapy.Field()
有了 CourseItem，就可以将 parse 方法的返回包装成它：

# -*- coding: utf-8 -*-
import scrapy
from shiyanlou.items import CourseItem


class CoursesSpider(scrapy.Spider):
    name = 'courses'

    @property
    def start_urls(self):
        url_tmpl = 'https://www.shiyanlou.com/courses/?category=all&course_type=all&fee=all&tag=all&page={}'
        return (url_tmpl.format(i) for i in range(1, 23))

    def parse(self, response):
        for course in response.css('div.course-body'):
            # 将返回结果包装为 CourseItem 其它地方同上一节
            item = CourseItem({
                'name': course.css('div.course-name::text').extract_first(),
                'description': course.css('div.course-desc::text').extract_first(),
                'type': course.css('div.course-footer span.pull-right::text').extract_first(default='免费'),
                'students': course.xpath('.//span[contains(@class, "pull-left")]/text()[2]').re_first('[^\d]*(\d*)[^\d]*')
            })
            yield item
定义 Item 容器视频：


Item Pipeline

如果把 scrapy 想象成一个产品线，spider 负责从网页上爬取数据，Item 相当于一个包装盒，对爬取的数据进行标准化包装，然后把他们扔到Pipeline 流水线中。

主要在 Pipeline 对 Item 进行这几项处理：

验证爬取到的数据 (检查 item 是否有特定的 field)
检查数据是否重复
存储到数据库
当创建项目时，scrapy 已经在 pipelines.py 中为项目生成了一个 pipline模版：

class ShiyanlouPipeline(object):
    def process_item(self, item, spider):
        """ parse 出来的 item 会被传入这里，这里编写的处理代码会
        作用到每一个 item 上面。这个方法必须要返回一个 item 对象。
        """
        return item
除了 process_item 还有俩个常用的 hooks 方法，open_spider 和 ｀close_spider`：

class ShiyanlouPipeline(object):
    def process_item(self, item, spider):
        return item

    def open_spider(self, spider):
        """ 当爬虫被开启的时候调用
        """
        pass

    def close_spider(self, spider):
        """ 当爬虫被关闭的时候调用
        """
        pass
定义 Item Pipeline 操作视频：


定义 Model，创建表

在 items.py 所在目录下创建 models.py，在里面使用 sqlalchemy 语法定义 courses 表结构：

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer


engine = create_engine('mysql+mysqldb://root@localhost:3306/shiyanlou?charset=utf8')
Base = declarative_base()

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True)
    description = Column(String(1024))
    type = Column(String(64), index=True)
    students = Column(Integer)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
运行程序：

python3 models.py
如果运行正确的话，程序什么都不会输出，执行完后，进去 MySQL 中检查是否已经创建了表：

mysql > use shiyanlou;
mysql> show tables;
+---------------------+
| Tables_in_shiyanlou |
+---------------------+
| courses             |
+---------------------+
如果出现类似上面的东西说明表已经创建成功了！

创建数据库表操作视频：


保存 item 到数据库

创建好数据表后，就可以在 pipeline 写编写代码将 爬取到的每个 item 存入数据库中。

from sqlalchemy.orm import sessionmaker
from shiyanlou.models import Course, engine


class ShiyanlouPipeline(object):

    def process_item(self, item, spider):
        # 提取的学习人数是字符串，把它转换成 int
        item['students'] = int(item['students'])
        # 根据 item 创建 Course Model 对象并添加到 session
        # item 可以当成字典来用，所以也可以使用字典解构, 相当于
        # Course(
        #     name=item['name'],
        #     type=item['type'],
        #     ...,
        # )
        self.session.add(Course(**item))
        return item

    def open_spider(self, spider):
        """ 在爬虫被开启的时候，创建数据库 session
        """
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_spider(self, spider):
        """ 爬虫关闭后，提交 session 然后关闭 session
        """
        self.session.commit()
        self.session.close()
我们编写的这个 ShiyanlouPipeline 默认是关闭的状态，要开启它，需要在 settings.py 将下面的代码取消注释：

# 默认是被注释的
ITEM_PIPELINES = {
    'shiyanlou.pipelines.ShiyanlouPipeline': 300
}
ITEM_PIPELINES 里面配置需要开启的 pipeline，它是一个字典，key 表示 pipeline 的位置，值是一个数字，表示的是当开启多个 pipeline 时它的执行顺序，值小的先执行，这个值通常设在 100~1000 之间。

保存数据到数据库操作视频：


运行

前面使用的 runspider 命令用于启动一个独立的 scrapy 爬虫脚本，在 scrapy 项目中启动爬虫使用 crawl 命令，需要指定爬虫的 name：

scrapy crawl courses
爬虫运行完后，进入 MySQL，输入下面的命令查看爬取数据的前 3 个：

mysql> use shiyanlou;
mysql> select name, type, description, students from courses limit 3\G;


因为 scrapy 爬虫是异步执行的，所以爬取到的 course 顺序和实验楼网站上的会不一样。

运行爬虫操作视频：


item 过滤

有时候，并不是每个爬取到的 item 都是我们想要，我们希望对 item 做一下过滤，丢弃不需要的 item。比如只希望保留学习人数超过 1000 的课程，那么就可以对 pipeline 做如下修改：

from scrapy.exceptions import DropItem

class ShiyanlouPipeline(object):

    def process_item(self, item, spider):
        item['students'] = int(item['students'])
        if item['students'] < 1000:
            # 对于不需要的 item，raise DropItem 异常
            raise DropItem('Course students less than 1000.')
        else:
            self.session.add(Course(**item))
总结

本节内容介绍了如何使用 scrapy 命令行工具快速创建项目，创建爬虫，以及如何基于项目框架编写爬虫，运行爬虫。除此之外，也介绍了如何在 scrapy 中使用 MySQL 数据库，将结果存入数据库。

本节涉及到的知识点如下：

连接数据库
创建 Scrapy 项目
创建爬虫
Item 容器
Item Pipeline
Models 创建表
保存 Item 到数据库
Item 过滤

Scrapy 爬取实验楼课程信息
介绍

Scrapy 使用 Python 实现的一个开源爬虫框架。秉承着 “Don’t Repeat Yourself” 的原则，Scrapy 提供了一套编写爬虫的基础框架和编写过程中常见问题的一些解决方案。Scrapy 主要拥有下面这些功能和特点：

内置数据提取器（Selector），支持XPath 和 Scrapy 自己的 CSS Selector 语法，并且支持正则表达式，方便从网页提取信息。
交互式的命令行工具，方便测试 Selector 和 debugging 爬虫。
支持将数据导出为 JSON，CSV，XML 格式。
内置了很多拓展和中间件用于处理：
cookies 和 session
HTTP 的压缩，认证，缓存
robots.txt
爬虫深度限制
可推展性强，运行自己编写特定功能的插件
除了列出的这些，还有很多小功能，比如内置的文件、图片下载器等等。另外，Scrapy 基于 twisted 这个高性能的事件驱动网络引擎框架，也就是说，Scrapy 爬虫拥有很高的性能。

下面的内容我们来实现一个爬取实验楼所有课程信息的爬虫。

知识点

scrapy 爬虫框架介绍
scrapy 框架安装
数据提取器：CSS 和 XPATH
scrapy shell
正则表达式数据提取
start_urls
安装

为了方便管理 Python 版本和依赖包，首先在 Code 下创建一个 python3.5 的虚拟环境（实验环境已经安装了 virtualenv）：

virtualenv -p python3.5 venv
激活环境：

. venv/bin/activate
后面的 scrapy 爬虫实验都基于这个虚拟环境。

安装 scrapy:

pip3 install scrapy
现在在命令行输入 scrapy，出现下面的内容说明已经安装成功了。

Scrapy 1.4.0 - no active project

Usage:
  scrapy <command> [options] [args]

Available commands:
  bench         Run quick benchmark test
  fetch         Fetch a URL using the Scrapy downloader
  genspider     Generate new spider using pre-defined templates
  runspider     Run a self-contained spider (without creating a project)
  settings      Get settings values
  shell         Interactive scraping console
  startproject  Create new project
  version       Print Scrapy version
  view          Open URL in browser, as seen by Scrapy

  [ more ]      More commands available when run from project directory

Use "scrapy <command> -h" to see more info about a command
从中我们也可以看到 scrapy 提供的命令行命令和它的功能简介。

Scrapy 安装操作视频：


数据提取器

在开始编写爬虫前，我们先来学习一下 scrapy 的数据提取器（Selector），因为爬虫的本质就是为了获取数据，所以在编写爬虫的过程中需要编写很多数据提取的代码。

scrapy 内置两种数据提取语法： CSS 和 XPath 。下面通过例子来看看怎么使用，有这样一个 HTML 文件：

<html>
 <head>
  <base href='http://example.com/' />
  <title>Example website</title>
 </head>
 <body>
  <div id='images'>
   <a href='image1.html'>Name: My image 1 <br /><img src='image1_thumb.jpg' /></a>
   <a href='image2.html'>Name: My image 2 <br /><img src='image2_thumb.jpg' /></a>
   <a href='image3.html'>Name: My image 3 <br /><img src='image3_thumb.jpg' /></a>
   <a href='image4.html'>Name: My image 4 <br /><img src='image4_thumb.jpg' /></a>
   <a href='image5.html'>Name: My image 5 <br /><img src='image5_thumb.jpg' /></a>
  </div>
 </body>
</html>
这是 scrapy 官方提供的一个网页，方便我们练习 Selector，它的地址是

http://doc.scrapy.org/en/latest/_static/selectors-sample1.html
scrapy shell

scrapy shell 提供了一个交互式的 Python 环境方便我们测试和debug 爬虫，使用方法是

scrapy shell [url]
需要提供一个网页的 url，执行命令后，scrapy 会自动去下载这个 url 对应的网页，将结果封装为 scrapy 内部的一个 response 对象并注入到 python shell 中，在这个 response 对象上，可以直接使用 scrapy 内置的css 和 xpath 数据提取器。

运行下面的命令下载上面的网页并进入 shell：

scrapy shell http://doc.scrapy.org/en/latest/_static/selectors-sample1.html
对于网页的源代码分析，推荐使用 Chrome 浏览器，在页面上的元素右键选择 检查 可以得到源代码，在源代码上可以拷贝出 xpath 路径。

CSS Selector

顾名思义，css selector 就是 css 的语法来定位标签。例如要提取例子网页中 ID 为 images 的 div 下所有 a 标签的文本，使用 css 语法可以这样写：

>>> response.css('div#images a::text').extract()
['Name: My image 1 ', 'Name: My image 2 ', 'Name: My image 3 ', 'Name: My image 4 ', 'Name: My image 5 ']
div#images 表示 id 为 images 的 div，如果是类名为 images，这里就是 div.images。div a 表示该 div 下所有 a 标签，::text 表示提取文本，extract 函数执行提取操作，返回一个列表。如果只想要列表中第一个 a 标签下的文本，可以使用 extract_first 函数：

>>> response.css('div#images a::text').extract_first()
'Name: My image 1 '
extract_first() 方法支持对没有匹配到的元素提供一个默认值：

>>> response.css('div#images p::text').extract_first(default='默认值')
'默认值'
div#images 下面并没有 p 标签，所以会返回提供的默认值。如果不提供 default 值的话会返回 None。

如果要提取所有 a 标签的 href 链接，可以这样写：

>>> response.css('div#images a::attr(href)').extract()
['image1.html', 'image2.html', 'image3.html', 'image4.html', 'image5.html']
不只是 href，任何标签的任意属性都可以用 attr() 提取。基于上面的知识，就能轻松写出提取所有图片的链接地址：

>>> response.css('div#images a img::attr(src)').extract()
['image1_thumb.jpg', 'image2_thumb.jpg', 'image3_thumb.jpg', 'image4_thumb.jpg', 'image5_thumb.jpg']
如果 div 中有多个 class 的情况，用 css 提取器可以写为 div[class="class1 class2"]

CSS Selector 操作视频：


XPath

XPath 是一门路径提取语言，常用于从 html/xml 文件中提取信息。它的基规则如下：

表达式	描述
nodename	选取此节点的所有子节点。
/	从根节点选取。
//	从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置。
.	选取当前节点。
..	选取当前节点的父节点。
@	选取属性。
用 scrapy 的 xpath 语法提取 div#images a 的所有文本，可以这样写：

>>> response.xpath('//div[@id="images"]/a/text()').extract()
['Name: My image 1 ', 'Name: My image 2 ', 'Name: My image 3 ', 'Name: My image 4 ', 'Name: My image 5 ']
// 表示当前文本，div[@id="images"] 表示 id 为 images 的 div，通过属性来选择一个标签，要以 tag[@attr="value"] 的方式表示。

用 XPath 语法提取所有图片链接：

>>> response.xpath('//div[@id="images"]/a/img/@src').extract()
['image1_thumb.jpg', 'image2_thumb.jpg', 'image3_thumb.jpg', 'image4_thumb.jpg', 'image5_thumb.jpg']
比较俩种语法，CSS 语法比较简单，对新手比较友好，CSS 语法在底层其实是被转换成 XPath 的。XPath 虽然有一点学习成本，但是功能更强大，性能也要好一点。

XPATH 操作视频：


re 和 re_first 方法

除了 extract() 和 extract_first()方法， 还有 re() 和 re_first() 方法可以用于 css() 或者 xpath() 方法返回的对象。

使用 extract() 直接提取的内容可能并不符合格式要求，比如上面获取的第一个 a 标签的 text 是这样的：Name: My image 1，现在要求不要开头的 Name: 和结尾的空格，这时候就可以使用 re() 替代 extract 方法，使用正则表达式对提取的内容做进一步的处理：

>>> response.css('div#images a::text').re('Name: (.+) ')
['My image 1', 'My image 2', 'My image 3', 'My image 4', 'My image 5']
re() 方法中定义的正则表达式会作用到每个提取到的文本中，只保留正则表达式中的子模式匹配到的内容，也就是 () 内的匹配内容。

re_first() 方法支持只作用于第一个文本：

>>> response.css('div#images a::text').re_first('Name: (.+) ')
'My image 1'
re 及 re_first 操作视频：


实战

下面我们使用 scrapy 写一个爬虫，爬取实验楼所有课程名称、简介、类型和学习人数信息，并保存为 JSON 文本。

在 Code 下新建 shiyanlou_courses_spider.py 文件，写入 scrapy 爬虫的基本机构：

# -*- coding:utf-8 -*-
import scrapy

class ShiyanlouCoursesSpider(scrapy.Spider):
    """ 所有 scrapy 爬虫需要写一个 Spider 类，这个类要继承 scrapy.Spider 类。在这个类中定义要请求的网站和链接、如何从返回的网页提取数据等等。
    """

    # 爬虫标识符号，在 scrapy 项目中可能会有多个爬虫，name 用于标识每个爬虫，不能相同
    name = 'shiyanlou-courses'

    def start_requests(self):
        """ 需要返回一个可迭代的对象，迭代的元素是 `scrapy.Request` 对象，可迭代对象可以是一个列表或者迭代器，这样 scrapy 就知道有哪些网页需要爬取了。`scrapy.Request` 接受一个 url 参数和一个 callback 参数，url 指明要爬取的网页，callback 是一个回调函数用于处理返回的网页，通常是一个提取数据的 parse 函数。
        """

    def parse(self, response):
        """ 这个方法作为 `scrapy.Request` 的 callback，在里面编写提取数据的代码。scrapy 中的下载器会下载 `start_reqeusts` 中定义的每个 `Request` 并且结果封装为一个 response 对象传入这个方法。
        """
        pass
分析实验楼的课程页面可以看出，一共有 22 个课程页面，URL 模版是这样的：

https://www.shiyanlou.com/courses/?category=all&course_type=all&fee=all&tag=all&page={}
这样就可以写出 start_requests 方法：

def start_requests(self):
    # 课程列表页面 url 模版
    url_tmpl = 'https://www.shiyanlou.com/courses/?category=all&course_type=all&fee=all&tag=all&page={}'
    # 所有要爬取的页面
    urls = (url_tmpl.format(i) for i in range(1, 23))
    # 返回一个生成器，生成 Request 对象，生成器是可迭代对象
    for url in urls:
        yield scrapy.Request(url=url, callback=self.parse)
scrapy 内部的下载器会下载每个 Request，然后将结果封装为 response 对象传入 parse 方法，这个对象和前面 scrapy shell 练习中的对象是一样的，也就是说你可以用 response.css() 或者 response.xpath() 来提取数据了。

通过分析实验楼课程页面的文档结构，以《Python 数据分析入门与进阶》课程为例，我们需要提取的数据主要包含在下面的 div 里面：

<div class="course-body">
    <div class="course-name">Python 数据分析入门与进阶</div>
            <div class="course-desc">在本训练营中，我们将学习怎么样使用 Python 进行数据分析。课程将从数据分析基础开始，一步步深入讲解。从 Python 的基础用法到数据分析的各种算法，并结合各种实例，讲解数据分析过程中的方方面面。</div>
            <div class="course-footer">
                <span class="course-per-num pull-left">
                    <i class="fa fa-users"></i>

                    133

                </span>

             <span class="course-bootcamp pull-right">训练营</span>        
      </div>
</div>
根据这个 div 可以用提取器写出 parse 方法：

def parse(self, response):
    # 遍历每个课程的 div.course-body
    for course in response.css('div.course-body'):
        # 使用 css 语法对每个 course 提取数据
        yield {
            # 课程名称
            'name': course.css('div.course-name::text').extract_first(),
            # 课程描述
            'description': course.css('div.course-desc::text').extract_first(),
            # 课程类型，实验楼的课程有免费，会员，训练营三种，免费课程并没有字样显示，也就是说没有 span.pull-right 这个标签，没有这个标签就代表时免费课程，使用默认值 `免费｀就可以了。
            'type': course.css('div.course-footer span.pull-right::text').extract_first(default='Free'),
            # 注意 // 前面的 .，没有点表示整个文档所有的 div.course-body，有 . 才表示当前迭代的这个 div.course-body
               'students': course.xpath('.//span[contains(@class, "pull-left")]/text()[2]').re_first('[^\d]*(\d*)[^\d]*')
        }
students 提取的课程学习人数，提取代码为什么要这样写，有几点需要注意一下。首先，我们要提取的数据在下面这个机构中的：

<span class="course-per-num pull-left">
                    <i class="fa fa-users"></i>

                    133

                </span>
这个结构的文本包含了很多空白和换行，如果是以下面的 xpath 提取的话：

course.xpath('.//span[contains(@class, "pull-left")]/text()').extract()
结果是这样的，有俩个文本内容，第一个是<span>和 <i>之间的文本，第二个是 </i>和 </span>之间的文本：

['\n                \t', '\n\t                \n            \t    151455\n                \t\n\t\t\t\t']
text()[2]表示取第二个文本，re_first('[^\d]*(\d*)[^\d]*')表示只需要文本中的数字。

运行

按照上一步中的格式写好 spider 后，就能使用 scrapy 的 runspider 命令来运行爬虫了。

scrapy runspider shiyanlou_courses_spider.py -o data.json
注意这里输出得到的 data.json 文件中的中文显示成 unicode 编码的形式，所以看到感觉像是乱码，其实是正常的。

-o 参数表示打开一个文件，scrapy 默认会将结果序列化为 JSON 格式写入其中。爬虫运行完后，在当前目录打开 data.json 文件都能开到爬取到的数据了。

实验楼课程爬虫开发视频：


start_urls

scrapy.Spider 类已经有了一个默认的 start_requests方法，我们的爬虫代码其实可以进一步简化，只提供需要爬取的 start_urls，默认的 start_requests 方法会根据 start_urls 生成 Request 对象。所以，代码可以修改为：

import scrapy


class ShiyanlouCoursesSpider(scrapy.Spider):

    name = 'shiyanlou-courses'

    @property
    def start_urls(self):
        """ start_urls  需要返回一个可迭代对象，所以，你可以把它写成一个列表、元组或者生成器，这里用的是生成器
        """
        url_tmpl = 'https://www.shiyanlou.com/courses/?category=all&course_type=all&fee=all&tag=all&page={}'
        return (url_tmpl.format(i) for i in range(1, 23))

    def parse(self, response):
        for course in response.css('div.course-body'):
            yield {
                'name': course.css('div.course-name::text').extract_first(),
                'description': course.css('div.course-desc::text').extract_first(),
                'type': course.css('div.course-footer span.pull-right::text').extract_first(),
                'students': course.xpath('.//span[contains(@class, "pull-left")]/text()[2]').re_first('[^\d]*(\d*)[^\d]*')
            }
start_urls 修改代码视频：


总结

本节内容介绍了 scrapy 的主要功能，如何使用 scrapy 内置的 css 和 xpath 选择器提取数据，以及如何基于 scrapy 写一个简单的爬虫脚本，运行爬虫，将爬取结果保存为 JSON 数据。

本节实验中涉及到的是 Scrapy 爬虫入门的知识点：

scrapy 爬虫框架介绍
scrapy 框架安装
数据提取器：CSS 和 XPATH
scrapy shell
正则表达式数据提取
start_urls
