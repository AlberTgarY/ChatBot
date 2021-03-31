import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import  encoders
def send(filename):
    msg_from = os.environ['EMAIL']
    passwd = os.environ['PASSWD']
    msg_to = []
    subject = "Slackbot history file"

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = msg_from

    msg.attach(MIMEText('This is a test file!!!', 'plain', 'utf-8'))

    att1 = MIMEText(open(filename, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="test.txt"'
    msg.attach(att1)

    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print('Done')
    except s.SMTPException as e:
        print(e)
    finally:
        s.quit()