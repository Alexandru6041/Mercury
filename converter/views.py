from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from utils.converter_functions.views_functions import generate_form_html
from .forms import FormIesiri, FormIntrari, FormMap
from utils.converter_functions.functions import *
from .models import FileModel
from django.core.exceptions import PermissionDenied
from pathlib import Path

def iesiri(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    
    form = FormIesiri()
    errors = ''

    if request.method == 'POST':
        # tip: [0, 1] -> 0 intrari, 1 iesiri
        form = FormIesiri(request.POST, request.FILES)

        if form.is_valid():
            path = save_uploaded_xlsx(request.FILES['file'], request.user.id)

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

            return HttpResponseRedirect(f'mapping/{file}')
        
        e = form.errors
        for key in e:
            errors += e[key] + '\n'
        
        errors.pop()
    
    with open('converter/templates/temp_iesiri.html', 'w') as f:
        f.write(generate_form_html(form.fields, 'converter/templates/iesiri.html', (request.POST if (request.method == 'POST') else {})))
        
    return render(request, 'temp_iesiri.html', {'errors': errors})


def iesiri_mapping(request, file):
    if not request.user.is_authenticated or request.user.id != int(file.split('_')[0]):
        raise PermissionDenied
    
    path = f'input files/{file}.xlsx'
    model = FileModel.objects.get(nume=f'{file}.xlsx')

    errors = ''

    if request.method == 'POST':
        map = FormMap(1, request.POST)

        if map.is_valid():
            try:
                output_path = proccess(map, model, request.user.id)
                return HttpResponseRedirect(f'/files/{output_path.split("/")[-1]}')
            
            except WrongTypeFieldException as e:
                map.add_error(e.field, 'Variabila invalida! Trebuie sa fie constanta sau tip Date')

        e = map.errors
        for key in e:
            errors += e[key] + '\n'
        
        errors.pop()

    else: map = FormMap(1)

    with open('converter/templates/temp_mapping.html', 'w') as f:
        f.write(generate_form_html(map.fields, 'converter/templates/mapping.html', request.POST if request.method == 'POST' else {}))

    return render(request, 'temp_mapping.html', {'model': model, 'form': map, 'json_file': as_json(path, model.sheet, model.rand_header), 'errors': errors})

def intrari(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    
    form = FormIntrari()
    errors = ''

    if request.method == 'POST':
        # tip: [0, 1] -> 0 intrari, 1 iesiri
        form = FormIntrari(request.POST, request.FILES)

        if form.is_valid():
            path = save_uploaded_xlsx(request.FILES['file'], request.user.id)

            model = FileModel.objects.create(
                nume=path.split('/')[-1],
                dimensiune=request.FILES['file'].size,
                sheet=form.cleaned_data['sheet'],
                rand_header=form.cleaned_data['header_row'],
                nume_firma=form.cleaned_data['client_nume'],
                cif_firma=form.cleaned_data['client_cif']
                )
            
            file = path.split("/")[-1].split(".")[:-1]
            file = file[0] + '.' + file[1]

            return HttpResponseRedirect(f'mapping/{file}')
        
        e = form.errors
        for key in e:
            errors += e[key] + '\n'
        
        errors.pop()
    
    with open('converter/templates/temp_intrari.html', 'w') as f:
        f.write(generate_form_html(form.fields, 'converter/templates/intrari.html', (request.POST if (request.method == 'POST') else {})))
        
    return render(request, 'temp_intrari.html', {'errors': errors})

def intrari_mapping(request, file):
    if not request.user.is_authenticated or request.user.id != int(file.split('_')[0]):
        raise PermissionDenied
    
    errors = ''
    path = f'input files/{file}.xlsx'
    model = FileModel.objects.get(nume=f'{file}.xlsx')

    if request.method == 'POST':
        map = FormMap(0, request.POST)

        if map.is_valid():
            try:
                output_path = proccess(map, model, request.user.id)
                return HttpResponseRedirect(f'/files/{output_path.split("/")[-1]}')
            
            except WrongTypeFieldException as e:
                map.add_error(e.field, 'Variabila invalida! Trebuie sa fie constanta sau tip Date')
        
        e = map.errors
        for key in e:
            errors += e[key] + '\n'
        
        errors.pop()

    else: map = FormMap(0)

    with open('converter/templates/temp_mapping.html', 'w') as f:
        f.write(generate_form_html(map.fields, 'converter/templates/mapping.html', request.POST if request.method == 'POST' else {}))

    return render(request, 'temp_mapping.html', {'model': model, 'form': map, 'json_file': as_json(path, model.sheet, model.rand_header), 'errors': errors})


def download_file(request, file):
    if not request.user.is_authenticated:
        raise PermissionDenied

    output_dir = f'output files/{request.user.id}'
    output_path = f'{output_dir}/{file}'

    if not Path(output_path).exists():
        raise Http404

    with open(output_path, 'rb') as f:
        data = f.read()
    
    response = HttpResponse(data, content_type='aplication/download-me-please')
    response['Content-Disposition'] = f'inline; filename={file}'
    
    return response