　　湖南科技大学图书馆自动续借系统
==============================================================
Autor : ciken  <br />
E-mail: ciken@live.cn  <br />
  <br />
功能：  <br />
　　　　1.根据读者相关信息（帐号、密码、邮箱）获取借阅信息  <br />
　　　　2.设置少于特定天数帮读者续借，并将续借结果发送邮件给读者  <br />
　　　　3.相关函数写的比较灵活，读者可根据自己的需要提取相关函数自用  <br />
  <br />
####PS：如果您觉得相关功能实现有更好的建议，欢迎指正<br />
<br />
<br />
#### 代码依赖关系
	python版本：python2.7
	代码在linux下测试上线
	python调用的非标准库：MySQLdb、BeautifulSoup
	数据库：Mysql


#### 相关模块说明
	目录结构
	dir
	├── renew_master.py 	 #主模块，负责各次模块调用
	├── api
	│   ├── __init__.py
	│   ├── CHECK.py 			    #次模块，负责借阅信息提取、字符串处理、邮件内容处理等
	│   ├── CONF-development.py 	#参数模板，请将此文件在当前目录复制一份为CONF.py
	│   ├── CONF.py 				#参数文件，项目主文件夹参数、Mysql连接参数、邮箱参数、log参数、公共调用函数、公共调用参数相关
	│   └── SERVER.py 				#次模块，负责数据库操作、邮件发送等
	├── logs				#日志文件夹
	│   └── renew
	│       └── 2014-07-30.logs 		#日志文件，以日期为文件名
	├── json				#续借信息
	│   └── *.json
	└── README.md 			#README



#### 各模块函数说明
	CHECK.py
	├── calcDate		#计算还剩多少天还书
	├──	getBorrowInfo 	#以list[dict]格式返回读者借阅信息
	├── checkReaderPasswd #获取登入返回信息
	├──	renewBook		#接受list[dict]格式的参数，以list[dict]格式返回续借信息，并更新还书期限
	└──	mailContentHand #邮件处理，接受字符串格式的学号、list[dict]格式的续借信息、list[dict]格式的借阅信息，返回字符串格式html形式的邮件内容

	SERVER.py
	├──	db			#数据库操作，相关接口待用。接受字符串（'GET'、'ADD'、'DEL'、'SWITCH'）格式、字符串（'GET'接收None参数、'ADD' 接收3个参数、'DEL'接收1个参数、'SWITCH'接受2个参数）
	└──	sendEmail	#发送邮件函数，接收字符串格式的（学号、邮件地址、邮件内容）

	master.py
	└──各模块函数调用、日志记录相关



####update information
version:1.4.1<br />
1.将获取登入信息函数提取出来 <br />
2.密码错误数据库续借开关关闭并发送邮件给读者 <br />
2014.12.17 <br />
 <br />
version:1.4 <br />
1.使用json进行内容交互 <br />
2.发送邮件成功记录进log <br />
2014.07.30 <br />
 <br />

version:1.3 <br />
1.使用mysql作为数据库对用户信息进行存取 <br />
2.引入BeautifulSoup库替换某些正则表达式 <br />
3.对邮件内容进行了html格式处理 <br />
2014.07.30 <br />
 <br />
version:1.2  <br />
1.将各函数模块分类  <br />
2.增加了配置文件一项  <br />
3.去掉了opener和cookie模块，替换为requests模块 <br />
 <br />
version:1.0 <br />
1.设置自动续借过期天数 <br />
2.续借过后发送邮件 <br />
3.续借过后检测未续借成功书籍并发送邮件 <br />
2014.03.19 <br />
<br /><br />
####　　　　　　　　Copyright © 2014 Free Software Foundation, ciken
