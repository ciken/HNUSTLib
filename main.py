#!/usr/bin/python
#-*- coding:utf-8 -*- 
print "Version 1.1"
print "Autor:ciken"
import os
import datetime
import time
import urllib2
import cookielib
import re
import socket
import smtplib
from email.mime.text import MIMEText

today = datetime.datetime.now()
cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
#send e-mail to reader
def sendEmail(stu_mail,msg_content):
    MAIL_HOST = "smtp.qq.com"
    MAIL_USER = "HNUSTer"
    MAIL_PWD  = "WeAreHNUSTer"
    MAIL_POSTFIX = "qq.com"
    FROM_MAIL = MAIL_USER + "<"+MAIL_USER+"@"+MAIL_POSTFIX+">"
    TO_MAIL = stu_mail
    MSG = MIMEText(msg_content)
    MSG['Subject'] = '湖南科技大学图书馆自动续借系统'
    MSG['From'] = FROM_MAIL
    MSG['To'] = TO_MAIL
    try:
        MAIL = smtplib.SMTP()
        MAIL.connect(MAIL_HOST)
        MAIL.login(MAIL_USER,MAIL_PWD)
        MAIL.sendmail(FROM_MAIL, TO_MAIL, MSG.as_string())
        MAIL.close()
        return True
    except Exception,e:
        log(stu_mail,e)
        return False
#start collect message
def collectReaderBorrowContent(borrow_html_content):
    jsessionid = re.findall(r"JSESSIONID=(.+?)\s",str(cookie))[0]
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

    book_name=[]; book_date=[]; book_borrow_endtime=[]; book_borrow_expired=[]; book_renew_information=''
    for i in range (0,is_borrow_num):
        #将还书过期日期截取出来
        book_borrow_endtime.append(datetime.datetime(int(book_name_date[i*2+1][:4]),int(book_name_date[i*2+1][5:7]),int(book_name_date[i*2+1][8:11])))
        #计算还书过期剩余时间
        book_borrow_expired.append((book_borrow_endtime[i] - today).days)
        book_name.append(book_name_date[i*2])
        book_date.append(book_name_date[i*2+1])
    for i in range (0,is_borrow_num):
        if book_borrow_expired[i] < 10 :
            os.system( "curl 'http://opac.hnust.cn:8080/reader/infoList.jsp' -H 'Cookie: JSESSIONID="+jsessionid+"' -H 'Connection: keep-alive' --data 'action=Renew&book_barcode="+str(book_coding[i])[2:-2]+"&department_id="+str(book_department_id[i])[2:-2]+"&library_id="+str(book_library_id[i])[2:-2]+"' --compressed")
            #print "curl 'http://opac.hnust.cn:8080/reader/infoList.jsp' -H 'Cookie: JSESSIONID="+jsessionid+"' -H 'Connection: keep-alive' --data 'action=Renew&book_barcode="+str(book_coding[i])[2:-2]+"&department_id="+str(book_department_id[i])[2:-2]+"&library_id="+str(book_library_id[i])[2:-2]+"' --compressed"
            book_renew_information += book_name[i]+'     '+str(book_coding[i])+'\n'
            #print type(book_name[i]),type(book_coding[i])
    return book_renew_information

#stuID check
def stuCheck(stu_id,stu_password = '888888'):
    lib_url = 'http://211.67.223.8:8080/'
    lib_request_url = lib_url + 'reader/login.jsp?str_kind=login&barcode='+stu_id+'&password='+stu_password
    lib_request_url_return_content = opener.open(lib_request_url).read()
    #linux乱码转码
    lib_request_url_return_content = lib_request_url_return_content.decode('gb2312').encode('utf8')
    if 'alert' in lib_request_url_return_content:
        login_error_information = re.findall(u'alert."(.+?)"',lib_request_url_return_content)[0]
        return False,login_error_information
    else:
        #获取数据并提取信息
        borrow_html_content = opener.open(lib_url+'reader/infoList.jsp').read()
        #如果是linux需要转码，否则会乱码
        borrow_html_content = borrow_html_content.decode('gb2312').encode('utf8')
        # print content

        #判断是否借书
        is_borrow = borrow_html_content.find('您的借阅情况如下')

        #截取字符串提高效率
        if is_borrow!=-1:
            borrow_html_content = re.search(r'您的借阅情况如下(.+)name="frmDelRecomm',borrow_html_content).group(0)
            return True,borrow_html_content
        else :
            return False,'No borrow book!'
    
#get student id
def getStuID():
    readers_file = open('/home/pi/HNUSTLibAutomaticallyRenewal/stuID','r')
    readers = readers_file.readlines()
    readers_len = len(readers)
    readers_file.close()
    readers_id = []; readers_mail=[];
    for i in range (0,readers_len):
        readers_id_temp,readers_mail_temp = readers[i].split('---',1)
        readers_id.append(readers_id_temp)
        readers_mail.append(readers_mail_temp[:-1])
    return readers_id,readers_mail,readers_len

def log(reader,log_content):
    fp = open('/home/pi/HNUSTLibAutomaticallyRenewal/log/'+str(today)[:10]+'.log',"a+")
    fp.write(time.strftime('%Y.%m.%d-%H.%M.%S\n',time.localtime(time.time())))
    fp.write(reader+'\n'+log_content+'\n\n\n')
    fp.close()
        
#main Function
if __name__=="__main__":
    readers_id=[]; readers_mail=[];i=0
    readers_id,readers_mail,readers_len = getStuID()
    for i in range (0,readers_len) :
        have_content,borrow_html_content = stuCheck(readers_id[i])
        if have_content == True:
            book_renew_information = collectReaderBorrowContent(borrow_html_content)
            if len(book_renew_information)<10:
                log(readers_id[i],"Don't have need borrow book")
                continue
            have_content,borrow_html_content = stuCheck(readers_id[i])
            book_norenew_information = collectReaderBorrowContent(borrow_html_content)
            email_msg_content = '已尝试帮您续借如下书籍:\n'+book_renew_information+'\n'+'下列书籍未续借成功：\n'+book_norenew_information+'\n'
            is_send_mail = sendEmail(readers_mail[i],email_msg_content) 
            log(readers_id[i],email_msg_content)
        elif have_content == False and borrow_html_content == 'No borrow book!':
             log(readers_id[i],'no borrow')
        else:
             log(readers_id[i],borrow_html_content)

    
