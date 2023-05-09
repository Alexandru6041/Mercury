from django.shortcuts import render
from django.http import HttpResponse

# Third-party modules
import sqlite3
import os

# Create your views here.

def index(response):
	return HttpResponse("Mercury Project")


def landing(request):
    return render(request, 'home.html')

def signUp(request):
    return render(request, 'signup.html')

def forgot_password(request):
    return render(request, 'forgot_password.html')
