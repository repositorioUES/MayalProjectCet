from email.mime import image
from multiprocessing import context

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView, View
from django.views.generic.list import ListView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from Mayal.forms import *
from Mayal.models import *

from django.contrib import messages
from django.shortcuts import render, redirect, render,get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder

# Create your views here.
def index(request):
    context = {}
    return render(request, 'administrador/base.html', context)


# CRUD ------ CATEGORIA------------------------------------------------------------------------------------

def ListadosCatSubcat(request):
    categorias = Categoria.objects.all().order_by('nombreCat')
    subcategorias = Subcategoria.objects.all().order_by('categoria')

    return render(request,'CRUDs/Categoria/lista.html', {'categorias' : categorias, 'subcategorias' : subcategorias})

class CrearCategoria(CreateView):
    model = Categoria
    template_name = 'CRUDs/Categoria/crear.html'
    form_class = CategoriaForm
    success_url = reverse_lazy('listar_categorias')

class ModificarCategoria(UpdateView):
    model = Categoria
    template_name = 'CRUDs/Categoria/crear.html'
    form_class = CategoriaForm
    success_url = reverse_lazy('listar_categorias')

def borrarCategoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)

    categoria.delete()
    messages.success(request, " Categoria eliminada correctamente")
    return redirect(to="listar_categorias")

# CRUD ------ SUBCATEGORIA----------------------------------------------------------------------------------

class CrearSubcategoria(CreateView):
    model = Subcategoria
    template_name = 'CRUDs/Subcategoria/crear.html'
    form_class = SubcategoriaForm
    success_url = reverse_lazy('listar_categorias')

class ModificarSubcategoria(UpdateView):
    model = Subcategoria
    template_name = 'CRUDs/Subcategoria/crear.html'
    form_class = SubcategoriaForm
    success_url = reverse_lazy('listar_categorias')

def borrarSubcategoria(request, id):
    subcategoria = get_object_or_404(Subcategoria, id=id)

    subcategoria.delete()
    messages.success(request, " Subcategoria eliminada correctamente")

    return redirect(to="listar_categorias")

# CRUD ------ PRODUCTO----------------------------------------------------------------------------------

class ListadoProducto(ListView):
    model = Producto
    template_name = 'CRUDs/Producto//lista.html'
    context_object_name = 'productos'

class CrearProducto(CreateView):
    model = Producto
    template_name = 'CRUDs/Producto/crear.html'
    form_class = ProductoForm
    success_url = reverse_lazy('listar_productos')

class ModificarProducto(UpdateView):
    model = Producto
    template_name = 'CRUDs/Producto/editar.html'
    form_class = ProductoForm
    success_url = reverse_lazy('listar_productos')

def borrarProducto(request, id):
    producto = get_object_or_404(Producto, id=id)

    producto.delete()
    messages.success(request, " Producto eliminado correctamente")

    return redirect(to="listar_productos")

# CONTROL DE LAS IMAGENES DE CADA PRODUCTO----------------------------------------------------------------------------------

def AgregarImagenes(request, pk):
    producto = get_object_or_404(Producto, id = pk)
    imagenesProducto = ImagenProducto.objects.filter(producto_id = pk)

    return render(request,'CRUDs/Producto/agregarImagenes.html', {'producto':producto,'imagenesProducto': imagenesProducto})

def GuardarImagenes(request, pk):
    producto = get_object_or_404(Producto, id = pk)

    if request.method == 'POST':
        data = request.POST
        imagenes = request.FILES.getlist('imagenes')

        for i in imagenes:
            imagenProducto = ImagenProducto.objects.create(
                producto_id = producto.id,
                imagen = i,
            )

        return HttpResponseRedirect('/administrador/agregarImagenes/' + str(producto.id) +'/')
            
    return render(request,'CRUDs/Producto/agregarImagenes.html', {'producto':producto})

def borrarImagen(request, id):
    imagenProducto = get_object_or_404(ImagenProducto, id=id)
    producto = get_object_or_404(Producto, id = imagenProducto.producto_id)

    imagenProducto.delete()
    messages.success(request, " Imagen eliminada correctamente")

    return HttpResponseRedirect('/administrador/agregarImagenes/' + str(producto.id) +'/')


# INICIO DE TIENDA----------------------------------------------------------------------------------

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Producto.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'tienda/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'tienda/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'tienda/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Producto.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)


# PREGUNTAS FRECUENTES ----------------------------------------------------------------------------------
def preguntas(request):
    context={}
    return render(request,'Otros/faq.html', context)

# TERMINOS DE VENTA Y SERVICIO ----------------------------------------------------------------------------------
def terminos(request):
    context={}
    return render(request,'Otros/terminos.html', context)

# LOGIN ----------------------------------------------------------------------------------

def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()

            #bitacora(request.user, "Registro de usuario: " + formulario.username)

            user = authenticate(username=formulario.cleaned_data["username"],
                                password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Registro exitoso")
            return redirect(to="index")
        data["form"] = formulario
    return render(request, 'registration/registro.html', data)