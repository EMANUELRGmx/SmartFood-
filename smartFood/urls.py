
from django.urls import path 
from. import views


app_name = 'smartFood'



urlpatterns = [
    path('', views.index,name='index'),
    path('productosPorCategoria/<int:categoria_id>' , views.productosPorCategoria,name='productosPorCategoria'),
    path('productosPorNombre' , views.productosPorNombre,name='productosPorNombre'),
    path('productoDetalle/<int:producto_id>' ,views.productoDetalle,name='productoDetalle')

    
]
