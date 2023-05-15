from django import forms
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import FormIesiri, FormMap
from django.conf import settings
from functions.functions import *

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
            map = FormMap(1)

            return render(request, 'mapping.html', {'form': map, 'json_file': as_json(path, form.cleaned_data['sheet'], form.cleaned_data['header_row'])})
    
    
    return render(request, 'iesiri.html', {'form': form})
