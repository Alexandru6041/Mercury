from django import forms
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from .forms import FormIesiri, FormMap
from functions.functions import *

def iesiri(request):
    form = FormIesiri()
    if request.method == 'POST':
        if 'load_xl' in request.POST:
            # tip: [0, 1] -> 0 intrari, 1 iesiri
            form = FormIesiri(request.POST, request.FILES)

            if form.is_valid():
                path = save_uploaded_xlsx(request.FILES['file'], 0)
                map = FormMap(1)

                return render(request, 'mapping.html', {'form': map, 'json_file': as_json(path, form.cleaned_data['sheet'], form.cleaned_data['header_row'])})
        
        else:
            map = FormMap(1, request.POST)

            if map.is_valid():
                pass
        
    return render(request, 'iesiri.html', {'form': form})
