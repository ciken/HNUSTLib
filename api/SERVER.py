#!/usr/bin/python2
# -*- coding:utf-8 -*-
import logging
import CONF


def db(operator, data):
	import MySQLdb
	db = MySQLdb.connect(CONF.DB_HOST, CONF.DB_USER, CONF.DB_PASSWD, CONF.DB_NAME)
	try:
		cursor = db.cursor()
		if operator == 'GET':
			sql = 'SELECT stu_id,stu_passwd,stu_mail FROM lib WHERE renew_switch=1'
			cursor.execute(sql)
			return cursor.fetchall()
		elif operator == 'ADD':
			#data[0]=stu_id, data[1]=stu_passwd, data[2]=stu_mail
			sql= 'INSERT INTO lib VALUES("%s","%s","%s",1)'%(data[0],data[1],data[2])
		elif operator == 'SWITCH':
			#data[0]=switch,data[1]=stu_id
			sql = 'UPDATE lib SET renew_switch=%s WHERE stu_id=%s'%(data[1], data[0])
		elif operator == 'DEL':
			#data=stu_id
			sql = 'DELETE FROM lib WHERE stu_id=%s'%(data)
		else:
			pass
		cursor.execute(sql)
		db.commit()
	except:
		db.rollback()
	finally:
		db.close()

def sendEmail(stu_id, stu_mail, msg_content):
	import smtplib
	from email.mime.text import MIMEText
	TO_MAIL = stu_mail
	MSG = MIMEText(msg_content,'html', _charset='utf8')
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
		logging.error('%s , %s has no send Email because : %s'%(stu_id, stu_mail, e))
		return False

logging.basicConfig(
	level=logging.INFO,
	format=CONF.LOG_CONTENT_FORMAT,
	datefmt=CONF.LOG_DATE_FROAMTE,
	filename=CONF.LOG_RENEW_FILE_NAME,
	filemode=CONF.LOG_FILE_MODE,)