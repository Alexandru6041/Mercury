from django.urls import path
from . import views as v

urlpatterns = [
    path('iesiri/', v.iesiri, name='iesiri'),
    path('iesiri/mapping/<file>', v.iesiri_mapping),
    path('intrari/', v.intrari, name='intrari'),
    path('intrari/mapping/<file>', v.intrari_mapping)
]