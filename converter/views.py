from django import forms
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from .forms import FormIesiri, FormMap
from functions.functions import *
from .models import FileModel
import datetime

#Third-Party
from utils.hash_utils.hash_utils import SecureHasher
import sqlite3

#Variables
DATABASE_PATH = settings.DATABASES['default']['NAME']

def iesiri(request):
    form = FormIesiri()

    url = request.build_absolute_uri()
    
    try:
        if("?token=" in url):
            sqliteConnection = sqlite3.connect(DATABASE_PATH)
            cursor = sqliteConnection.cursor()
            
            url_token = request.GET.get("token")
            token = url_token
            
            if ("=" in token):
                return render(request, "403.html", status=403)
            
            chiper = SecureHasher.AESCipher()
            dec_token = chiper.decrypt(url_token)
            token = dec_token
            
            valid = cursor.execute("SELECT * FROM main_user WHERE display_name = ?", [token])
            sqliteConnection.commit()
            valid = cursor.fetchall()
            
            if(len(valid) == 0):
                return render(request, "403.html", status = 403)
            
    except Exception as e:
            print(e)
            return render(request, "403.html", status = 403)

    if request.method == 'POST':
        # tip: [0, 1] -> 0 intrari, 1 iesiri
        form = FormIesiri(request.POST, request.FILES)

        if form.is_valid():
            path = save_uploaded_xlsx(request.FILES['file'], 0)

            model = FileModel.objects.create(
                nume=path.split('/')[-1],
                dimensiune=request.FILES['file'].size,
                sheet=form.cleaned_data['sheet'],
                rand_header=form.cleaned_data['header_row'],
                nume_firma=form.cleaned_data['furnizor_nume'],
                cif_firma=form.cleaned_data['furnizor_cif']
                )
            
            file = path.split("/")[-1].split(".")[:-1]
            file = file[0] + '.' + file[1]

            return HttpResponseRedirect(f'iesiri/mapping/{file}')
        
    return render(request, 'iesiri.html', {'form': form})

def mapping(request, file):
    path = f'input files/{file}.xlsx'
    model = FileModel.objects.get(nume=f'{file}.xlsx')

    url = request.build_absolute_uri()
    
    try:
        if("?token=" in url):
            sqliteConnection = sqlite3.connect(DATABASE_PATH)
            cursor = sqliteConnection.cursor()
            
            url_token = request.GET.get("token")
            token = url_token
            
            if ("=" in token):
                return render(request, "403.html", status=403)
            
            chiper = SecureHasher.AESCipher()
            dec_token = chiper.decrypt(url_token)
            token = dec_token
            
            valid = cursor.execute("SELECT * FROM main_user WHERE display_name = ?", [token])
            sqliteConnection.commit()
            valid = cursor.fetchall()
            
            if(len(valid) == 0):
                return render(request, "403.html", status = 403)
            
    except Exception as e:
            print(e)
            return render(request, "403.html", status = 403)

    if request.method == 'POST':
        map = FormMap(1, request.POST)

        if map.is_valid():
            data = dict(map.cleaned_data)
            l1, l2 = str(data['interval']).split('-')
            output_path = f'output files/F_RO{model.cif_firma}_multiple_{datetime.datetime.today().strftime("%d.%m.%Y")}.xml'

            for key in data:
                if data[key][0] == '&':
                    data[key] = MappedColumn(data[key][1:])
            
            data.pop('interval')
            data.update({
                'pv': '',
                'nume_fur': model.nume_firma,
                'cif_fur': model.cif_firma
            })
            
            gen_xml(path, model.sheet, (int(l1), int(l2)), data, output_path)

        
        return render(request, 'mapping.html', {'form': map, 'json_file': as_json(path, model.sheet, model.rand_header)})

    map = FormMap(1)
    return render(request, 'mapping.html', {'form': map, 'json_file': as_json(path, model.sheet, model.rand_header)})

