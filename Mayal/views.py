from email.mime import image
from django.shortcuts import render
from Mayal.models import *
from Mayal.forms import *
from django.views.generic.edit import View, UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView
from django.contrib import messages
from django.shortcuts import render, redirect, render,get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse

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