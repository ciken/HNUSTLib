#!/usr/bin/python
#-*- coding:utf8 -*- 
import CONF
import datetime
import re
import requests

lib = requests.session()

#start collect message
def collectReaderBorrowContent(borrow_html_content):
    #判断借了几本书
    is_borrow_num = borrow_html_content.count('确实要续借吗')
    book_renewcode = re.findall(r"(Renew.'.+?);",borrow_html_content)
    #将续借需要的编码提取出来
    book_coding=[];book_department_id=[];book_library_id=[]
    for i in range(0,is_borrow_num):
        book_coding.append(re.findall(r"'(\w{10})'",book_renewcode[i]))
        book_department_id.append(re.findall(r"'(\w{2})'",book_renewcode[i]))
        book_library_id.append(re.findall(r"'(\w{1})'",book_renewcode[i]))
    book_name_date = re.findall(r";</td><td>(.+?)&nbsp;<",borrow_html_content)
    book_name=[]; book_date=[]; book_borrow_endtime=[];
    for i in range (0,is_borrow_num):
        #将还书过期日期截取出来
        book_borrow_endtime.append(datetime.datetime(int(book_name_date[i*2+1][:4]),int(book_name_date[i*2+1][5:7]),int(book_name_date[i*2+1][8:11])))
        #计算还书过期剩余时间
        book_name.append(book_name_date[i*2])
        book_date.append(book_name_date[i*2+1])
    return is_borrow_num,book_coding,book_name,book_borrow_endtime,book_department_id,book_library_id


def renewBook(borrow_html_content):
    is_borrow_num,book_coding,book_name,book_borrow_endtime,book_department_id,book_library_id = collectReaderBorrowContent(borrow_html_content)
    book_borrow_expired=[];book_renew_information='\n图书条码     /     图书题名    /     续借情况\n'
    for i in range (0,is_borrow_num):
        book_borrow_expired.append((book_borrow_endtime[i] - CONF.TODAY).days)
        if abs(book_borrow_expired[i]) < CONF.RENEW_BOOK_EXPIRED_TIME:
            postData = {'action':'Renew', 'book_barcode':str(book_coding[i])[2:-2], 'department_id':str(book_department_id[i])[2:-2], 'library_id':str(book_library_id[i])[2:-2],};
            lib_renew_back_content = lib.post(CONF.LIB_BORROW_INFO_URL,postData).text.decode('gbk').encode('utf8')
            book_renew_information +=  str(book_coding[i]) + '     '+ book_name[i] + '     '+ re.findall(u'alert."(.+?)"',lib_renew_back_content)[0]+'\n'
    return book_renew_information



#stuID check
def stuCheck(stu_id,stu_password = '888888'):
    lib_request_url = CONF.LIB_URL + CONF.LIB_LOGIN_URL[0]+stu_id + CONF.LIB_LOGIN_URL[1] + stu_password
    lib_request_url_return_content = lib.get(lib_request_url).text
    if 'alert' in lib_request_url_return_content:
        login_error_information = re.findall(u'alert."(.+?)"',lib_request_url_return_content)[0]
        return False,login_error_information
    else:
        #获取数据并提取信息
        borrow_html_content = lib.get(CONF.LIB_BORROW_INFO_URL).text.decode('gbk').encode('utf8')
        #判断是否借书
        is_borrow = borrow_html_content.find('topictitle2')
        #截取字符串提高效率
        if is_borrow!=-1:
            borrow_html_content = re.search(r'topictitle2(.+)name="frmDelRecomm',borrow_html_content).group(0)
            return True,borrow_html_content
        else :
            return False,'No borrow book!'

#get student id
def getStuID():
    readers_file = open(CONF.STU_ID_FILE,'r')
    readers = readers_file.readlines()
    readers_len = len(readers)
    readers_file.close()
    readers_id = []; readers_mail=[];
    for i in range (0,readers_len):
        readers_id_temp,readers_mail_temp = readers[i].split('---',1)
        readers_id.append(readers_id_temp)
        readers_mail.append(readers_mail_temp[:-1])
    return readers_id,readers_mail,readers_len
