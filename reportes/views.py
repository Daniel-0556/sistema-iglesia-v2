from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncMonth
from accounts.views import rol_requerido
from miembros.models import Persona
from eventos.models import Evento, Asistencia


@login_required(login_url='login')
@rol_requerido('Supervisor', 'Secretaria', 'Pastor', 'Presidente')
def reportes(request):
    return render(request, 'reportes/reportes.html')


@login_required(login_url='login')
@rol_requerido('Supervisor', 'Secretaria', 'Pastor', 'Presidente')
def reporte_por_evento(request):
    iglesia = request.user.iglesia
    eventos = Evento.objects.filter(iglesia=iglesia).order_by('-fecha_evento')
    evento_seleccionado = None
    asistencias = []
    presentes = ausentes = justificados = total = 0

    evento_pk = request.GET.get('evento')
    if evento_pk:
        evento_seleccionado = get_object_or_404(Evento, pk=evento_pk, iglesia=iglesia)
        asistencias = Asistencia.objects.filter(
            evento=evento_seleccionado
        ).order_by('persona__nombre_persona')
        total = asistencias.count()
        presentes = asistencias.filter(estado='presente').count()
        ausentes = asistencias.filter(estado='ausente').count()
        justificados = asistencias.filter(estado='justificado').count()

    return render(request, 'reportes/reporte_por_evento.html', {
        'eventos': eventos,
        'evento_seleccionado': evento_seleccionado,
        'asistencias': asistencias,
        'total': total,
        'presentes': presentes,
        'ausentes': ausentes,
        'justificados': justificados,
    })


@login_required(login_url='login')
@rol_requerido('Supervisor', 'Secretaria', 'Pastor', 'Presidente')
def reporte_por_mes(request):
    iglesia = request.user.iglesia
    meses = Evento.objects.filter(
        iglesia=iglesia
    ).annotate(
        mes=TruncMonth('fecha_evento')
    ).values('mes').distinct().order_by('-mes')

    mes_seleccionado = request.GET.get('mes')
    datos_mes = []
    resumen = None

    if mes_seleccionado:
        try:
            from datetime import datetime
            fecha = datetime.strptime(mes_seleccionado, '%Y-%m')
            eventos_mes = Evento.objects.filter(
                iglesia=iglesia,
                fecha_evento__year=fecha.year,
                fecha_evento__month=fecha.month
            ).order_by('fecha_evento')

            total_presentes = total_ausentes = total_justificados = 0

            for evento in eventos_mes:
                asistencias = Asistencia.objects.filter(evento=evento)
                p = asistencias.filter(estado='presente').count()
                a = asistencias.filter(estado='ausente').count()
                j = asistencias.filter(estado='justificado').count()
                t = asistencias.count()
                porcentaje = round((p / t) * 100) if t > 0 else 0
                total_presentes += p
                total_ausentes += a
                total_justificados += j
                datos_mes.append({
                    'evento': evento,
                    'presentes': p,
                    'ausentes': a,
                    'justificados': j,
                    'total': t,
                    'porcentaje': porcentaje,
                })

            total_general = total_presentes + total_ausentes + total_justificados
            resumen = {
                'total_eventos': len(datos_mes),
                'total_presentes': total_presentes,
                'total_ausentes': total_ausentes,
                'total_justificados': total_justificados,
                'promedio': round((total_presentes / total_general) * 100) if total_general > 0 else 0,
            }
        except ValueError:
            pass

    return render(request, 'reportes/reporte_por_mes.html', {
        'meses': meses,
        'mes_seleccionado': mes_seleccionado,
        'datos_mes': datos_mes,
        'resumen': resumen,
    })


@login_required(login_url='login')
@rol_requerido('Supervisor', 'Secretaria', 'Pastor', 'Presidente')
def reporte_poca_asistencia(request):
    iglesia = request.user.iglesia
    total_eventos = Evento.objects.filter(iglesia=iglesia).count()
    miembros = Persona.objects.filter(iglesia=iglesia).order_by('nombre_persona')

    datos = []
    for miembro in miembros:
        if total_eventos == 0:
            porcentaje = 0
            presencias = 0
        else:
            presencias = Asistencia.objects.filter(
                persona=miembro,
                estado='presente'
            ).count()
            porcentaje = round((presencias / total_eventos) * 100)

        datos.append({
            'miembro': miembro,
            'porcentaje': porcentaje,
            'presencias': presencias,
            'total_eventos': total_eventos,
        })

    datos.sort(key=lambda x: x['porcentaje'])
    poca_asistencia = [d for d in datos if d['porcentaje'] < 30]
    buena_asistencia = [d for d in datos if d['porcentaje'] >= 30]

    return render(request, 'reportes/reporte_poca_asistencia.html', {
        'poca_asistencia': poca_asistencia,
        'buena_asistencia': buena_asistencia,
        'total_eventos': total_eventos,
    })