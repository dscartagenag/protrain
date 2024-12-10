from django.db import models

from ..usuarios.models import Operador


# Estado de control de calidad
ESTATUS_CALIDAD = (
    ("Paso", "Paso"),
    ("Pendiente", "Pendiente"),
    ("Fallo", "Fallo"),
)

# Estado del lote producido
ESTADO_LOTE = (
    ("Vendido", "Vendido"),
    ("Retirado", "Retirado"),
    ("Activo", "Activo"),
)


class Lote(models.Model):
    """
    Representa un lote de producción de productos.

    Atributos:
        numero (int): Número identificador del lote.
        fecha_vencimiento (date): Fecha de vencimiento del lote.
        fecha_fabricacion (date): Fecha de fabricación del lote.
        cantidad_producida (int): Cantidad de unidades producidas en el lote.
        estatus_calidad (str): Estado del control de calidad (Paso, Pendiente, Fallo).
        fecha_registro_sistema (date): Fecha en la que el lote fue registrado en el sistema.
        observaciones (str, opcional): Comentarios o detalles adicionales sobre el lote.
        estado_lote (str): Estado actual del lote (Vendido, Retirado, Activo).
        operador (ForeignKey): Relación con el operador responsable del lote.
    """
    numero = models.IntegerField()
    fecha_vencimiento = models.DateField()
    fecha_fabricacion = models.DateField()
    cantidad_producida = models.IntegerField()
    estatus_calidad = models.CharField(max_length=50, choices=ESTATUS_CALIDAD)
    fecha_registro_sistema = models.DateField(auto_now_add=True)
    observaciones = models.CharField(max_length=255, null=True, blank=True)
    estado_lote = models.CharField(max_length=50, choices=ESTADO_LOTE)
    operador = models.ForeignKey('Operador', on_delete=models.RESTRICT)

    def __str__(self):
        """
        Representación en cadena del objeto Lote.

        Returns:
            str: Identificador del lote y su estado.
        """
        return f"Lote {self.numero} - {self.estado_lote}"

    @classmethod
    def obtener_lotes_activos(cls):
        """
        Obtiene todos los lotes activos.

        Returns:
            QuerySet: Lotes con estado "Activo".
        """
        return cls.objects.filter(estado_lote="Activo")


class Producto(models.Model):
    """
    Representa un producto fabricado en un lote.

    Atributos:
        nombre (str): Nombre del producto.
        lote (ForeignKey): Relación con el lote asociado.
        receta (ForeignKey): Relación con la receta utilizada para fabricar el producto.
        sabor (str): Sabor o característica del producto.
        cantidad (int): Tamaño o peso del producto en gramos.
        precio (int): Precio del producto en la moneda local.
    """
    nombre = models.CharField(max_length=50)
    lote = models.ForeignKey(
        Lote, on_delete=models.RESTRICT, verbose_name="Lote asociado")
    receta = models.ForeignKey(
        'Receta', on_delete=models.SET_NULL, null=True, verbose_name="Receta utilizada")
    sabor = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    precio = models.SmallIntegerField()

    def __str__(self):
        """
        Representación en cadena del objeto Producto.

        Returns:
            str: Nombre del producto, su sabor y el lote asociado.
        """
        return f"{self.nombre} ({self.sabor}) - Lote: {self.lote.numero}"


class Ingrediente(models.Model):
    """
    Representa un ingrediente utilizado en las recetas.

    Atributos:
        nombre (str): Nombre del ingrediente.
        unidad_medida (str): Unidad de medida para el ingrediente (ej. gramos, litros).
    """
    nombre = models.CharField(max_length=50, null=False, blank=False)
    unidad_medida = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        """
        Representación en cadena del objeto Ingrediente.

        Returns:
            str: Nombre del ingrediente y su unidad de medida.
        """
        return f"{self.nombre} ({self.unidad_medida})"


class Receta(models.Model):
    """
    Representa una receta para la fabricación de un producto.

    Atributos:
        nombre (str): Nombre de la receta.
        descripcion (str): Descripción de la receta.
    """
    nombre = models.CharField(max_length=50, null=False, blank=False)
    descripcion = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        """
        Representación en cadena del objeto Receta.

        Returns:
            str: Nombre de la receta.
        """
        return self.nombre


class RecetaIngrediente(models.Model):
    """
    Relación entre recetas e ingredientes, con las cantidades requeridas.

    Atributos:
        receta (ForeignKey): Relación con la receta asociada.
        ingrediente (ForeignKey): Relación con el ingrediente asociado.
        cantidad (int): Cantidad requerida del ingrediente en la receta.
    """
    receta = models.ForeignKey('Receta', on_delete=models.RESTRICT)
    ingrediente = models.ForeignKey('Ingrediente', on_delete=models.RESTRICT)
    cantidad = models.SmallIntegerField()

    class Meta:
        # Evita duplicados en una receta
        unique_together = ('receta', 'ingrediente')

    def __str__(self):
        """
        Representación en cadena del objeto RecetaIngrediente.

        Returns:
            str: Cantidad del ingrediente requerido para una receta específica.
        """
        return f"{self.cantidad} de {self.ingrediente.nombre} en {self.receta.nombre}"


class ProductoImagen(models.Model):
    """
    Representa las imágenes asociadas a un producto.

    Atributos:
        producto (ForeignKey): Relación con el producto asociado.
        image (ImageField): Imagen del producto.
        principal (bool): Indicador de si es la imagen principal.
        description (str): Descripción de la imagen.
    """
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name="images", verbose_name="Producto")
    image = models.ImageField(
        upload_to="img/producto_imagenes/", verbose_name="Imagen del producto")
    principal = models.BooleanField(
        default=False, verbose_name="Imagen principal")
    description = models.CharField(
        max_length=255, blank=True, verbose_name="Descripción de la imagen")

    class Meta:
        # Garantiza una sola imagen principal
        unique_together = ('producto', 'principal')

    def __str__(self):
        """
        Representación en cadena del objeto ProductoImagen.

        Returns:
            str: Detalles de la imagen del producto, indicando si es principal o secundaria.
        """
        return f"Imagen de {self.producto.nombre} ({'Principal' if self.principal else 'Secundaria'})"

    @classmethod
    def obtener_imagen_principal(cls, producto_id):
        """
        Obtiene la imagen principal de un producto.

        Args:
            producto_id (int): ID del producto.

        Returns:
            ProductoImagen: Objeto de la imagen principal, o None si no existe.
        """
        return cls.objects.filter(producto_id=producto_id, principal=True).first()
