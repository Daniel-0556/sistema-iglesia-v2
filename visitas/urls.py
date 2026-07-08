from django.urls import path
from . import views

urlpatterns = [
    path('', views.portal_pastor, name='portal_pastor'),
    path('marcar/<int:persona_pk>/', views.marcar_visita, name='marcar_visita'),
    path('realizar/<int:visita_pk>/', views.realizar_visita, name='realizar_visita'),
    path('historial/', views.historial_visitas, name='historial_visitas'),
]