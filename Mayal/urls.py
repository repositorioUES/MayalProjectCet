from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from .views import *
from .ajax import *
from . import views
from getpaid.registry import registry

urlpatterns = [
    #Para los pagos con criptomoneda.
    path('criptos/',criptos,name="criptos"),
    #Fin de las vistas de pagos con BTC y ETH.

    #Para los pagos de PayPal.
    path('paypal/',paypal,name="paypal"),
    path('paypal-return/', views.PaypalReturnView.as_view(), name='paypal-return'),
    path('paypal-cancel/', views.PaypalCancelView.as_view(), name='paypal-cancel'),
    #Fin de las vistas de pagos con PayPal.

    #Para los pagos con PayU.
    path("order/<int:pk>/", OrderView.as_view(), name="order_detail"),
    path("payments/new/", views.new_payment, name="create-payment"),
    path(
        "success/<uuid:pk>/",
        views.success,
        name="payment-success",
    ),
    path(
        "failure/<uuid:pk>/",
        views.failure,
        name="payment-failure",
    ),
    path(
        "callback/<uuid:pk>/",
        views.callback,
        name="callback",
    ),
    path("", include(registry.urls)),
    #Fin de las vistas de pagos con tarjeta de crédito y débito.

    #Vistas del administrador.
    path('administrador/', index, name="index"),

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
    path('administrador/detalleProducto/<int:pk>/',detalleProducto, name='detalle_producto'),

    path('administrador/agregarImagenes/<int:pk>/',AgregarImagenes, name='agregar_imagenes'),
    path('administrador/guardarImagenes/<int:pk>/',GuardarImagenes, name='guardar_imagenes'),
    path('administrador/borrarImagen/<id>/',borrarImagen, name='borrar_imagen'),

    #url para mostrar mapa de seguimiento
    path('administrador/seguimiento/', seguimiento, name='seguimiento_producto'),  
    path('store/seguimientoEntrega/', tracking, name='seguimiento_entrega'),

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

    # URLs para LOGIN ----------------------------------------------------------------------------------------------
    path('registro/', registro, name="registro"),

    # URLs para el Usuario ----------------------------------------------------------------------------------------------
    path('administrador/listarUsuario', listarUsuario, name="listarUsuario"),
    path('administrador/editarUsuario/<id>/', editarUsuario, name="editarUsuario"),
    path('administrador/eliminarUsuario/<id>/', eliminarUsuario, name="eliminarUsuario"),
    path('administrador/listarOrdenes', listarOrdenes, name="listarOrdenes"),
    path('administrador/listarOrdenesProductos/<id>/', listarOrdenesProductos, name="listarOrdenesProductos"),
]

# Para mostrar las imagenes guardadas -----------------------------------------------------------------------------------------
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve,{
        'document_root': settings.MEDIA_ROOT,
    })
]