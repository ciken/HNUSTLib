#!/usr/bin/python2
# -*- coding:utf-8 -*-
import requests,re
import CONF

def libConnect():
	try:
		global lib
		lib = requests.session()
		#test connec to lib
		lib.get(CONF.LIB_URL + CONF.LIB_LOGIN_URL[0])
		return False

	except Exception,e:
		return e

def calcDate(Date):
	return (CONF.date(int(Date[0]), int(Date[1]), int(Date[2])) - CONF.TODAY).days

def checkReaderPasswd(stu_id, stu_passwd ):
	lib_request_url = CONF.LIB_URL + CONF.LIB_LOGIN_URL[0] + stu_id + CONF.LIB_LOGIN_URL[1] +stu_passwd
	lib_request_return_content = lib.get(lib_request_url).text
	if 'alert' in lib_request_return_content:
		return re.search(r'(?<=alert.").+?(?=")', lib_request_return_content).group(0).encode('utf-8')
	else:
		return False

def collectReaderBorrowContent(stu_id, stu_passwd ):
	from bs4 import BeautifulSoup
	#获取数据并提取信息
	borrow_html_content = lib.get(CONF.LIB_BORROW_INFO_URL).text
	borrow_content = BeautifulSoup(borrow_html_content).find(attrs={"cellpadding":"2"})
	return borrow_content
		
	
def getBorrowInfo(stu_id, borrow_content):
	borrow_table = borrow_content.find_all(re.compile("td"))
	i=0; table=[]
	for tag in borrow_table:
		if not tag.has_attr('class') and not tag.has_attr('background'):
			if i%5==0:
				table.append({'seq':'', 'name':'', 'deadline':'', 'barcode':'', 'department_id':'', 'library_id':'', 'expire':'', 'renrw_return_info':None})
				table[i/5]['seq']=int(tag.string)
			elif i%5==1:
				table[i/5]['name']=tag.string
			elif i%5==2:
				pass
			elif i%5==3:
				table[i/5]['deadline']=tag.string
			else:
				#get re new information
				temp=(re.search(r'(?<=Renew..).+?(?=..;)',str(tag.contents[0])).group(0)).split("','")
				from copy import deepcopy
				table[i/5]['barcode']=deepcopy(temp[0])
				table[i/5]['department_id']=deepcopy(temp[1])
				table[i/5]['library_id']=deepcopy(temp[2])
				table[i/5]['expire'] = calcDate(table[i/5]['deadline'].split('/'))
			i+=1;
	return table 	#table type is list[dict]

def renewStu(stu_id, borrow_table):
	# borrow_table=json.load(file("%s/json/%s.json"%(CONF.WORKSPACE_DIR, stu_id)))
	try_renew = False
	for book in borrow_table:
		if abs(int(book['expire'])) < CONF.RENEW_BOOK_EXPIRED_TIME :
			renew_info = renewBook(book['barcode'], book['department_id'], book['library_id'])
			if renew_info['book_deadline'] :
				book['deadline'] = renew_info['book_deadline']
				book['expire'] = renew_info['book_expire']
			book['renrw_return_info'] = renew_info['lib_renew_return_content']
			try_renew=True
	# return renew_return_content
	if try_renew:
		return borrow_table
	else :
		return False

def renewBook(book_barcode, department_id, library_id):
	book_deadline = ''; book_expire = '',
	post_data = {'action':'Renew', 'book_barcode':book_barcode, 'department_id':department_id, 'library_id':library_id,}
	lib_renew_return_content = (re.search(r'(?<=alert..).+(?=")', lib.post(CONF.LIB_BORROW_INFO_URL, post_data).text)).group(0)
	if u'续借成功' in lib_renew_return_content :
		book_deadline  = (re.search(r'\d{4}/\d{2}/\d{2}', lib_renew_return_content)).group(0)
		book_expire = int((re.search(u'(?<=共计).+?(?=天)', lib_renew_return_content)).group(0))
		print book_expire,book_deadline
	return {'lib_renew_return_content':lib_renew_return_content, 'book_deadline':book_deadline, 'book_expire':book_expire}

def mailContentHand(stu_id, borrow_table):
	# lib_table=json.load(file("%s/json/%s.json"%(CONF.WORKSPACE_DIR, stu_id)))
	mail_content="<br><br><table border='1'> \
	<tr align='center'><th colspan='3'>图书续借情况 (距应还日期 %d 天自动续借)</th></tr>\
	<tr align='center'>\
		<th>图书条码</th>\
		<th>图书题名</th>\
		<th>续借情况</th>\
	</tr>\
	"%(CONF.RENEW_BOOK_EXPIRED_TIME)
	for renew_info_temp in borrow_table:
		if not renew_info_temp['renrw_return_info'] :
			continue
		if u'续借失败' in renew_info_temp['renrw_return_info'] :
			style_color = 'style="color:red"'
		else :
			style_color = ''
		mail_content += "<tr %s>\
			<th>%s</th>\
			<th>%s</th>\
			<th>%s</th>\
		</tr>"%(style_color, str(renew_info_temp['barcode']), str(renew_info_temp['name'].encode('utf-8')), str(renew_info_temp['renrw_return_info'].encode('utf-8')))
	mail_content += "</table><br><br>\
	<table border='1'>\
	<tr align='center'><th colspan='4'>图书借阅信息 (%s)</th></tr>\
	<tr align='center'>\
		<th>图书条码</th>\
		<th>图书题名</th>\
		<th>应还日期</th>\
		<th>剩（天）</th>\
	</tr>\
	"%(stu_id)
	for table_temp in borrow_table:
		# print  book['barcode'], book['name'], book['deadline'], book['expire']
		if int(table_temp['expire']) < 0 :
			style_color = 'style="color:red"'
		elif int(table_temp['expire']) < 7:
			style_color = 'style="color:blue"'
		else:
			style_color = ''
		mail_content +="<tr %s>\
			<th>%s</th>\
			<th>%s</th>\
			<th>%s</th>\
			<th>%s</th>\
		</tr>"%(style_color, str(table_temp['barcode']), str(table_temp['name'].encode('utf-8')), str(table_temp['deadline'].encode('utf-8')), str(table_temp['expire']))
	mail_content +="</table></br></br>"
	return mail_content