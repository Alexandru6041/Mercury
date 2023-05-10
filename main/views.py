from django.shortcuts import render
from django.http import HttpResponse

# Third-party modules
import sqlite3
import os

# Create your views here.

def index(request):
	return render(request, 'index.html')

def signin(request):
    return render(request, 'signin.html')

def signUp(request):
    return render(request, 'signup.html')

def forgot_password(request):
    return render(request, 'forgot_password.html')
