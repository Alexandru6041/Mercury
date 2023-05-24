from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .forms import FormIesiri, FormIntrari, FormMap
from utils.converter_functions.functions import *
from .models import FileModel
from django.core.exceptions import PermissionDenied
from pathlib import Path
from string import Template

def iesiri(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    
    form = FormIesiri()
    errors = ''
    html_form = ''

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
    
    with open('templates/html/field.html', 'r') as f:
        field_template = Template(f.read())
    
    for field in form.fields:
        _type = 'text'
        value = None

        match(type(form.fields[field])):
            case forms.FileField:
                _type = 'file'
            
            case forms.IntegerField:
                _type = 'number'
                if request.method == 'POST':
                    value = form.fields[field].value
            
            case _:
                if request.method == 'POST':
                    value = form.fields[field].value
                _type = 'text'
                
        html_form += field_template.substitute({
            'type': _type,
            'placeholder': form.fields[field].label,
            'name': field,
            'value': '' if not value else value,
            'required': 'required' if(form.fields[field].required) else ''
        }) + '\n'
    
    with open('converter/templates/iesiri.html', 'r') as f:
        html_template = Template(f.read())
    
    with open('converter/templates/temp_iesiri.html', 'w') as f:
        f.write(html_template.substitute({'form': html_form}))
        
    return render(request, 'temp_iesiri.html', {'errors': errors})


def iesiri_mapping(request, file):
    if not request.user.is_authenticated or request.user.id != int(file.split('_')[0]):
        raise PermissionDenied
    
    path = f'input files/{file}.xlsx'
    model = FileModel.objects.get(nume=f'{file}.xlsx')

    if request.method == 'POST':
        map = FormMap(1, request.POST)

        if map.is_valid():
            try:
                output_path = proccess(map, model, request.user.id)
                return HttpResponseRedirect(f'/files/{output_path.split("/")[-1]}')
            
            except WrongTypeFieldException as e:
                map.add_error(e.field, 'Variabila invalida! Trebuie sa fie constanta sau tip Date')

        
        return render(request, 'mapping.html', {'form': map, 'json_file': as_json(path, model.sheet, model.rand_header)})

    map = FormMap(1)
    return render(request, 'mapping.html', {'form': map, 'json_file': as_json(path, model.sheet, model.rand_header)})

def intrari(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    
    form = FormIntrari()

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
        
    return render(request, 'intrari.html', {'form': form})

def intrari_mapping(request, file):
    if not request.user.is_authenticated or request.user.id != int(file.split('_')[0]):
        raise PermissionDenied
    
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
        
        return render(request, 'mapping.html', {'form': map, 'json_file': as_json(path, model.sheet, model.rand_header)})

    map = FormMap(0)
    j = as_json(path, model.sheet, model.rand_header)
    return render(request, 'mapping.html', {'form': map, 'json_file': j})


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