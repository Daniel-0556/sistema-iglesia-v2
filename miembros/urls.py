from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_miembros, name='lista_miembros'),
    path('agregar/', views.agregar_miembro, name='agregar_miembro'),
    path('editar/<int:pk>/', views.editar_miembro, name='editar_miembro'),
    path('eliminar/<int:pk>/', views.eliminar_miembro, name='eliminar_miembro'),
    path('solicitar-eliminacion/<int:pk>/', views.solicitar_eliminacion, name='solicitar_eliminacion'),
    path('solicitudes/', views.gestionar_solicitudes, name='gestionar_solicitudes'),
    path('solicitudes/resolver/<int:pk>/', views.resolver_solicitud, name='resolver_solicitud'),
]