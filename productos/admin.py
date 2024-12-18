from django.contrib import admin

from .models import Lote, Receta, Producto, Ingrediente, RecetaIngrediente, ProductoImagen

admin.site.register(Lote)
admin.site.register(Receta)
admin.site.register(Producto)
admin.site.register(Ingrediente)
admin.site.register(RecetaIngrediente)
admin.site.register(ProductoImagen)