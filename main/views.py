from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login, authenticate
from main.forms import RegisterUser
from django.http import HttpResponse

# Third-party modules
import sqlite3
from utils.hash_utils.hash_utils import SecureHasher
from utils.communication_utils.main_c import gService
import datetime

# Variables
DATABASE_PATH = settings.DATABASES['default']['NAME']

# Create your views here.

def index(request):
    return HttpResponse('ceva')

def signin(request):
    if request.user.is_authenticated:
        return redirect("/")
        
    error = None
    
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)
        
        if user:
            login(username, password)
            return redirect("/")
        
        error = "Credentiale Incorecte"
    
    return render(request, 'signin.html', {'error_credentials': error})

def signUp(request):
    if request.user.is_authenticated:
        return redirect("/")
        
    error_credentials = ''
    
    if request.method == 'POST':
        creation_form = RegisterUser(request.POST)
        
        if creation_form.is_valid():
            creation_form.save()
            return redirect("/sign-in/")
        
        error_dict = creation_form.errors
        
        for field in error_dict:
            error_credentials += error_dict[field]
        
    else:
        creation_form = RegisterUser()
        
        
    return render(request, 'signup.html', {'form': creation_form, 'error_credentials' : error_credentials})

def forgot_password(request):
    pass


def code_check(request):
    pass
