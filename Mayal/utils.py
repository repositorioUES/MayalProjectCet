import json
from Mayal.models import *

def cookieCart(request):

	#Create empty cart for now for non-logged in user
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}
		print('CART:', cart)

	items = []
	order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
	cartItems = order['get_cart_items']

	for i in cart:
		#We use try block to prevent items in cart that may have been removed from causing error
		try:	
			if(cart[i]['quantity']>0): #items with negative quantity = lot of freebies  
				cartItems += cart[i]['quantity']

				product = Producto.objects.get(id=i)
				total = (product.precio * cart[i]['quantity'])

				order['get_cart_total'] += total
				order['get_cart_items'] += cart[i]['quantity']

				item = {
				'id':product.id,
				'product':{'id':product.id,'nombreProd':product.nombreProd, 'precio':product.precio, 'imagen':product.imagen}, 'quantity':cart[i]['quantity'],'get_total':total,
				}

				items.append(item)
				if product.digital == False:
					order['shipping'] = True
		except:
			pass
			
	return {'cartItems':cartItems ,'order':order, 'items':items}

def cartData(request):
	if request.user.is_authenticated:
		user = request.user
		order, created = Order.objects.get_or_create(user=user, complete=False)
		
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']

	return {'cartItems':cartItems ,'order':order, 'items':items}

	
def guestOrder(request, data):
	first_name = data['form']['first_name']
	email = data['form']['email']

	cookieData = cookieCart(request)
	items = cookieData['items']

	user, created = User.objects.get_or_create(
			email=email,
			)
	user.first_name = first_name
	user.save()

	order = Order.objects.create(
		user=user,
		complete=False,
		)

	for item in items:
		product = Producto.objects.get(id=item['id'])
		orderItem = OrderItem.objects.create(
			product=product,
			order=order,
			quantity=(item['quantity'] if item['quantity']>0 else -1*item['quantity']), # negative quantity = freebies
		)
	return user, order

