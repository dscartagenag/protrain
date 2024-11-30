import qrcode
from PIL import Image
import os


def generar_codigo_qr(texto_convertir, nombre_guardar):
    """
    Genera un código QR a partir del texto proporcionado y lo guarda como una imagen.

    Args:
        texto_convertir (str): El texto que se convertirá en un código QR.
        nombre_guardar (str): El nombre del archivo en el que se guardará la imagen del código QR.

    Returns:
        bool: True si el código QR se genera y guarda correctamente, False en caso contrario.
    """
    try:
        # Crear un objeto QRCode
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        # Agregar datos al objeto QRCode
        qr.add_data(texto_convertir)
        qr.make(fit=True)

        # Crear la imagen del código QR
        img = qr.make_image(fill='black', back_color='white')

        # Guardar la imagen con el nombre especificado
        ruta_archivo = os.path.join('utilidades/img_qr', nombre_guardar)
        img.save(ruta_archivo)

        return True
    except Exception as e:
        # Si ocurre un error, imprimir el error y retornar False
        print(f"Error al generar el código QR: {e}")
        return False


if __name__ == "__main__":
    texto = "https://www.pamec.com.co"
    nombre_archivo = "ir_pamec.png"

    if generar_codigo_qr(texto, nombre_archivo):
        print("Código QR generado y guardado correctamente.")
    else:
        print("Hubo un error al generar el código QR.")

    



    