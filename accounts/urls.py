from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirigir_por_rol, name='inicio'),
    path('dashboard/supervisor/', views.dashboard_supervisor, name='dashboard_supervisor'),
    path('dashboard/secretaria/', views.dashboard_secretaria, name='dashboard_secretaria'),
    path('dashboard/digitador/', views.dashboard_digitador, name='dashboard_digitador'),
    path('dashboard/pastor/', views.dashboard_pastor, name='dashboard_pastor'),
    path('dashboard/presidente/', views.dashboard_presidente, name='dashboard_presidente'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/desactivar/<int:pk>/', views.desactivar_usuario, name='desactivar_usuario'),
    path('usuarios/activar/<int:pk>/', views.activar_usuario, name='activar_usuario'),
    path('usuarios/eliminar/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),
]