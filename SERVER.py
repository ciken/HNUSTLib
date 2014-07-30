#!/usr/bin/python
#-*- coding:utf8 -*- 
import CONF
import time
import smtplib
from email.mime.text import MIMEText
def sendEmail(stu_mail,msg_content):
    TO_MAIL = stu_mail
    MSG = MIMEText(msg_content,_charset='utf8')
    MSG['Subject'] = CONF.MSG_SUBJECT
    MSG['From'] = CONF.FROM_MAIL
    MSG['To'] = TO_MAIL
    try:
        MAIL = smtplib.SMTP()
        MAIL.connect(CONF.MAIL_HOST)
        MAIL.login(CONF.MAIL_USER,CONF.MAIL_PWD)
        MAIL.sendmail(CONF.FROM_MAIL, TO_MAIL, MSG.as_string())
        MAIL.close()
        return True
    except Exception,e:
        log(stu_mail,e)
        return False


def log(reader,log_content):
    fp = open(CONF.LOG_DIR+str(CONF.TODAY)[:10]+'.log',"a+")
    fp.write(time.strftime('%Y.%m.%d-%H.%M.%S\n',time.localtime(time.time())))
    fp.write(reader+'\n'+str(log_content)+'\n\n\n')
    fp.close()