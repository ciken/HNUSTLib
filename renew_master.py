#!/usr/bin/python2
# -*- coding:utf-8 -*-
#version:1.4.1
#Autor:ciken
#Email:ciken@live.cn
from api import CHECK, SERVER
if __name__=='__main__':
	#get stu_id,stu_passwd,stu_mail . type is a tuple
	stu_data = SERVER.db('GET', None)
	for stu in stu_data:
		stu_id = stu[0];stu_lib_passwd = stu[1]; stu_lib_mail = stu[2]
		SERVER.logging.info("starting : %s"%(stu[0]))
		stu_lib_secret_false = CHECK.checkReaderPasswd(stu_id, stu_lib_passwd)
		if stu_lib_secret_false:
			SERVER.db('SWITCH', [stu_id, '0'])
			SERVER.logging.info("%s, %s"%(stu_id, stu_lib_secret_false))
			mail_content = '您的图书馆帐号<b style="color:red">%s</b>由于<b style="color:blue">%s</b>的原因，将不能再享受自动续借的功能。若要继续享受图书馆自动续借，请重新登记。如有疑问，请联系邮箱：ciken@live.cn'%(stu_id, stu_lib_secret_false)
			SERVER.sendEmail(stu_id, stu_lib_mail, mail_content)
		else:
			borrow_content = CHECK.collectReaderBorrowContent(stu_id, stu_lib_passwd)
			if borrow_content:
				if isinstance(borrow_content, str):	
					#if logging login error info
					SERVER.logging.warning('%s, %s'%(stu_id, borrow_content))	
				else:
					CHECK.getBorrowInfo(stu_id, borrow_content)	
					is_renew = CHECK.renewBook(stu_id)	
					#table and renew_info type is list['dict']
					if is_renew :
						mail_content = CHECK.mailContentHand(stu_id)
						SERVER.sendEmail(stu_id, stu_lib_mail, mail_content)
					else:
						SERVER.logging.info("%s, Don't need renew book"%(stu_id))
			else :
				SERVER.logging.info("%s, no borrow book"%(stu_id))