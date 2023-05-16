from django.contrib.auth import login, authenticate
from django.contrib.auth import models
from django.contrib.auth.forms import UserCreationForm
from django import forms

class Form2(UserCreationForm):
    pass
    
class RegisterUser(UserCreationForm):
    class Meta:
        model = models.User
        fields = ('email', 'username', 'password1', 'password2')
    
    