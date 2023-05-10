#imports
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.landing, name = "landing"),
    path("sign-up/", views.signUp, name = "inregistrare"),
    path("forgot-password/", views.forgot_password, name = "parola_uitata"),
]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)