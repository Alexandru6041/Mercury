from django import forms
from django.core.exceptions import ValidationError

from functions.functions import MappedColumn

def validate_file(file):
    if file.name.split('.')[-1].lower() != 'xlsx':
        raise ValidationError('Fisierul incarcat nu are format .xlsx!')
    
    elif file.size / 10**6 > 50:
        raise ValidationError('Fisierul incarcat este prea mare!')

def check_range(range:str):
    if range.count('-') != 1:
        raise ValidationError('Intervalul scris nu este valid')
    
    l1, l2 = range.split('-')

    try:
        l1, l2 = int(l1), int(l2)
    
    except ValueError:
        raise ValidationError('Intervalul scris nu este valid')

class FormIesiri(forms.Form):
    file = forms.FileField(required=True, label='Fisierul .xlsx', validators=[validate_file])
    sheet = forms.CharField(required=True)
    header_row = forms.IntegerField(required=True, label='Randul cu header')
    furnizor_nume = forms.CharField(max_length=100, label="Numele Furnizorului")
    furnizor_cif = forms.IntegerField(label="CUIul Furnizorului")

class FormIntrari(forms.Form):
    file = forms.FileField(required=True, label='Fisierul .xlsx', validators=[validate_file])
    sheet = forms.CharField(required=True)
    header_row = forms.IntegerField(required=True, label='Randul cu header')
    client_nume = forms.CharField(max_length=100, label="Numele Clientului")
    client_cif = forms.IntegerField(label="CUIul Clientului")

class FormMap(forms.Form):
    interval = forms.CharField(initial='1-10', required=True, label='Interval*', validators=[check_range])

    def __init__(self, _type:int, *args, **kwargs):
        super(FormMap, self).__init__(*args, **kwargs)
        self.type = _type

        FIELDS = [
            'nrdoc',
            'denpr',
            ('um', 'unitate de masura'),
            ('cant', 'cantitate'),
            'pret',
            ('val', 'valoare'),
            ('cota_tva', 'cota tva'),
            'tva',
            ('cont', 'cont contabil'),
            'data'
        ]

        if _type: #iesiri
            FIELDS += [
                ('nume_cli', 'nume client'),
                ('cif_cli', 'cif client'),
            ]

        else: #intrari
            FIELDS += [
                ('nume_fur', 'nume furnizor'),
                ('cif_fur', 'cif furnizor'),
                ('pv', 'pret vanzare')
            ]

        for field in FIELDS:
            if type(field) == str:
                self.fields[field] = forms.CharField(max_length=40, required=False, label=field.upper())
            
            else:
                self.fields[field[0]] = forms.CharField(max_length=40, required=False, label=field[1].upper())
    
    def proccess(self, nume_firma, cif_firma):
        data = self.cleaned_data
        l1, l2 = str(data['interval']).split('-')
        for key in data:
            if data[key] and data[key][0] == '&':
                data[key] = MappedColumn(data[key][1:])
            
            elif not data[key]:
                data[key] = ''
        
        data.pop('interval')
        if self.type:
            data.update({
                'nume_fur': nume_firma,
                'cif_fur': cif_firma
            })

        else:
            data.update({
                'pv': '',
                'nume_cli': nume_firma,
                'cif_cli': cif_firma
            })

        return data, int(l1), int(l2)
