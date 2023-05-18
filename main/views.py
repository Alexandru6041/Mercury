import binascii
from tkinter import E
from types import NoneType
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from main.forms import RegisterUser
from main.forms import ChangePassword
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from sib_api_v3_sdk.rest import ApiException
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
# from django.contrib.auth.backends import

# Utilities
from utils.communication_utils.main_c import gService
from utils.hash_utils.hash_utils import SecureHasher

@login_required(login_url="/sign-in/", redirect_field_name="")
def index(request):
    username = None

    if request.user.is_authenticated:
        username = request.user.username
    else:
        return redirect("/sign-in/")

    return render(request, "index.html", {'display_name' : username})


@login_required(login_url="/sign-in/", redirect_field_name="")
def logout_user(request):
    logout(request)

    return redirect("/sign-in/")

def signin(request):
    if request.user.is_authenticated:
        return redirect("/")
    
    error = None
    
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)
        
        if user:
            login(request, user)
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
            email_user = request.POST["email"]
            username_user = request.POST["username"]
            
            # if(User.objects.filter(username = username_user).exists() == True):
            #     error_credentials = "Acest nume de utilizator este deja in uz"
            
            if(User.objects.filter(email = email_user).exists() == False): 
                creation_form.save()
                return redirect("/sign-in/")
            else:
                error_credentials = "Aceasta adresa de email este deja in uz"
        
        if(error_credentials == ''):
            error_dict = creation_form.errors
        
            for field in error_dict:
                error_credentials += error_dict[field]
                
    else:
        creation_form = RegisterUser()
        
        
    return render(request, 'signup.html', {'form': creation_form, 'error_credentials' : error_credentials})

def forgot_password(request):
    error = None

    if request.method == "POST":
        username = request.POST["user_detail"]
        pin = gService.generate_pin()
        pin = str(pin)
        enc_pin = SecureHasher.AESCipher.encrypt(plaintext=pin)
        enc_username = SecureHasher.AESCipher.encrypt(plaintext=username)
        def valid_email(email: str):
            try:
                validate_email(email)
            except Exception:
                return False
        
            return True
        print(username, valid_email(username))
        if(valid_email(username) == False):
            try:
                user = User.objects.get(username = username)
                user_email = user.email
                try:
                    gService.send_mail("Mercury", "requests.mercury@gmail.com", user_email, username, "Resetare Parola", "main/templates/email_template.html", pin, request=request)
                
                except ApiException:
                    return render(request, "502.html", status = 502)
                return redirect("/change_password?code={}&username={}".format(enc_pin, enc_username))
            
            except User.DoesNotExist:
                error = "Nu exista niciun utilizator cu acest nume"
                
        elif(error == None):
            user_email = username
            try:
                user = User.objects.get(email = user_email)
            
                username = user.username
                if(error == None):
                    try:
                        gService.send_mail("Mercury", "requests.mercury@gmail.com", user_email,
                                    username, "Resetare Parola", "main/templates/email_template.html", pin, request=request)
                    except ApiException:
                        return render(request, "502.html", status = 502)

                    return redirect("/change_password?code={}&username={}".format(enc_pin, enc_username))
            
            except User.DoesNotExist:
                error = "Nu exista niciun utilizator cu aceasta adresa de email"

    return render(request, "forgot_password.html", {'error' : error})


def code_check(request):
    error = None
    url = request.build_absolute_uri()
    if("&username=" not in url):
        return render(request, "403.html", status=403)
    else:
        url_argument_username = request.GET.get("username")
        if("=" in url_argument_username):
            return render(request, "403.html", status=403)
        try:
            dec_username  = SecureHasher.AESCipher.decrypt(ciphertext = url_argument_username)
        except binascii.Error:
            return render(request, "403.html", status=403)

    if("?code=" in url):

        url_argument = request.GET.get("code")
        
        if("=" in url_argument):
            return render(request, "403.html", status=403)
        try:
            dec_code = SecureHasher.AESCipher.decrypt(ciphertext= url_argument)
        except binascii.Error:
            return render(request, "403.html", status = 403)
        
    else:
        return render(request, "403.html", status = 403)
    try:
        user = User.objects.get(username = dec_username)
    except User.DoesNotExist:
        try:
            user = User.objects.get(email = dec_username)
        
        except User.DoesNotExist:
            return render(request, "403.html", status=403)

    
    change_form = ChangePassword(user)
    
    if request.method == "POST":
        change_form = ChangePassword(request.POST)
        user_code = request.POST["pin"]
        new_password = request.POST["new_password"]
        new_password_confirm = request.POST["new_password_confirm"]
        
        error_dict = change_form.errors

        for field in error_dict:
            error_credentials += error_dict[field]
            
        if(change_form.is_valid()):
            if(user_code == dec_code):
                if(new_password != new_password_confirm):
                    error = "Parolele nu coincid"
            else:
                error = "Codul introdus nu este corect. Verificati emailul"
        else:
            change_form = ChangePassword(user)

        
        print(error)
        
        if(error == None):
            try:
                new_password = make_password(new_password)
                user.password = new_password
                user.save()
                return redirect("/sign-in/")
            except User.DoesNotExist:
                return render(request, "403.html", status=403)

    return render(request, "change_password.html", {'error' : error, 'code' : url_argument, 'username' : url_argument_username, 'form' : change_form})
