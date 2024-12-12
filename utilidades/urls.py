from .views import generar_codigo_qr
from django.urls import path

app_name = 'utilidades'

urlpatterns = [
    path('generar_qr/', generar_codigo_qr, name='index'), # urls  utilidades: index
]
