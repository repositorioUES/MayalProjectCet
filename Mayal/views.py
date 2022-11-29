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
from .utils import cookieCart, cartData, guestOrder
from django.http import JsonResponse
import json
import datetime
from django.db.models import Sum
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import render, redirect, render,get_object_or_404
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from django.views.generic import TemplateView, RedirectView, FormView, View, CreateView
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.views.generic.detail import DetailView
from getpaid.forms import PaymentMethodForm
from django import http
import swapper
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .filters import *

#Pagos con PayU.
class CreatePaymentView(CreateView):
	model = swapper.load_model("getpaid", "Payment")
	form_class = PaymentMethodForm

	def get(self, request, *args, **kwargs):
		"""
		This view operates only on POST requests from order view where
		you select payment method
		"""
		return http.HttpResponseNotAllowed(["POST"])

	def form_valid(self, form):
		payment = form.save()
		return payment.prepare_transaction(request=self.request, view=self)

	def form_invalid(self, form):
		return super().form_invalid(form)

new_payment = CreatePaymentView.as_view()

class FallbackView(RedirectView):
	"""
	This view (in form of either SuccessView or FailureView) can be used as
	general return view from paywall after completing/rejecting the payment.
	Final url is returned by
	:meth:`getpaid.models.AbstractPayment.get_return_redirect_url`
	which allows for customization.
	"""

	success = None
	permanent = False

	def get_redirect_url(self, *args, **kwargs):
		Payment = swapper.load_model("getpaid", "Payment")
		payment = get_object_or_404(Payment, pk=self.kwargs["pk"])

		return payment.get_return_redirect_url(
			request=self.request, success=self.success
		)


class SuccessView(FallbackView):
	success = True

success = SuccessView.as_view()


class FailureView(FallbackView):
	success = False

failure = FailureView.as_view()


class CallbackDetailView(View):
	"""
	This view can be used if paywall supports
	setting callback url with payment data.
	The flow is then passed to
	:meth:`getpaid.models.AbstractPayment.handle_paywall_callback`.
	"""

	def post(self, request, pk, *args, **kwargs):
		Payment = swapper.load_model("getpaid", "Payment")
		payment = get_object_or_404(Payment, pk=pk)
		return payment.handle_paywall_callback(request, *args, **kwargs)


callback = csrf_exempt(CallbackDetailView.as_view())

class OrderView(DetailView):
	model = Order

	def get_context_data(self, **kwargs):
		context = super(OrderView, self).get_context_data(**kwargs)
		context["payment_form"] = PaymentMethodForm(
			initial={"order":self.object, "currency": self.object.currency}
		)
		return context
#Fin de los pagos mediante PayU.
def criptos(request):
	return render(request, "criptos/payCripto.html")
#Para los pagos con criptomonedas.

#Fin de los pagos con criptomonedas.

#Pagos a través de Paypal.
#@receiver(valid_ipn_received)
def paypal_payment_received(sender, **kwargs):
	ipn_obj = sender
	if ipn_obj.payment_status == ST_PP_COMPLETED:
		# WARNING !
		# Check that the receiver email is the same we previously
		# set on the `business` field. (The user could tamper with
		# that fields on the payment form before it goes to PayPal)
		if ipn_obj.receiver_email != 'myeveryapp@gmail.com':
			# Not a valid payment
			return

		# ALSO: for the same reason, you need to check the amount
		# received, `custom` etc. are all what you expect or what
		# is allowed.
		try:
			my_pk = ipn_obj.invoice
			mytransaction = MyTransaction.objects.get(pk=my_pk)
			assert ipn_obj.mc_gross == mytransaction.amount and ipn_obj.mc_currency == 'USD'
		except Exception:
			logger.exception('Paypal ipn_obj data not valid!')
		else:
			mytransaction.paid = True
			mytransaction.save()
	else:
		logger.debug('Paypal payment status not completed: %s' % ipn_obj.payment_status)

class PaypalFormView(FormView):
	template_name = 'paypal_form.html'
	form_class = PayPalPaymentsForm

	def get_initial(self):
		return {
			"business": 'myeveryapps@gmail.com',
			"amount": 40,
			"currency_code": "USD",
			"item_name": 'Ratón',
			"invoice": 1234,
			"notify_url": self.request.build_absolute_uri(reverse('paypal')),
			"return_url": self.request.build_absolute_uri(reverse('paypal-return')),
			"cancel_return": self.request.build_absolute_uri(reverse('paypal-cancel')),
			"lc": 'SV',
			"no_shipping": '0',
		}

class PaypalReturnView(TemplateView):
	template_name = 'paypal_success.html'

class PaypalCancelView(TemplateView):
	template_name = 'paypal_cancel.html'


#Vista que muestra la pasarela de pago de PayPal.
def paypal(request):
	# Create the instance.

	paypal_dict = {
			"business": 'myeveryapps@gmail.com',
			"amount": 40,
			"currency_code": "USD",
			"item_name": 'Ratón',
			"invoice": 1234,
			"notify_url": request.build_absolute_uri(reverse('paypal')),
			"return_url": request.build_absolute_uri(reverse('paypal-return')),
			"cancel_return": request.build_absolute_uri(reverse('paypal-cancel')),
			"lc": 'SV',
			"no_shipping": '0',
	}

	form = PayPalPaymentsForm(initial=paypal_dict)
	context = {"form": form}
	return render(request, "paypal/paypal_form.html", context)

class SuperUserCheck(UserPassesTestMixin, View):
	def test_func(self):
		return self.request.user.is_superuser


# Create your views here.
@permission_required('is_superuser')
def index(request):
	context = {}
	return render(request, 'administrador/base.html', context)


# CRUD ------ CATEGORIA------------------------------------------------------------------------------------
@permission_required('is_superuser')
def ListadosCatSubcat(request):
	categorias = Categoria.objects.all().order_by('nombreCat')
	subcategorias = Subcategoria.objects.all().order_by('categoria')

	return render(request,'CRUDs/Categoria/lista.html', {'categorias' : categorias, 'subcategorias' : subcategorias})

class CrearCategoria(SuperUserCheck,CreateView):
	model = Categoria
	template_name = 'CRUDs/Categoria/crear.html'
	form_class = CategoriaForm
	success_url = reverse_lazy('listar_categorias')

class ModificarCategoria(SuperUserCheck,UpdateView):
	model = Categoria
	template_name = 'CRUDs/Categoria/crear.html'
	form_class = CategoriaForm
	success_url = reverse_lazy('listar_categorias')

@permission_required('is_superuser')
def borrarCategoria(request, id):
	categoria = get_object_or_404(Categoria, id=id)

	categoria.delete()
	messages.success(request, " Categoria eliminada correctamente")
	return redirect(to="listar_categorias")

# CRUD ------ SUBCATEGORIA----------------------------------------------------------------------------------

class CrearSubcategoria(SuperUserCheck,CreateView):
	model = Subcategoria
	template_name = 'CRUDs/Subcategoria/crear.html'
	form_class = SubcategoriaForm
	success_url = reverse_lazy('listar_categorias')

class ModificarSubcategoria(SuperUserCheck,UpdateView):
	model = Subcategoria
	template_name = 'CRUDs/Subcategoria/crear.html'
	form_class = SubcategoriaForm
	success_url = reverse_lazy('listar_categorias')

@permission_required('is_superuser')
def borrarSubcategoria(request, id):
	subcategoria = get_object_or_404(Subcategoria, id=id)

	subcategoria.delete()
	messages.success(request, " Subcategoria eliminada correctamente")

	return redirect(to="listar_categorias")

# CRUD ------ PRODUCTO----------------------------------------------------------------------------------


class ListadoProducto(SuperUserCheck,ListView):
	model = Producto
	template_name = 'CRUDs/Producto//lista.html'
	context_object_name = 'productos'


class CrearProducto(SuperUserCheck,CreateView):
	model = Producto
	template_name = 'CRUDs/Producto/crear.html'
	form_class = ProductoForm
	success_url = reverse_lazy('listar_productos')

class ModificarProducto(SuperUserCheck,UpdateView):
	model = Producto
	template_name = 'CRUDs/Producto/editar.html'
	form_class = ProductoForm
	success_url = reverse_lazy('listar_productos')
	
@permission_required('is_superuser')
def borrarProducto(request, id):
	producto = get_object_or_404(Producto, id=id)

	producto.delete()
	messages.success(request, " Producto eliminado correctamente")

	return redirect(to="listar_productos")

# CONTROL DE LAS IMAGENES DE CADA PRODUCTO----------------------------------------------------------------------------------
@permission_required('is_superuser')
def AgregarImagenes(request, pk):
	producto = get_object_or_404(Producto, id = pk)
	imagenesProducto = ImagenProducto.objects.filter(producto_id = pk)

	return render(request,'CRUDs/Producto/agregarImagenes.html', {'producto':producto,'imagenesProducto': imagenesProducto})
@permission_required('is_superuser')
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

@permission_required('is_superuser')
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
	filter = ProductoFilter(request.GET, queryset=products)
	products = filter.qs

	context = {'products':products, 'cartItems':cartItems, 'filter' : filter,}
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

	user = request.user
	product = Producto.objects.get(id=productId)
	order, created = Order.objects.get_or_create(user=user, complete=False)

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
		user = request.user
		order, created = Order.objects.get_or_create(user=user, complete=False)
	else:
		user, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		user=user,
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
			return redirect(to="two_factor:setup")
		data["form"] = formulario
	return render(request, 'registration/registro.html', data)


# USUARIOS ----------------------------------------------------------------------------------
@permission_required('is_superuser')
def listarUsuario(request):
	usuarios = User.objects.all()
	data = {
		'usuarios': usuarios,
	}

	return render(request, 'CRUDs/usuario/listarUsuario.html', data)

@permission_required('is_superuser')
def listarOrdenes(request):
	ordenes = Order.objects.all()
	data = {
		'ordenes': ordenes,
	}

	return render(request, 'administrador/listaOrdenes.html', data)

@permission_required('is_superuser')
def listarOrdenesProductos(request,id):
	ordenes = Order.objects.get(id=id)
	ordenesItems = ordenes.orderitem_set.all()
	productos = ordenes.orderitem_set.all().count()

	data = {
		'ordenes': ordenes,
		'ordenesItems': ordenesItems,
		'productos': productos,

	}

	return render(request, 'administrador/listarOrdenesProductos.html', data)

@permission_required('is_superuser')
def editarUsuario(request, id):
	usuario = get_object_or_404(User, id=id)
	data = {
		'form': CustomUserEditForm(instance=usuario)
	}

	if request.method == 'POST':
		formulario = CustomUserEditForm(data=request.POST, instance=usuario)
		if formulario.is_valid():
			formulario.save()

			messages.success(request, " Usuario actualizado correctamente")
			return redirect(to="listarUsuario")
		data['form'] = formulario
	return render(request, 'CRUDs/usuario/editarUsuario.html', data)


@permission_required('is_superuser')
def eliminarUsuario(request, id):
	usuario = get_object_or_404(User, id=id)

	usuario.delete()
	messages.success(request, " Usuario eliminado correctamente")
	return redirect(to="listarUsuario")

## importacion de librerias para modulo de seguimiento
import folium
import phonenumbers
import os

def seguimiento(request):
	from phonenumbers import geocoder
	number = "+505 77253153"

	llave = '30e3f905fb6b4f5dbf4bf759a091fe8c'
	
	sanNumber = phonenumbers.parse(number)
	tulocacion = geocoder.description_for_number(sanNumber,"en")
	print(tulocacion)

	##obteniendo el nombre del proveedor del servicio
	from phonenumbers import carrier
	provedorServicio =phonenumbers.parse(number)
	print(carrier.name_for_number(provedorServicio, "en"))
	
	##generando el mapa 
	from opencage.geocoder import OpenCageGeocode
	geocoder = OpenCageGeocode(llave)
	query = str(tulocacion)
	resultado = geocoder.geocode(query)
	lat = resultado[0]['geometry']['lat']
	lng = resultado[0]['geometry']['lng']
	mimapa = folium.Map(location=[lat, lng], zoom_start = 9)
	folium.Marker([lat, lng],popup=tulocacion).add_to((mimapa))
	## Guardando nuestro mapa en un archivo html en donde se ubica este archivo
	mimapa.save("miMapa.html")
	html = open(os.path.dirname(os.path.realpath(__file__))  + '\miMapa.html', "r")   
	
	return HttpResponse(html.read())


# SEGUIMIENTO DE ENTREGA ( simulado XD ) ------------------------------------------------------------------------
def tracking(request):
	context={}
	return render(request,'Otros/seguimiento.html', context)

# DETALLE DE LA INFO E IMAGENES DE CADA PRODUCTO----------------------------------------------------------------------------------
@permission_required('is_superuser')
def detalleProducto(request, pk):
	producto = get_object_or_404(Producto, id = pk)
	imagenesProducto = ImagenProducto.objects.filter(producto_id = pk)

	return render(request,'CRUDs/Producto/detalle.html', {'producto':producto,'imagenesProducto': imagenesProducto})

