from django.shortcuts import render
from django.http import HttpResponse

# Third-party modules
import sqlite3
import os

# Create your views here.

def index(response):
	return HttpResponse("Mercury Project")