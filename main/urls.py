#imports
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

# app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path("sign-in/", views.signin, name = "sign-in"),
    path("sign-up/", views.signUp, name = "inregistrare"),
    path("forgot-password/", views.forgot_password, name = "parola_uitata"),
    path("change_password", views.code_check, name = "schimbare_parola"),
    path("logout/", views.logout_user, name = "logout"),
    path("my_account/", views.account_manage, name = "contulmeu"),
    path("about_us/", views.about_us, name = "despre_noi"),
    path("pricing/", views.pricing, name = "oferte"),
    path("check_user", views.check_user, name = "checkUser"),
    path("process_code/", views.process_code, name = "processcode"),
    path("delete_user/", views.delete_user, name = "deleteuser")
]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

handler404 = "main.views.handler404"
handler403 = "main.views.handler403"
handler502 = "main.views.handler502"
