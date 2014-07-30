#!/usr/bin/python
#-*- coding:utf8 -*- 
#"Version 1.2"
# "Autor:ciken"
import sys
import datetime
reload(sys) ; sys.setdefaultencoding('gbk')	#set coding
TODAY = datetime.datetime.now()
RENEW_BOOK_EXPIRED_TIME = 7
#set workspace dir
WORKSPACE_DIR = '/home/pi/HNUSTLibAutomaticallyRenewal/'
LOG_DIR = WORKSPACE_DIR + 'log/'
STU_ID_FILE = WORKSPACE_DIR + 'stuID'

#URL set
LIB_URL = 'http://211.67.223.8:8080/'
LIB_LOGIN_URL =['reader/login.jsp?str_kind=login&barcode=','&password=']
LIB_BORROW_INFO_URL = 'http://211.67.223.8:8080/reader/infoList.jsp'

#Mail set
MAIL_HOST = "smtp.qq.com"
MAIL_USER = "HNUSTer"
MAIL_PWD  = "WeAreHNUSTer"
MAIL_POSTFIX = "qq.com"
FROM_MAIL = MAIL_USER + "<"+MAIL_USER+"@"+MAIL_POSTFIX+">"
MSG_SUBJECT = '湖南科技大学图书馆自动续借系统'
