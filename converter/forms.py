from django import forms
from django.core.exceptions import ValidationError

def validate_file(file):
    if file.name.split('.')[-1].lower() != 'xlsx':
        raise ValidationError('Fisierul incarcat nu are format .xlsx!')
    
    elif file.size / 10**6 > 50:
        raise ValidationError('Fisierul incarcat este prea mare!')

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
    interval = forms.CharField(initial='1-10', required=True, label='Interval*')

    def __init__(self, tip:int, *args, **kwargs):
        super(FormMap, self).__init__(*args, **kwargs)

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

        if tip: #iesiri
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
