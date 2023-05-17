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
    path("logout/", views.logout_user, name = "logout")
]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)