from django.urls import path

app_name = 'utilidades'

from views import index

urlpatterns = [
    path('generar_qr/', index, name='index'),    
]
