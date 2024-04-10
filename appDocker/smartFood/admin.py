from django.contrib import admin

# Register your models here.

from .models import Categoria,Producto,Pedido,PedidoDetalle
# mostar en el administrador las tablas de Producto yCategoria 
admin.site.register(Categoria)

#mostar campos de la tabla producto con sus registros 
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display=('nombre' , 'precio' , 'categoria' , 'fecha_registro')
    list_editable=('precio',)



@admin.register(Pedido)
class PedidoAdmin (admin.ModelAdmin):
    list_display=('cliente' , 'fecha_registro' , 'nro_pedido' , 'monto_total','estado')


@admin.register(PedidoDetalle)
class PedidoDetalleAdmin (admin.ModelAdmin):
    list_display=('pedido' , 'producto' , 'cantidad' , 'subtotal')
    


