from itertools import product
from django.http import JsonResponse

from django.db.models import Q
from django.shortcuts import render
from .models import *


def load_Subcategorias(request):
	catId = request.GET.get('catId')
	subcategorias = Subcategoria.objects.filter(categoria_id = catId)
	
	return render(request, 'Ajax/Subcat_dropdown.html', context={'subcategorias': subcategorias})

def load_Subcategorias_Edit(request):
	catId = request.GET.get('catId')
	prodId = request.GET.get('prodId')
	subcategorias = Subcategoria.objects.filter(categoria_id = catId)
	producto = Producto.objects.get(id = prodId)
	
	return render(request, 'Ajax/Subcat_Edit_dropdown.html', context={'subcategorias': subcategorias, 'producto': producto})