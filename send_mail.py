#!/usr/bin/env python
#-*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender = 'admin@xxx.com.cn'

receivers = ['sb@xxx.com.cn']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

# 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码

body = '''
您好:
    目前已对邮件系统进行升级，各位同事需在新邮件系统上线前进行登录认证。
    否则新邮件系统上线后无法正常接收邮件，影响正常工作。
    新邮件系统认证地址:
        http://163.44.xxx.xxx/

----
'''

message = MIMEText(body, 'plain', 'utf-8') #body
message['From'] = Header("邮箱管理员", 'utf-8')
message['To'] =  Header("", 'utf-8')

subject = '【重要】邮件系统升级通知' #标题
message['Subject'] = Header(subject, 'utf-8')
mail_host = 'mail.xxx.com.cn'

try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)
    smtpObj.login('xxx', 'pass')
    smtpObj.sendmail(sender, receivers, message.as_string())
    print "邮件发送成功"
except smtplib.SMTPException as e:
    print(e)
    print "Error: 无法发送邮件"
