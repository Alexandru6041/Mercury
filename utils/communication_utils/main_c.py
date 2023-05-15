from __future__ import print_function
import sib_api_v3_sdk
from random import randint
from sib_api_v3_sdk.rest import ApiException


class gService(object):
    
    def send_mail(name_from, email_from, email_to, name_to, Subject, Context):
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = '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'

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration))
        subject = Subject
        sender = {"name": "{}".format(
            name_from), "email": "{}".format(email_from)}
        html_content = Context
        to = [{"email": "{}".format(email_to), "name": "{}".format(name_to)}]

        # params = {"parameter": "My param value", "subject": "New Subject"}

        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=to, html_content=html_content, sender=sender, subject=subject)

        try:
            api_response = api_instance.send_transac_email(send_smtp_email)
            print(api_response)
        except ApiException as e:
            print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
        
    def generate_pin():
        sol = 0
        numbers = []
        
        for i in range(6):
            numbers.append(randint(0, 9))
        
        for digit in numbers:
            sol = sol * 10 + digit
            
        numbers.clear()
        return sol    
        