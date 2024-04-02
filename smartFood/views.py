from django.shortcuts import render,get_object_or_404,redirect
from .models import Categoria,Producto,Client
from .carrito import Cart
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .forms import ClienteForm
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

# vistas para el carrito de compras 

def carrito (request):

    return render(request,'carrito.html')

#agregar a carrito 

def agregarCarrito (request , producto_id):
    if request.method == 'POST':
        cantidad = int(request.POST['cantidad'])
    else:
        cantidad = 1

    objProducto =  Producto.objects.get(pk=producto_id)
    carritoProducto = Cart(request)
    carritoProducto.add(objProducto,cantidad)

    if request.method == 'GET' :
        return redirect('/')
   

    return render (request , 'carrito.html')

# eliminar producto de carrito 
def eliminarProductoCarrito(request,producto_id):
    objProducto = Producto.objects.get(pk=producto_id)
    carritoProducto = Cart(request)
    carritoProducto.delete(objProducto)

    return render(request, 'carrito.html')


#limpiar carrito 

def limpiarCarrito (request):
    carritoProducto = Cart(request)
    carritoProducto.clear()

    return render(request,'carrito.html')


# VISTAS PARA CLIENTES Y USUARIOS 

def crearUsuario(request):

    if request.method == 'POST':
        dataUsuario = request.POST['nuevoUsuario']
        dataPassword = request.POST['nuevoPassword']

        nuevoUsuario = User.objects.create_user(username=dataUsuario,password=dataPassword)
        if nuevoUsuario is not None:
            login(request,nuevoUsuario)
            return redirect('/cuenta')

    return render(request, 'login.html')

def loginUsuario(request):
    paginaDestino = request.GET.get('next',None)
    context = {
        'destino':paginaDestino
    }

    if request.method == 'POST':
        dataUsuario = request.POST['usuario']
        dataPassword = request.POST['password']
        dataDestino = request.POST['destino']
      

        usuarioAuth = authenticate(request,username=dataUsuario,password=dataPassword)
        if usuarioAuth is not None:
            login(request,usuarioAuth)

            if dataDestino != 'None':
                return redirect(dataDestino)

           
            
            return redirect('/cuenta')
        else:
            context = {
                'mensajeError':'Datos incorrectos'
            }

    return render(request,'login.html',context)

def logoutUsuario(request):
    logout(request)
    return render(request,'login.html')




def cuentaUsuario(request):
    try:

        clienteEditar = Client.objects.get(usuario = request.user)

        dataCliente = {
            'nombre':request.user.first_name,
            'apellidos' :request.user.last_name,
            'email' :request.user.email,
            'telefono':clienteEditar.telefono,
            'matricula' :clienteEditar.matricula,
            'direccion':clienteEditar.direccion,
            'sexo' :clienteEditar.sexo,
            'fecha_nacimiento' :clienteEditar.fecha_nacimiento
        }   
    
    except: 
        dataCliente = {
            'nombre':request.user.first_name,
            'apellidos' :request.user.last_name,
            'email' :request.user.email
         }


    frmCliente = ClienteForm(dataCliente)
    context = {
        'frmCliente' : frmCliente
    }
    return render(request,'cuenta.html',context)


def actualizarCliente(request):
    mensaje = ""

    if request.method == "POST":
        frmCliente = ClienteForm(request.POST)
        if frmCliente.is_valid():
            dataCliente = frmCliente.cleaned_data

            #actualizar usuario 
            actUsuario = User.objects.get(pk=request.user.id)
            actUsuario.first_name = dataCliente["nombre"]
            actUsuario.last_name = dataCliente["apellidos"]
            actUsuario.email = dataCliente["email"]
            actUsuario.save()

            #registrar cliente
            nuevoCliente = Client()
            nuevoCliente.usuario = actUsuario
            nuevoCliente.matricula = dataCliente["matricula"]
            nuevoCliente.direccion = dataCliente["direccion"]
            nuevoCliente.telefono = dataCliente["telefono"]
           
            nuevoCliente.sexo = dataCliente["sexo"]
            nuevoCliente.fecha_nacimiento = dataCliente["fecha_nacimiento"]
            nuevoCliente.save()
            mensaje = "DATOS ACTUALIZADOS"

    context ={
        'mensaje' :mensaje,
        'frmCliente' :frmCliente
    }


    return render (request,'cuenta.html',context)



#VISTAS PARA PROCESO DE COMPRA

@login_required(login_url='/login')
def registrarPedido (request):
    try:

        clienteEditar = Client.objects.get(usuario = request.user)

        dataCliente = {
            'nombre':request.user.first_name,
            'apellidos' :request.user.last_name,
            'email' :request.user.email,
            'telefono':clienteEditar.telefono,
            'matricula' :clienteEditar.matricula,
            'direccion':clienteEditar.direccion,
            'sexo' :clienteEditar.sexo,
            'fecha_nacimiento' :clienteEditar.fecha_nacimiento
        }   
    
    except: 
        dataCliente = {
            'nombre':request.user.first_name,
            'apellidos' :request.user.last_name,
            'email' :request.user.email
         }
    frmCliente = ClienteForm(dataCliente)
    context = {
        'frmCliente' : frmCliente
    }


    return render ( request,'pedido.html',context)
