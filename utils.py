import smtplib
import os
from email.message import EmailMessage
import requests
import json


class Email:
    def __init__(self):
        self.recipient = os.environ['RECIPIENT']
        self.sender = os.environ["SENDER"]
        self.subject = 'Dizzle Question Suggestion'
        password = os.environ['PASSWORD']
        self.server = smtplib.SMTP_SSL('smtp.yandex.com', 465)
        self.server.login(self.sender, password)
        print('Connected')

    def sendEmail(self, email):
        msg = EmailMessage()
        msg.set_content(email)
        msg['Subject'] = self.subject
        msg['From'] = self.sender
        msg['To'] = self.recipient
        try:
            self.server.send_message(msg)
            print('Email successfully sent')
            return True
        except Exception as e:
            print(e)
            return False


def is_human(captcha_response):
    """
    Validating recaptcha response from google server
    Returns True captcha test passed for submitted form else returns False.
    """
    secret = os.environ['CAPTCHA_SECRET_KEY']
    payload = {'response': captcha_response, 'secret': secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify",
                             payload)
    response_text = json.loads(response.text)
    return response_text['success']
