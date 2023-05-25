from django import forms
from string import Template

def generate_form_html(fields:dict, template:str, post:dict={}):
    html_form = ''
    with open('templates/html/field.html', 'r') as f:
        field_template = Template(f.read())
    
    for field in fields:
        _type = 'text'
        value = None

        match(type(fields[field])):
            case forms.FileField:
                _type = 'file'
            
            case forms.IntegerField:
                _type = 'number'
                if post:
                    value = post[field]
            
            case _:
                if post:
                    value = post[field]
                _type = 'text'
                
        html_form += field_template.substitute({
            'type': _type,
            'placeholder': fields[field].label,
            'name': field,
            'value': '' if not value else value,
            'required': 'required' if(fields[field].required) else ''
        }) + '\n'
    
    with open(template, 'r') as f:
        html_template = Template(f.read())
    
    return html_template.substitute({'form': html_form})