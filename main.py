#!/usr/bin/python
#-*- coding:utf8 -*- 
import CONF
import SERVER
import CHECK
#main Function
if __name__=="__main__":
    readers_id=[]; readers_mail=[];i=0
    readers_id,readers_mail,readers_len = CHECK.getStuID()
    for i in range (0,readers_len) :
        have_content,borrow_html_content = CHECK.stuCheck(readers_id[i])
        if have_content == True:
            book_now_information=' 您的当前借阅信息如下：\n' + '\n图书条码     /     图书题名    /     应还日期\n';
            book_renew_information = CHECK.renewBook(borrow_html_content)
            if len(book_renew_information)<70:
                SERVER.log(readers_id[i],"Don't need Renew book")
                continue
            have_content,borrow_html_content = CHECK.stuCheck(readers_id[i])
            is_borrow_num,book_coding,book_name,book_borrow_endtime,book_department_id,book_library_id = CHECK.collectReaderBorrowContent(borrow_html_content)
            for borrow_num in range(0,is_borrow_num):
                book_now_information += str(book_coding[borrow_num]) + '      ' + str(book_name[borrow_num]) + '      ' +str(book_borrow_endtime[borrow_num])[0:10] + '\n'
            email_msg_content = '\n已尝试帮您续借如下书籍:\n'+book_renew_information+'\n' + book_now_information
            is_send_mail = SERVER.sendEmail(readers_mail[i],email_msg_content)
            SERVER.log(readers_id[i],email_msg_content)
        elif have_content == False and borrow_html_content == 'No borrow book!':
             SERVER.log(readers_id[i],'no borrow book')
        else:
             SERVER.log(readers_id[i],borrow_html_content)
