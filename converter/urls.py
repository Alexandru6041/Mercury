from django.urls import path
from . import views as v

urlpatterns = [
    path('iesiri', v.iesiri, name='iesiri'),
    path('iesiri/mapping/<file>', v.mapping,  name='mapping')
]