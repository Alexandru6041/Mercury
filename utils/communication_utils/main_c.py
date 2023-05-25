from __future__ import print_function
from random import randint
from jinja2 import Template
from django.shortcuts import render
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Mercury.settings import EMAIL_ACCOUNT, EMAIL_ACCOUNT_PASSWORD, EMAIL_HOST, EMAIL_HOST_PORT

class gService(object):
    
    def __init__(self):
        '''
        Initializeaza conexiunea cu serverul SMTP
        '''
        self.messages = []
        self.smtp = smtplib.SMTP(host=EMAIL_HOST, port=EMAIL_HOST_PORT)

        self.smtp.ehlo()
        self.smtp.starttls()
        self.smtp.login(EMAIL_ACCOUNT, EMAIL_ACCOUNT_PASSWORD)

    @staticmethod
    def read_html_file(path):
        with open(path, "r") as file:
            content = Template(file.read())
        
        return content
    
    def close_smtp(self):
        '''
        Inchide conexiunea cu serverul SMTP
        '''
        self.smtp.close()

    @staticmethod
    def create_message(to: str, _from: str, subject: str, body) -> MIMEMultipart:
        '''
        Instantiaza un mesaj de tip MIMEMultipart.
        body: MIME
        '''
        message = MIMEMultipart()
        message['from'] = _from
        message['to'] = to
        message['subject'] = subject

        message.attach(body)

        return message

    def add_message(self, message: MIMEMultipart):
        self.messages.append(message)

    def send(self):
        try:
            for x, message in enumerate(self.messages):
                self.smtp.send_message(message)

            self.messages.clear()

        except:
            pass
    
    @staticmethod
    def send_message(to, _from, subject, name_from, name_to, pin, path_to_html, request):
        try:
            email_service = gService()
            context = MIMEText(gService.read_html_file(path_to_html).render(name_from = name_from, name_to = name_to, pin = pin), _subtype="html")
            email_service.add_message(gService.create_message(to, _from, subject, context))
            email_service.send()
            email_service.close_smtp()
        except:
            return render(request, "502.html", status = 502)
    
    def generate_pin():
        sol = 0
        numbers = []
        
        for i in range(6):
            numbers.append(randint(0, 9))
        
        for digit in numbers:
            sol = sol * 10 + digit
            
        numbers.clear()
        return sol