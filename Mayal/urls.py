from django.urls import path
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from .views import *
from .ajax import *

urlpatterns = [
    # URLs para panel de ADMINISTRADOR ----------------------------------------------------------------------------------------------
    path('administrador', index, name="index"),

    path('administrador/listadoCategorias/', ListadosCatSubcat, name='listar_categorias'),
    path('administrador/crearCategoria', CrearCategoria.as_view(), name="crear_categoria"),
    path('administrador/modificarCategoria/<int:pk>', ModificarCategoria.as_view(), name='modificar_categoria'),
    path('administrador/borrarCategoria/<id>',borrarCategoria, name='borrar_categoria'),

    path('administrador/crearSubcategoria', CrearSubcategoria.as_view(), name="crear_subcategoria"),
    path('administrador/modificarSubcategoria/<int:pk>', ModificarSubcategoria.as_view(), name='modificar_subcategoria'),
    path('administrador/borrarSubcategoria/<id>/',borrarSubcategoria, name='borrar_subcategoria'),

    path('administrador/listadoProductos/', ListadoProducto.as_view(), name='listar_productos'),
    path('administrador/crearProducto', CrearProducto.as_view(), name="crear_producto"),
    path('administrador/modificarProducto/<int:pk>', ModificarProducto.as_view(), name='modificar_producto'),
    path('administrador/borrarProducto/<id>',borrarProducto, name='borrar_producto'),

    path('administrador/agregarImagenes/<int:pk>/',AgregarImagenes, name='agregar_imagenes'),
    path('administrador/guardarImagenes/<int:pk>/',GuardarImagenes, name='guardar_imagenes'),
    path('administrador/borrarImagen/<id>/',borrarImagen, name='borrar_imagen'),

    path('store/preguntasFrecuentes/', preguntas, name='faq'),
    path('store/terminosVS/', terminos, name='terminos'),

    # URLs para las funciones AJAX ----------------------------------------------------------------------------------------------
    path('ajax/load_Subcategorias/', load_Subcategorias, name='load_subcategorias'),
    path('ajax/load_Subcategorias_Edit/', load_Subcategorias_Edit, name='load_subcategorias_Edit'),
    path('ajax/simple_chatbot/', chatBot, name='chat'),
    
    # URLs para la TIENDA ----------------------------------------------------------------------------------------------
	path('', store, name="store"),
	path('cart/', cart, name="cart"),
	path('checkout/', checkout, name="checkout"),

	path('update_item/', updateItem, name="update_item"),
	path('process_order/', processOrder, name="process_order"),

    path('registro/', registro, name="registro"),
]

# Para mostrar las imagenes guardadas -----------------------------------------------------------------------------------------
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve,{
        'document_root': settings.MEDIA_ROOT,
    })
]