#!/usr/bin/env python
'''Configure Email to be sent'''

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import sotero_password


class NoticeEmail(object):
    def __init__(self, to_address):
        self.login_address = 'websotero@gmail.com'
        self.to_address = to_address
        self.msg = MIMEMultipart()
        self.msg['From'] = self.login_address
        self.msg['To'] = self.to_address

        self.server = smtplib.SMTP('smtp.gmail.com', 587)

    def send_message(self, subject, msg):
        self.msg['Subject'] = subject
        body = msg
        self.msg.attach(MIMEText(body, 'plain'))
        text = self.msg.as_string()

        self.server.ehlo()
        self.server.starttls()
        self.server.login(self.login_address, sotero_password.password)
        self.server.sendmail(self.login_address, self.to_address, text)
        self.server.quit()
