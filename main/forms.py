from django.contrib.auth import login, authenticate
from django.contrib.auth import models
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms

class Form2(UserCreationForm):
    pass
    
class RegisterUser(UserCreationForm):
    class Meta:
        model = models.User
        fields = ('email', 'username', 'password1', 'password2')

class ChangePassword(PasswordChangeForm):
    new_password = forms.CharField(max_length=256)
    new_password_confirm = forms.CharField(max_length=256)
