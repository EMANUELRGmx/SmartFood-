from django.contrib import admin

# Register your models here.

from .models import Categoria,Producto
# mostar en el administrador las tablas de Producto yCategoria 
admin.site.register(Categoria)

#mostar campos de la tabla producto con sus registros 
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display=('nombre' , 'precio' , 'categoria' , 'fecha_registro')
    list_editable=('precio',)

