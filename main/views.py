from atexit import register
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from main.forms import RegisterUser
from main.forms import ChangePassword
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from sib_api_v3_sdk.rest import ApiException
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

# Utilities
from utils.communication_utils.main_c import gService
from utils.costum_backend.main import MyBackend, AESCipher
from Mercury.settings import EMAIL_ACCOUNT, EMAIL_NAME, DEFAULT_EMAIL_PATH


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
        user = MyBackend.authenticate(request, username = username, password = password)
        if user:
            login(request, user)
            return redirect("/")
        else:
            error = "Credentiale Incorecte"
    
    return render(request, 'signin.html', {'error_credentials': error})

def signUp(request):
    if request.user.is_authenticated:
        return redirect("/")
        
    error_credentials = ''
    creation_form = RegisterUser()
    
    if request.method == 'POST':
        creation_form = RegisterUser(request.POST)
        email_user = request.POST["email"]
        username_user = request.POST["username"]
        
        if(User.objects.filter(email = email_user).exists() == True): 
            error_credentials = "Aceasta adresa de email este deja in uz"
        
        if(error_credentials == ''):
            error_dict = creation_form.errors
        
            for field in error_dict:
                error_credentials += error_dict[field]
                
        if creation_form.is_valid():
            creation_form.save()
            return redirect("/sign-in/")
        
        else:
            creation_form = RegisterUser()
        
        
    return render(request, 'signup.html', {'form': creation_form, 'error_credentials' : error_credentials})

def forgot_password(request):
    error = None
    if request.method == "POST":
        username = request.POST["user_detail"]
        pin = gService.generate_pin()
        pin = str(pin)
        enc_pin = AESCipher.encrypt(plaintext=pin)
        enc_username = AESCipher.encrypt(plaintext=username)
        
        
        def valid_email(email: str):
            try:
                validate_email(email)
            except Exception:
                return False
        
            return True
        if(valid_email(username) == False):
            try:
                user = User.objects.get(username = username)
                user_email = user.email
                
                gService.send_message(user_email, EMAIL_ACCOUNT, "Echipa Mercury: Resetare Parola", EMAIL_NAME, username, pin, DEFAULT_EMAIL_PATH, request)
                
                return redirect("/change_password?code={}&username={}".format(enc_pin, enc_username))
            
            except User.DoesNotExist:
                error = "Nu exista niciun utilizator cu acest nume"
                
        elif(error == None):
            user_email = username
            try:
                user = User.objects.get(email = user_email)
            
                username = user.username
                if(error == None):

                    gService.send_message(user_email, EMAIL_ACCOUNT, "Echipa Mercury: Resetare Parola", EMAIL_NAME, username, pin, DEFAULT_EMAIL_PATH, request)

                    return redirect("/change_password?code={}&username={}".format(enc_pin, enc_username))
            
            except User.DoesNotExist:
                error = "Nu exista niciun utilizator cu aceasta adresa de email"

    return render(request, "forgot_password.html", {'error' : error})


def code_check(request):
    error = ''
    url = request.build_absolute_uri()
    
    if("&username=" not in url):
        return render(request, "403.html", status=403)
    else:
        url_argument_username = request.GET.get("username")
        if("=" in url_argument_username):
            return render(request, "403.html", status=403)
        
        
        try:
            dec_username  = AESCipher.decrypt(ciphertext = url_argument_username)
        except:
            return render(request, "403.html", status=403)

    if("?code=" in url):

        url_argument = request.GET.get("code")
        
        if("=" in url_argument):
            return render(request, "403.html", status=403)
        try:
            dec_code = AESCipher.decrypt(ciphertext= url_argument)
        except:
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
        
        
        if(user_code == dec_code):
            if(new_password != new_password_confirm):
                error = 'Parolele nu coincid'
                
            if(error == '' and user.password == new_password):
                error = 'Parola noua nu poate fi la fel cu cea veche'
            
            error_dict = MyBackend.validate_password(new_password, user)

            if(error == '' and len(error_dict) != 0):
                for i in range(len(error_dict)):
                    error += error_dict[i]
            
        else:
            error = 'Codul introdus nu este corect. Verificati emailul'
        

        
        if(error == ''):
            try:
                new_password = make_password(password = new_password, salt = None, hasher='myhasher')
                user.password = new_password
                user.save()
                return redirect("/sign-in/")
            except User.DoesNotExist:
                return render(request, "403.html", status=403)
    else:
        change_form = ChangePassword(user)

    return render(request, "change_password.html", {'error' : error, 'code' : url_argument, 'username' : url_argument_username, 'form' : change_form})


@login_required(login_url="/sign-in/", redirect_field_name="")
def account_manage(request):
    user = request.user
    user_email = user.email
    display_name = user.username
    ok = None
    error = ''
    
    if request.method == "POST":
        new_username = request.POST["username"]
        new_password = request.POST["password"]
        new_email = request.POST["email"]
        
        if(new_username != ''):
            if (User.objects.filter(username=new_username).exists() == True):
                error = 'Acest nume de utilizator exista deja'
        
        if(error == '' and new_email != '' and User.objects.filter(email=new_email).exists() == True):
            error = 'Aceasta adresa de email este deja in uz'
        
        if(error == '' and new_password != ''):
            
             error_dict = MyBackend.validate_password(new_password, user)    
             if(len(error_dict) != 0):
                for i in range(len(error_dict)):
                    error += error_dict[i]
        
        if(error == ''):
            if(new_username != ''):
                user.username = new_username
            
            if(new_email != ''):
                user.email = new_email
            
            if(new_password != ''):
                new_password_copy = new_password
                new_password = make_password(password=new_password, salt=None, hasher='myhasher')
                user.password = new_password
            
            user.save()
            user = MyBackend.authenticate(request, username = user.username, password = new_password_copy)
            login(request, user)
            
            ok = "Datele au fost actualizate cu succes"
    
    return render(request, "manage_account.html", {'error' : error, 'ok' : ok, 'user_email' : user.email, 'display_name' : user.username})


@login_required(login_url="/sign-in/", redirect_field_name="")
def check_user(request):
    error = None
    url = request.build_absolute_uri()
    
    if("?code=" in url):
        enc_code = request.GET["code"]
        
        if("=" in enc_code):
            return render(request, "403.html", status = 403)
    else:
        return render(request, "403.html", status=403)
        
    dec_code = AESCipher.decrypt(enc_code)
    
    if request.method == 'POST':
        code = request.POST["code"]
        if(dec_code == code):
            return redirect("/my_account/")
        else:
            error = "Codul introdus este incorect. Verifcati mailul"
    
    return render(request, "check_code.html", {'error' : error, 'pin' : enc_code})



@login_required(login_url="/sign-in/", redirect_field_name="")
def process_code(request):
    try:
        user = request.user
        user_email = user.email
        username = user.username
        pin = gService.generate_pin()
        pin = str(pin)
        
        gService.send_message(user_email, EMAIL_ACCOUNT, "Echipa Mercury: Verificare Identitate", EMAIL_NAME, username, pin, DEFAULT_EMAIL_PATH, request)

        enc_code = AESCipher.encrypt(pin)
        return redirect("/check_user?code={}".format(enc_code))
    except ApiException:
        return render(request, "502.html", status=502)

def delete_user(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        return redirect("/sign-in/")

def about_us(request):
    return render(request, "aboutus.html")

def pricing(request):
    return render(request, "pricing.html")


# Costum Http Errors Handler
def handler404(request, exception):
    return render(request, "404.html", status = 404)

def handler403(request, exception):
    return render(request, "403.html", status = 403)

def handler502(request, execption):
    return render(request, "502.html", status = 502)