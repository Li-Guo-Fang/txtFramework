import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr

def send_mail():
    mail_host="smtp.qq.com"  #设置服务器
    mail_user="367224698@qq.com"    #用户名
    mail_pass="自己的口令，这里需要百度下客户端发送邮件时的密码"   #口令
    sender = '367224698@qq.com'
    receivers = ['367224698@qq.com'] # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    # 创建一个带附件的实例
    message = MIMEMultipart()
    # print("message: %s" % message)
    # print("type(message): %s" % type(message))
    message['From'] = formataddr(["李国芳", "367224698@qq.com"])
    message['To'] = ','.join(receivers)
    subject = '接口自动化测试执行报告'
    message['Subject'] = Header(subject, 'utf-8')
    message["Accept-Language"]="zh-CN"
    message["Accept-Charset"]="ISO-8859-1,utf-8,gbk"
    # 邮件正文内容
    message.attach(MIMEText('最新执行的接口自动化测试报告，请参阅附件内容！', 'plain', 'utf-8'))

    # 构造附件1，传送测试结果的excel文件
    att = MIMEBase('application', 'octet-stream')
    att.set_payload(open("接口测试报告.html", 'rb').read())
    att.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', "接口测试报告.html"))
    encoders.encode_base64(att)
    message.attach(att)


    try:
        smtpObj = smtplib.SMTP(mail_host)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件", e)

if __name__ == '__main__':
    send_mail()

