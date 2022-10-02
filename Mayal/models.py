from unicodedata import category
from django.db import models

# Create your models here.

# ---CATEGORIA ------------------------------------------------------------------------------------------------------
class Categoria(models.Model):
    id = models.AutoField(primary_key = True)
    nombreCat = models.CharField(max_length = 100)

    def __str__(self):
        return self.nombreCat
#FIN CATEGORIA

# ---SUB-CATEGORIA --------------------------------------------------------------------------------------------------
class Subcategoria(models.Model):
    id = models.AutoField(primary_key = True)
    nombreSub = models.CharField(max_length = 100)
    categoria = models.ForeignKey('Categoria', on_delete = models.CASCADE)

    def __str__(self):
        return self.nombreSub
#FIN SUB-CATEGORIA

# --- PRODUCTO ---------------------------------------------------------------------------------------------------------
class Producto(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombreProd = models.CharField(max_length=250)
    coleccion = models.CharField(max_length=250, null=True, blank=True)
    material = models.CharField(max_length=250, null=True, blank=True)
    color = models.CharField(max_length=250, null=True, blank=True)
    precio = models.DecimalField(max_digits = 5, decimal_places= 2)
    existencias = models.IntegerField(null=True, blank=True)

    categoria = models.ForeignKey('Categoria', on_delete = models.SET_NULL, null=True)
    subCategoria = models.ForeignKey('Subcategoria', on_delete = models.SET_NULL, null=True)

    imagen = models.ImageField(upload_to='Galeria')

    def __str__(self):
        return self.nombreProd
#FIN PRODUCTO    

# -- IMAGEN -> PRODUCTO ----------------------------------------------------------------------------------------------------
class ImagenProducto(models.Model):
    id = models.AutoField(primary_key = True)
    imagen = models.ImageField(upload_to='Galeria')
    producto = models.ForeignKey('Producto', on_delete = models.CASCADE, related_name='imagenes')