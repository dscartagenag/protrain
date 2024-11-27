import qrcode
from django.http import HttpResponse
from django.shortcuts import render
from io import BytesIO


def generar_qr(request):    
    data = request.GET.get('data', 'protrain la mejor opcion')

    qr = qrcode.QRCode(
        version=1,  # Controla el tamaño del código QR
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Genera una imagen del código QR
    img = qr.make_image(fill='black', back_color='white')

    # Convierte la imagen a un formato que pueda ser enviado en la respuesta HTTP
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_str = buffer.getvalue()

    # Retorna la imagen como una respuesta HTTP
    return HttpResponse(img_str, content_type='image/png')

    
    



    