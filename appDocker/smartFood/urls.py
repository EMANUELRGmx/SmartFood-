
from django.urls import path 
from. import views


app_name = 'smartFood'



urlpatterns = [
    path('', views.index,name='index'),
    path('productosPorCategoria/<int:categoria_id>' , views.productosPorCategoria,name='productosPorCategoria'),
    path('productosPorNombre' , views.productosPorNombre,name='productosPorNombre'),
    path('productoDetalle/<int:producto_id>' ,views.productoDetalle,name='productoDetalle'),
    path('carrito' , views.carrito,name='carrito'),
    path('agregarCarrito/<int:producto_id>' , views.agregarCarrito,name='agregarCarrito'),
    path('eliminarProductoCarrito/<int:producto_id>' ,views.eliminarProductoCarrito,name='eliminarProductoCarrito'),
    path('limpiarCarrito', views.limpiarCarrito,name='limpiarCarrito'),
    path('crearUsuario',views.crearUsuario,name='crearUsuario'),
    path('cuenta',views.cuentaUsuario,name='cuentaUsuario'),
    path('actualizarCliente', views.actualizarCliente,name='actualizarCliente'),
    path('login', views.loginUsuario,name='loginUsuario'),
    path('logout',views.logoutUsuario,name='logoutUsuario'),
    path('registrarPedido',views.registrarPedido,name='registrarPedido'),
    path('pruebapaypal',views.view_that_asks_for_money,name='pruebapaypal'),
    path('confirmarPedido',views.confirmarPedido,name='confirmarPedido'),
    path('gracias', views.gracias,name='gracias')
    

    
]