from http.client import CannotSendRequest
from django.shortcuts import render, redirect
from django.conf import settings

# Third-party modules
import sqlite3
from utils.hash_utils.hash_utils import SecureHasher
from utils.communication_utils.main_c import gService
import datetime

# Variables
DATABASE_PATH = settings.DATABASES['default']['NAME']

# Create your views here.

def index(request):
    
    token = None
    url_token = None
    
    url = request.build_absolute_uri()
    
    try:
        if("?token=" in url):
            sqliteConnection = sqlite3.connect(DATABASE_PATH)
            cursor = sqliteConnection.cursor()

            url_token = request.GET.get("token")
            
            token = url_token
            
            if("=" in token):
                return render(request, "403.html", status = 403)
            
            chiper = SecureHasher.AESCipher()
            dec_token = chiper.decrypt(url_token)

            valid = cursor.execute("SELECT * FROM main_user WHERE display_name = ?", [dec_token])
            sqliteConnection.commit()
            valid = cursor.fetchall()
            
            if(len(valid) == 0):
                return redirect("sign-in/")
        
        else:
            return redirect('sign-in/')
        
    except Exception as e:
        # return HttpResponse(status=403)
        return render(request, "403.html", status = 403)
    
    return render(request, 'index.html', {'token' : token, 'display_name' : dec_token})

def signin(request):
    global enc_token
    enc_token = None
    key = None
    error = None
    # global token
    
    if request.method == 'POST':
        # print(datetime.datetime.now())
        sqliteConnection = sqlite3.connect(DATABASE_PATH)
        cursor = sqliteConnection.cursor()
        form_username = request.POST["username"]
        form_password = request.POST["password"]
        
        print(form_username, form_password)
        
        cursor.execute("SELECT * FROM main_user WHERE email = ? OR display_name = ?", [form_username, form_username])
        sqliteConnection.commit()
        
        data = cursor.fetchall()
        if(len(data) == 0):
            error = "Nu exista niciun utilizator cu aceste credentiale"

        # try:
        if(error == None):
            for row in data:
                if(SecureHasher.verify_string(form_username, row[1]) or form_username == row[3]):
                    if(SecureHasher.verify_string(form_password, row[2])):
                        error = None
                        chiper = SecureHasher.AESCipher()
                        display_name = row[4]
                        enc_token = chiper.encrypt(display_name)

                        return redirect("/?token={}".format(enc_token))
                    
                    else:
                        error = "Credentiale Incorecte"
        
        sqliteConnection.close()
        
    return render(request, 'signin.html', {'error_credentials' : error})

def signUp(request):
    ok = None
    error = None
    
    if request.method == 'POST':
        sqliteConnection = sqlite3.connect(DATABASE_PATH)
        cursor = sqliteConnection.cursor()
        
        form_username = request.POST["username"]
        form_password = request.POST["password"]
        form_confirm_password = request.POST["confirm_password"]
        form_email = request.POST["email"]
        
        if(form_confirm_password != form_password):
            error = "Parolele nu coincid"
            
        elif(error is None):
            
            cursor.execute("SELECT * FROM main_user WHERE display_name = ?",[form_username])
            sqliteConnection.commit()
            data = cursor.fetchall()
            
            if(len(data) != 0):
                error = "Un cont cu acest nume de utilizator deja exista"
            
            cursor.execute("SELECT * FROM main_user WHERE email = ?", [form_email])
            sqliteConnection.commit()
            data = cursor.fetchall()
            if(len(data) != 0 and error == None):
                error = "Un cont cu aceast email deja exista"
            
            elif(error == None):
                hash_username = SecureHasher.hash_string(form_username)
                hash_password = SecureHasher.hash_string(form_password)
                
                cursor.execute("SELECT id FROM main_user")
                sqliteConnection.commit()
                data = cursor.fetchall()
                if len(data) == 0:
                    index = 1;
                else:
                    for row in data:
                        index = row[0] + 1
                
                cursor.execute("INSERT INTO main_user VALUES (?,?,?,?,?,?,?)", [index, hash_username, hash_password, form_email, form_username, 0, ""])
                sqliteConnection.commit()
                ok = "{} a fost inregistrat cu succes".format(form_username)
                
        sqliteConnection.close()
        
    return render(request, 'signup.html', {'error_credentials' : error, 'ok' : ok})

def forgot_password(request):
    error = None
    
    if request.method == "POST":
        sqliteConnection = sqlite3.connect(DATABASE_PATH)
        cursor = sqliteConnection.cursor()
        
        username = request.POST["user_detail"]
        
        cursor.execute("SELECT * FROM main_user WHERE email = ? or display_name = ?", [username, username])
        sqliteConnection.commit()
        
        data = cursor.fetchall()
        
        if(len(data) == 0):
            if("@" in username):
                error = "Nu exista niciun utilizator cu acest email"
            else:
                error = "Nu exista niciun utilizator cu acest nume de utilizator"
        elif(error == None):
            for row in data:
                email_to = row[3]
                username_to = row[1]
                
            pin = gService.generate_pin()
            chiper = SecureHasher.AESCipher()
            
            enc_token = chiper.encrypt(username)
            cursor.execute("UPDATE main_user SET user_token = ? WHERE email = ? or display_name = ?", [pin, username, username])
            sqliteConnection.commit()
            
            Context = """
            
                 <div class="img js-fullheight" style="background: #95b3bb; background-color: #171c24; backround-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='264' height='264' viewBox='0 0 800 800'%3E%3Cg fill='none' stroke='%231c212e' stroke-width='1'%3E%3Cpath d='M769 229L1037 260.9M927 880L731 737 520 660 309 538 40 599 295 764 126.5 879.5 40 599-197 493 102 382-31 229 126.5 79.5-69-63'/%3E%3Cpath d='M-31 229L237 261 390 382 603 493 308.5 537.5 101.5 381.5M370 905L295 764'/%3E%3Cpath d='M520 660L578 842 731 737 840 599 603 493 520 660 295 764 309 538 390 382 539 269 769 229 577.5 41.5 370 105 295 -36 126.5 79.5 237 261 102 382 40 599 -69 737 127 880'/%3E%3Cpath d='M520-140L578.5 42.5 731-63M603 493L539 269 237 261 370 105M902 382L539 269M390 382L102 382'/%3E%3Cpath d='M-222 42L126.5 79.5 370 105 539 269 577.5 41.5 927 80 769 229 902 382 603 493 731 737M295-36L577.5 41.5M578 842L295 764M40-201L127 80M102 382L-261 269'/%3E%3C/g%3E%3Cg fill='%232d4b4d'%3E%3Ccircle cx='769' cy='229' r='5'/%3E%3Ccircle cx='539' cy='269' r='5'/%3E%3Ccircle cx='603' cy='493' r='5'/%3E%3Ccircle cx='731' cy='737' r='5'/%3E%3Ccircle cx='520' cy='660' r='5'/%3E%3Ccircle cx='309' cy='538' r='5'/%3E%3Ccircle cx='295' cy='764' r='5'/%3E%3Ccircle cx='40' cy='599' r='5'/%3E%3Ccircle cx='102' cy='382' r='5'/%3E%3Ccircle cx='127' cy='80' r='5'/%3E%3Ccircle cx='370' cy='105' r='5'/%3E%3Ccircle cx='578' cy='42' r='5'/%3E%3Ccircle cx='237' cy='261' r='5'/%3E%3Ccircle cx='390' cy='382' r='5'/%3E%3C/g%3E%3C/svg%3E");">
                    <h1>Centrul de Ajutor Mercury</h1>
                    <h3>Codul dumneavoastra pentru resetarea parolei este {}</h3>""".format(pin)
            
            gService.send_mail("Mercury", "requests.mercury@gmail.com", email_to, username_to, "Cerere Schimbare Parola", Context)
            return redirect("/change_password?token={}".format(enc_token))

    else:
        pass
    
    return render(request, 'forgot_password.html', {'error' : error})

        


def code_check(request):
    ok = None
    error = None
    pin = None
    token = request.GET["token"]
    url = request.build_absolute_uri()
    
    try:
        sqliteConnection = sqlite3.connect(DATABASE_PATH)
        cursor = sqliteConnection.cursor()
        
        if("?token=" in url):
            token = request.GET["token"]
            
            if("=" in token):
                return render(request, "403.html", status=403)
            
            chiper = SecureHasher.AESCipher()
            dec_token = chiper.decrypt(token)

            valid = cursor.execute(
                "SELECT * FROM main_user WHERE email = ? or display_name = ?", [dec_token, dec_token])
            sqliteConnection.commit()
            valid = cursor.fetchall()
            
            if(len(valid) == 0):
                return render(request, "403.html", status=403)
            
            for row in valid:
                pin = row[6]

        else:
            return render(request, "403.html", status = 403)
        
        if request.method == "POST":
            
            form_pin = request.POST["pin"]
            form_new_password = request.POST["new_password"]
            form_new_password_confirm = request.POST["new_password_confirm"]
            
            if(form_pin != pin):
                error = "Codul de verificare este invalid"
                
            elif(error == None):
                if(form_new_password != form_new_password_confirm):
                    error = "Parolele nu coincid"
                    
                elif(error == None):
                    enc_new_password = SecureHasher.hash_string(form_new_password)
                    cursor.execute("UPDATE main_user SET password = ? WHERE user_token = ?", [enc_new_password, pin])
                    sqliteConnection.commit()
                    ok = "Parola a fost schimbata cu succes"
                    
    except Exception as e:
        print(e)
        return render(request, "403.html", status=403)

    return render(request, 'change_password.html', {'error': error, 'ok': ok, 'token' : token})

