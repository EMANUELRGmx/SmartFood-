from django.shortcuts import render,get_object_or_404,redirect
from .models import Categoria,Producto,Client,Pedido,PedidoDetalle
from .carrito import Cart
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .forms import ClienteForm
from django.core.mail import send_mail
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


@login_required(login_url='/login')
def confirmarPedido(request):
    context = {}
    if request.method == "POST":
        #actualizar datos de usuario
        actUsuario = User.objects.get(pk=request.user.id)
        actUsuario.first_name=request.POST['nombre']
        actUsuario.last_name=request.POST['apellidos']
        actUsuario.save()

        #registramos o actualizamos cliente 
        try:
            clientePedido = Client.objects.get(usuario=request.user)
            clientePedido.telefono = request.POST['telefono']
            clientePedido.direccion= request.POST['direccion']
            clientePedido.save()
        except:
            clientePedido=Client()
            clientePedido.usuario = actUsuario
            clientePedido.telefono = request.POST['telefono']
            clientePedido.direccion= request.POST['direccion']
            clientePedido.save()

        #registrar nuevo pedido 
        nroPedido = ''
        montoTotal = float (request.session.get('cartMontoTotal'))
        nuevoPedido = Pedido()
        nuevoPedido.cliente = clientePedido
        nuevoPedido.save()

        #registro de detalle pedido 
        carritoPedido = request.session.get('cart')
        
        for key,value in carritoPedido.items():
            productoPedido = Producto.objects.get(pk=value['producto_id'])
            detalle = PedidoDetalle()
            detalle.pedido = nuevoPedido
            detalle.producto = productoPedido
            detalle.cantidad = int(value['cantidad'])
            detalle.subtotal = float(value['subtotal'])
            detalle.save()



        #actualizar pedido
        nroPedido = 'PED' + nuevoPedido.fecha_registro.strftime('%Y') + str(nuevoPedido.id)
        nuevoPedido.nro_pedido = nroPedido
        nuevoPedido.monto_total=montoTotal
        nuevoPedido.save()

        #registrar variable de sesion para el pedido 
        request.session['pedidoId'] = nuevoPedido.id


        # boton de PAYPAL 
        paypal_dict = {
        "business": "sb-rzomt30237007@business.example.com",
        "amount": montoTotal,
        "item_name": "PEDIDO CODIGO : " +  nroPedido,
        "invoice":  nroPedido,
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri('/gracias'),
        "cancel_return": request.build_absolute_uri('/')
          # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    formPaypal = PayPalPaymentsForm(initial=paypal_dict)
        



    context = {
          'pedido' : nuevoPedido,
          'formPaypal': formPaypal
        }
    
    #limpiar carrito de compras 

    carrito = Cart(request)
    carrito.clear()
          
    return render (request,'compra.html',context)


#vista de GRACIAS
@login_required(login_url='/login')
def gracias(request):
    paypalId = request.GET.get('PayerID',None)
    context = {}
    if paypalId is not None:
        pedidoId = request.session.get('pedidoId')
        pedido = Pedido.objects.get(pk=pedidoId)
        pedido.estado = '1'
        pedido.save()

        send_mail(
            "GRACIAS POR TU COMPRA ",
            "Tu numero de pedido es: " + pedido.nro_pedido,
            "malayadelossigos@gmail.com",
            [request.user.email],
            fail_silently=False,
        )


        context = {
            'pedido':pedido
        }
    else:
        return redirect('/')
    
    return render (request, 'gracias.html',context)

#prueba de paypal 

from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
from django.shortcuts import render

def view_that_asks_for_money(request):

    # What you want the button to do.
    paypal_dict = {
        "business": "sb-rzomt30237007@business.example.com",
        "amount": "100.00",
        "item_name": "produdcto de prueba ",
        "invoice": "100-SMF100",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri('/'),
        "cancel_return": request.build_absolute_uri('/logout'),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payment.html", context)



