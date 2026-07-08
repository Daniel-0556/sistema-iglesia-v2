from django.urls import path
from . import views

urlpatterns = [
    path('', views.reportes, name='reportes'),
    path('por-evento/', views.reporte_por_evento, name='reporte_por_evento'),
    path('por-mes/', views.reporte_por_mes, name='reporte_por_mes'),
    path('poca-asistencia/', views.reporte_poca_asistencia, name='reporte_poca_asistencia'),
]