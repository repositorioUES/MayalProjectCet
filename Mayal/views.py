from email.mime import image
from django.shortcuts import render
from Mayal.models import *
from Mayal.forms import *
from django.views.generic.edit import View, UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView
from django.contrib import messages
from django.shortcuts import render, redirect, render,get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from django.views.generic import TemplateView
from django.urls import reverse
from django.views.generic import FormView
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

#@receiver(valid_ipn_received)
def paypal_payment_received(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the `business` field. (The user could tamper with
        # that fields on the payment form before it goes to PayPal)
        if ipn_obj.receiver_email != 'your-paypal-business-address@example.com':
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
            "return_url": self.request.build_absolute_uri(reverse('paypal_return')),
            "cancel_return": self.request.build_absolute_uri(reverse('paypal')),
            "lc": 'SV',
            "no_shipping": '0',
        }

class PaypalReturnView(TemplateView):
    template_name = 'paypal_success.html'

def paypal_return(request):
    context = {}
    return render(request, 'paypal/paypal_success.html', context)

class PaypalCancelView(TemplateView):
    template_name = 'paypal_cancel.html'


# Create your views here.
def paypal(request):
    #return HttpResponse("Index");
    # Create the instance.

    paypal_dict = {
        "business": "receiver_email@example.com",
        "amount": "40.00",
        "item_name": "name of the item",
        "invoice": "unique-invoice-id",
        "notify_url": request.build_absolute_uri(reverse('paypal')),
        "return": request.build_absolute_uri(reverse('paypal')),
        "cancel_return": request.build_absolute_uri(reverse('paypal')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "paypal/paypal_form.html", context)

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