from unicodedata import category
from django.db import models
from django.contrib.auth.models import User

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
    digital = models.BooleanField(default=False,null=True, blank=True)
    imagen = models.ImageField(upload_to='Galeria')

    def __str__(self):
        return self.nombreProd
#FIN PRODUCTO    

# -- IMAGEN -> PRODUCTO ----------------------------------------------------------------------------------------------------
class ImagenProducto(models.Model):
    id = models.AutoField(primary_key = True)
    imagen = models.ImageField(upload_to='Galeria')
    producto = models.ForeignKey('Producto', on_delete = models.CASCADE, related_name='imagenes')


class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class Order(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
		
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

class OrderItem(models.Model):
	product = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.precio * self.quantity
		return total

class ShippingAddress(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address