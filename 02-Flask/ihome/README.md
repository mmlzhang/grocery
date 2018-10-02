# eHome

#### 项目介绍
宜居人家是基于Flask框架开发的，一个提供短期出租、寻租房屋移动O2O平台的项目。

- 主要目标是为用户提供租房、寻租的一个平台,项目基于Flask框架.
- 项目以前后端分离的形式实现具体功能业务，前后端交互数据形式主要使用json。
- 后台接口负责处理业务逻辑，并提供响应数据，前端页面负责展示数据和效果。
- 项目接口设计符合RestfulAPI风格。
##### 项目模块：用户管理、房屋管理、订单管理

![宜居人家](/2018年6月21日1448072.png)

- 目前使用的主要是Flask框架以及其相关的一些插件 

  包括 Flask-Migrate、Flask-Script、Flask-Session、Flask-SQLAlchemy、Flask-WTF具体的插件可以看我的requirement.txt 

- 图片存储(文件)采用第三方文件存储系统——七牛云，当然也可以自己搭建文件存储系统（如：FastDFS）

- 登录错误限制：登录错误次数超过设定次数则封ip，选用Redis记录用户登录错误次数，每错误一次，Redis中的数据加1， 达到最大限制次数的时，不再进行用户名密码判断

- 前端模板：[art-template](http://aui.github.io/art-template/zh-cn)是一个简约、超快的模板引擎 ，它采用作用域预声明的技术来优化模板渲染速度，从而获得接近 JavaScript 极限的运行性能，并且同时支持 NodeJS 和浏览器 

- 支付宝Python SDK：因为官方并没有提供Python语言的SDK，但在github上有大神提供了二次封装的工具[python-alipay-sdk](https://github.com/fzlee/alipay/blob/master/README.zh-hans.md)

在本项目中采用的蚂蚁金服开放平台 [沙箱环境](https://openhome.alipay.com/platform/appDaily.htm) :

> 第一步：配置沙箱应用环境 
>
> ​	首先点击“开放平台-管理中心-沙箱环境”配置相关信息； 
>
> 第二步：了解并调用接口 
>
> ​	蚂蚁沙箱网关地址为：https://openapi.alipaydev.com/gateway.do 
>
> 第三步：线上验收 
>
> ​	在沙箱环境完成功能调试后，必须将支付宝网关、appid、应用私钥、支付宝公钥修改成正式环境的配置，并在蚂蚁正式环境进行完整的功能验收测试。 


#### 下载安装的步骤

1. 本地新建项目

   > git clone https://gitee.com/gavinliu4011/eHome.git
   >
   > cd eHome
   >
   > virtualenv --no-site-packages env 

2. 安装项目依赖

   > pip install -r requirements.txt 

3. 注册云通讯

   > 在utils文件夹下的sms.py文件里修改配置

4. 注册七牛云

   > 在utils文件夹下的image_storage.py文件里修改配置信息
   >
   > 在constants.py文件里修改七牛的空间外链域名

5. 修改Redis、MySQL以及其他配置信息

   > 在config文件中修改自己的配置 

6. 创建表

   > python manage.py db init
   >
   > python manage.py db migrate
   >
   > python manage.py db upgrade

7. 导入地区数据(可根据需求更改SQL语句)

   > 把areas_facility.sql文件的insert语句插入数据库中

8. 运行程序

   > python manage.py  runserver
