#!/usr/bin/python2
# -*- coding:utf-8 -*-
from api import CHECK, SERVER
if __name__=='__main__':
	#get stu_id,stu_passwd,stu_mail . type is a tuple
	stu_data = SERVER.db('GET',None)
	for stu in stu_data:
		SERVER.logging.info("starting : %s"%(stu[0]))
		borrow_content = CHECK.collectReaderBorrowContent(stu[0],stu[1],stu[2])
		if borrow_content:
			if isinstance(borrow_content, str):	
				#if logging login error info
				SERVER.logging.warning('%s, %s'%(stu[0], borrow_content))	
			else:
				table = CHECK.getBorrowInfo(borrow_content)	
				renew_info = CHECK.renewBook(table)	
				#table and renew_info type is list['dict']
				if renew_info :
					mail_content = CHECK.mailContentHand(stu[0], renew_info, table)
					SERVER.sendEmail(stu[0], stu[2], mail_content)
				else:
					SERVER.logging.info("%s, Don't need renew book"%(stu[0]))
		else :
			SERVER.logging.info("%s, no borrow book"%(stu[0]))