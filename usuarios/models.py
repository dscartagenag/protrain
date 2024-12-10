from django.db import models
from django.contrib.auth.models import User


# Opciones de estado para la sede
OPCIONES_SEDES = [
    ('Active', 'Active'),
    ('Inactive', 'Inactive'),
    ('Under Maintenance', 'Under Maintenance'),
]


class Sede(models.Model):
    """
    Representa una sede donde se realizan operaciones o almacenamiento.

    Atributos:
        nombre (str): Nombre único que identifica la sede.
        direccion (str): Dirección física de la sede.
        ciudad (str): Ciudad en la que se encuentra ubicada la sede.
        capacidad (int): Capacidad máxima de almacenamiento u operaciones de la sede (en número de productos).
        estado (str): Estado actual de la sede (Activo, Inactivo o En Mantenimiento).
    """
    nombre = models.CharField(
        max_length=100, unique=True, verbose_name="Nombre de la Sede")
    direccion = models.TextField(verbose_name="Dirección")
    ciudad = models.CharField(max_length=50, verbose_name="Ciudad")
    capacidad = models.IntegerField(
        blank=True, null=True, verbose_name="Capacidad Máxima")
    estado = models.CharField(
        max_length=20,
        choices=OPCIONES_SEDES,
        default='Active',
        verbose_name="Estado de la Sede"
    )

    def __str__(self):
        return f"{self.nombre} - {self.estado}"


class Operador(models.Model):
    """
    Representa a un operador asignado a una sede específica.

    Atributos:
        usuario (OneToOneField): Relación uno a uno con el modelo de usuario (Django User).
        cargo (str): Cargo o rol del operador dentro de la sede.
        sede (ForeignKey): Relación con la sede donde trabaja el operador.
        telefono (str): Número de teléfono del operador.
    """
    usuario = models.OneToOneField(
        User, on_delete=models.RESTRICT, verbose_name="Usuario")
    cargo = models.CharField(max_length=50, null=True,
                             blank=True, verbose_name="Cargo")
    sede = models.ForeignKey(
        Sede, on_delete=models.RESTRICT, verbose_name="Sede Asignada")
    telefono = models.CharField(
        max_length=11, verbose_name="Teléfono de Contacto")

    def __str__(self):
        return f"{self.usuario.username} - {self.cargo if self.cargo else 'Sin Cargo'} en {self.sede.nombre}"
