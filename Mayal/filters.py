from django.db.models import fields
import django_filters
from django_filters import CharFilter

from .models import *

class ProductoFilter(django_filters.FilterSet):
    nombreProd = CharFilter(field_name='nombreProd', lookup_expr='icontains', label='Producto')

    class Meta:
        model = Producto 
        fields = ['categoria', 'nombreProd']

