import random
import re
from email import message
from itertools import product

from django.db.models import Q
from django.http import JsonResponse
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













def chatBot(request):
	return get_response(str(request.GET.get('message')), request)


def get_response(user_input, request):
	# Dividir el mensaje en palabras, qutarle los caracteres especiales y ponerlo todo a minúscula
	split_message = re.split(r'\s|[,;.:?¿!/-_]\s*', user_input.lower())
	response = check_all_messages(split_message)
	print(split_message)

	return render(request, 'ChatBot/chat.html', context={'response':response, 'message':user_input})
    
def message_probability(user_message, recognized_words, single_response=False, required_word=[]):
	message_certainty = 0
	has_required_words = True

	for word in user_message:
		if word in recognized_words:
			message_certainty += 1
	print("certeza " + str(message_certainty) + "  longitud " + str(len(recognized_words)))
	percentage = message_certainty
	for word in required_word:
		if word not in recognized_words:
			has_required_words = False
			break
	if has_required_words or single_response:
		return float(percentage * 100)
	else:
		return 0

# Se encarga de determinar la probabilidad de lo que está preguntando el usuario y devolver la respuesta
def check_all_messages(message):
	highest_prob = {}

	def response(bot_response, list_of_words, single_response=False):
		nonlocal highest_prob
		highest_prob[bot_response] = message_probability(message, list_of_words, single_response)

# 1 Saludos -------------------------------------------
	response(['Hola, como puedo ayudarle?','Que tal, tiene alguna duda?','Cómo está?, será un gusto resolver sus dudas'][random.randrange(3)], ['hola','buenas','saludos','buenos', 'buen','dias', 'dia','días','día','tal','terdes','noches','alguien', 'atiende','atendiendo','holi','hello'], single_response = True)
# 2 Despedidas ----------------------------------------
	response(['Siempre a la orden','Ha sido un gusto ayudarle','Estoy para servirle'][random.randrange(3)],['salu','gracias', 'agradezco', 'thanks', 'ty', 'amable','adios','adiós','bye','bai','bay','chao','chau','cuidese','cuídese','vemos'], single_response = True)
# 3 Formas de pago ------------------------------------
	response('Aceptamos tarjetas de credito, pagos con paypal, BTC y ETH',['agarran','pago','pagos','pagar','transferencia','transferencias','criptos', 'Kriptos', 'criptomonedas', 'Kriptomonedas','formas','aceptan','bitcoin','bitcoins','btc','ethereum','eterium','eth','paypal','electrónica','electronica','electrónicas','electronicas','tarjeta','tarjetas'], single_response=True)
# 4 Que ofrecemos -------------------------------------
	response('Ofrecemos Accesorios para dama y Productos de belleza, además puedes pedir accesorios personalizados',['venden', 'productos', 'venta', 'hallar', 'encontrar','ofrecen','ofrecer',], single_response=True)

# 5 Tipos de Accesorios -------------------------------
	response('Los Accesorios que ofrecemos: Anillos, Collares, Pulseras, Brazaletes, Vinchas, Peintas y Aretes, de colecciones especiales o puedes pedir un estilo personalizado',['tipo','tipos','clase','clases','accesorio','accesorios'], single_response=True)
# 6 Tipos de Productos de Belleza ---------------------
	response('Los Productos de belleza que ofrecemos: Cremas para Cara y Cuerpo, Cremas para peinar, Tratamientos para el cabello y Maquillaje, todos de la más alta calidad y de marcas recinocidas',['tipo','tipos','clase','clases','belleza','bellesa','beyesa','producto','productos'], single_response=True)

# 7 Donde hallar los Accesorios -----------------------
	response('Los puede encontrar en la categoría de ACCESORIOS',['venden','vende','tiene','tienen','anillos','anillo','collares','collar','pulsera','pulseras','arito','aritos','arete','aretes','vincha','vinchas','peineta','peinetas'], single_response=True)
# 8 Donde hallar los Productos de Belleza -------------
	response('Los puede encontrar en la categoría de PRODUCTOS DE BELLEZA',['venden','vende','tiene','tienen','producto','productos','crema','cremas','para','cara','facial','cuerpo','mano','manos','cabello','pelo','peinar','maquillaje','maquillajes','sombra','ojos','labial','labiales','pintalabio','pintalabios','labios','pinta','labios','tratamiento','tratamientos','acondicionador','acondicionadores'], single_response=True)

# 9 Como pedir Diseños personalizados -----------------
	response('Puedes ponerte en contacto con nosotros por medio de nuestras redes sociales, nos describes tu idea y puedes envirnos fotos de tu diseño o referencias que te gusten',['pedir','quiero','pido','elegir','solicitar','diseño','personalizado','personalizados','estilo','propio'],single_response=True)

# 10 Sobre May-Bot-------------------------------------
	response('Soy May-Bot, el chatbot de accesorios MAYAL', ['sos','eres','humana','humano','persona','bot','robot'], single_response=True)

# 11 Sobre Envios-------------------------------------
	response('Realizamos entregas a domicilio o también podemos acordar la entrega en otro lugar, como un centro comercial o en tu lugar de trabajo, sólo necesitamos la direccón', ['envio','envíos','domicilio','entregas','entrega','realizan','hacen','hace'], single_response=True)

	best_match = max(highest_prob, key=highest_prob.get)
	
	return unknown() if highest_prob[best_match] < 1 else best_match

# Si se pregunta algo fuera del alcance del Bot, se devuelve esta respuesta
def unknown():
	response = ['Lo siento, no entiendo, Soy un bot, puede reformular su pregunta por favor','No logro entender su pregunta, soy un bot','No estoy segura de lo que desea'][random.randrange(3)]
	return response

    
