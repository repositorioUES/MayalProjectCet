from django import forms
from django.contrib.admin import widgets
from django.forms import fields
from django.forms.forms import Form
from django.forms.models import ModelMultipleChoiceField
from django.forms.widgets import SelectMultiple
from Mayal.models import *
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CategoriaForm(forms.ModelForm):
	class Meta:
		model = Categoria
		fields = [
			 'nombreCat'
		]
		labels = {
			'nombreCat': 'Nombre de la Categoría'
		}

class SubcategoriaForm(forms.ModelForm):
	class Meta:
		model = Subcategoria
		fields = [
			 'nombreSub','categoria',
		]
		labels = {
			'nombreSub': 'Nombre de la Subcategoría',
            'categoria': 'Categoría a la que pertenece',
		}

class ProductoForm(forms.ModelForm):
	class Meta:
		model = Producto
		fields = [
			 'nombreProd','coleccion','material','color','precio','existencias','categoria','subCategoria', 'imagen',
		]
		labels = {
			'nombreProd': 'Nombre del Producto',
			'coleccion':'Colección',
			'material':'Material',
			'color':'Color',
			'precio':'Precio',
			'existencias':'Existencias',
            'categoria': 'Categoría',
			'subCategoria':'Subcategoria',
			'imagen': 'Imagen Principal',
		}

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2',]

        labels = {
            'username': 'Usuario'
        }


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', ]


class CustomUserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',]
        exclude = ['password']

        labels = {
            'username': 'Usuario'
        }
