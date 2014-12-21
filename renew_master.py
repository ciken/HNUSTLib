#!/usr/bin/python2
# -*- coding:utf-8 -*-
#version:1.4.2
#Autor:ciken
#Email:ciken@live.cn
from api import CONF, SERVER, CHECK
import json, codecs

def libConnectTest():
	lib_connect_fail = CHECK.libConnect()
	if lib_connect_fail:
		SERVER.logging.error("URL get request error,because: %s"%(e))
		SERVER.sendEmail(None, CONF.ADMIN_MAIL, 'Lib get request ERROR, %s'%(e))
		exit(0)
	else :
		return True

def stuLibSecretFalseHand(stu_id, stu_lib_mail, stu_lib_secret_false_reason):
	SERVER.db('SWITCH', [stu_id, '0'])
	SERVER.logging.info("%s, %s"%(stu_id, stu_lib_secret_false_reason))
	mail_content = '您的图书馆帐号<b style="color:red">%s</b>由于<b style="color:blue">%s</b>的原因，将不能再享受自动续借的功能。若要继续享受图书馆自动续借，请重新登记。如有疑问，请联系邮箱：ciken@live.cn'%(stu_id, stu_lib_secret_false)
	SERVER.sendEmail(stu_id, stu_lib_mail, mail_content)

def stuLibSecretTrueHand(stu_id, stu_lib_passwd, stu_lib_mail):
	borrow_content = CHECK.collectReaderBorrowContent(stu_id, stu_lib_passwd)
	if borrow_content:
		if isinstance(borrow_content, str):
			#if logging login error info
			SERVER.logging.warning('%s, %s'%(stu_id, borrow_content))
		else:
			borrow_table = CHECK.getBorrowInfo(stu_id, borrow_content)
			is_renew = CHECK.renewStu(stu_id, borrow_table)
			#table and renew_info type is list['dict']
			if is_renew :
				borrow_table = is_renew
				mail_content = CHECK.mailContentHand(stu_id, borrow_table)
				SERVER.sendEmail(stu_id, stu_lib_mail, mail_content)
			else:
				SERVER.logging.info("%s, Don't need renew book"%(stu_id))
			json.dump(borrow_table , codecs.open("%sjson/%s.json"%(CONF.WORKSPACE_DIR, stu_id),"w+",encoding='utf-8'),indent=2,ensure_ascii =False)
	else :
		SERVER.logging.info("%s, no borrow book"%(stu_id))

if __name__=='__main__':
	#get stu_id,stu_passwd,stu_mail . type is a tuple
	libConnectTest()
	stu_data = SERVER.db('GET', None)
	for stu in stu_data:
		stu_id = stu[0];stu_lib_passwd = stu[1]; stu_lib_mail = stu[2]
		SERVER.logging.info("starting : %s"%(stu[0]))
		stu_lib_secret_false = CHECK.checkReaderPasswd(stu_id, stu_lib_passwd)
		if stu_lib_secret_false:
			stuLibSecretFalseHand(stu_id, stu_lib_mail, stu_lib_secret_false)
		else:
			stuLibSecretTrueHand(stu_id, stu_lib_passwd, stu_lib_mail)