from django.shortcuts import render,get_object_or_404
from .models import Categoria,Producto
# Create your views here.


# VISTA PARA EL CATALOGO DE PRODUCTO 

def index(request):

    listaProductos = Producto.objects.all()
    listaCategorias = Categoria.objects.all()
    context = {
        'productos' : listaProductos,
        'categorias' : listaCategorias
    }
    
    return render(request,'index.html',context)

#vista para filtrado por categorias 

def productosPorCategoria (request,categoria_id):

    objCategoria = Categoria.objects.get(pk=categoria_id)
    listaProductos = objCategoria.producto_set.all()

    listaCategorias = Categoria.objects.all()

    context = {
        'categorias' : listaCategorias,
        'productos' : listaProductos
    }

    return render(request , 'index.html',context)


#vista para el filtrado por nombre

def productosPorNombre (request):
    nombre = request.POST['nombre']

    listaProductos = Producto.objects.filter(nombre__contains=nombre)
    listaCategorias = Categoria.objects.all()

    context = {
        'categorias': listaCategorias,
        'productos' : listaProductos
    }

    return render ( request, 'index.html' , context)


#detalle de producto 

def productoDetalle (request, producto_id):

    #objProducto = Producto.objects.get(pk=producto_id)
    objProducto = get_object_or_404(Producto,pk=producto_id)

    context = {
    'producto':objProducto,
    }

    return render (request,'producto.html' , context)
