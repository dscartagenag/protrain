from .views import generar_qr
from django.urls import path

app_name = 'utilidades'

urlpatterns = [
    path('generar_qr/', generar_qr, name='index'),
]
