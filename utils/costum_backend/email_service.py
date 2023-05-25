import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Mercury.settings import EMAIL_ACCOUNT, EMAIL_ACCOUNT_PASSWORD, EMAIL_HOST, EMAIL_HOST_PORT

class EmailServiceProvider:
    def __init__(self):
        '''
        Initializeaza conexiunea cu serverul SMTP
        '''
        self.messages = []
        self.smtp = smtplib.SMTP(host=EMAIL_HOST, port=EMAIL_HOST_PORT)

        self.smtp.ehlo()
        self.smtp.starttls()
        self.smtp.login(EMAIL_ACCOUNT, EMAIL_ACCOUNT_PASSWORD)
    
    def close_smtp(self):
        '''
        Inchide conexiunea cu serverul SMTP
        '''
        self.smtp.close()
    
    @staticmethod
    def create_message(to:str, _from:str, subject:str, body) -> MIMEMultipart:
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

    def add_message(self, message:MIMEMultipart):
        self.messages.append(message)
    
    def send(self):
        try:
            for x, message in enumerate(self.messages):
                self.smtp.send_message(message)
            
            self.messages.clear()
        
        except:
            pass

if __name__ == '__main__':
    email_service = EmailServiceProvider()
    email_service.add_message(EmailServiceProvider.create_message(
        'cacenschivlad@gmail.com',
        'Echipa Mercury',
        'Test clasa EmailServiceProvider',
        MIMEText('acesta este un test\nVom vedea daca noua clasa functioneaza in\n\tTotalitate!')))

    email_service.send()
    email_service.close_smtp()
