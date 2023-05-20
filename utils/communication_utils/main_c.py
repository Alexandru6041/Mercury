from __future__ import print_function
import sib_api_v3_sdk
from random import randint
from jinja2 import Template

class gService(object):
    
    def __read_html_file(path):
        with open(path, "r") as file:
            content = Template(file.read())
        
        return content
    
    def send_mail(name_from, email_from, email_to, name_to, Subject, path_to_html, pin, request):
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = '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'

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration))
        subject = Subject
        sender = {"name": "{}".format(
            name_from), "email": "{}".format(email_from)}
        
        html_content = gService.__read_html_file(path_to_html).render(name_from = name_from, name_to = name_to, pin = pin)
        
        to = [{"email": "{}".format(email_to), "name": "{}".format(name_to)}]

        # params = {"parameter": "My param value", "subject": "New Subject"}

        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=to, html_content=html_content, sender=sender, subject=subject)

        # try:
        #     api_response = api_instance.send_transac_email(send_smtp_email)
        #     return api_response
        # except ApiException as e:
        #     return render(request, "502.html", status = 502)
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
            
    
    def generate_pin():
        sol = 0
        numbers = []
        
        for i in range(6):
            numbers.append(randint(0, 9))
        
        for digit in numbers:
            sol = sol * 10 + digit
            
        numbers.clear()
        return sol    
        