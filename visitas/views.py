from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from accounts.views import rol_requerido
from miembros.models import Persona
from eventos.models import Evento, Asistencia
from .models import VisitaPendiente
from .forms import VisitaRealizadaForm


@login_required(login_url='login')
@rol_requerido('Pastor')
def portal_pastor(request):
    iglesia = request.user.iglesia
    total_eventos = Evento.objects.filter(iglesia=iglesia).count()
    miembros = Persona.objects.filter(iglesia=iglesia)

    sin_visita = []
    visita_realizada = []
    buena_asistencia = []

    for miembro in miembros:
        if total_eventos == 0:
            porcentaje = 0
        else:
            presencias = Asistencia.objects.filter(
                persona=miembro,
                estado='presente'
            ).count()
            porcentaje = round((presencias / total_eventos) * 100)

        visita_pendiente = VisitaPendiente.objects.filter(
            persona=miembro,
            estado='pendiente'
        ).first()

        visita_hecha = VisitaPendiente.objects.filter(
            persona=miembro,
            estado='realizada'
        ).order_by('-fecha_realizada').first()

        datos = {
            'miembro': miembro,
            'porcentaje': porcentaje,
            'visita': visita_pendiente,
            'visita_hecha': visita_hecha,
        }

        if porcentaje >= 30:
            buena_asistencia.append(datos)
        elif visita_hecha and not visita_pendiente:
            visita_realizada.append(datos)
        else:
            sin_visita.append(datos)

    sin_visita.sort(key=lambda x: x['porcentaje'])
    visita_realizada.sort(key=lambda x: x['porcentaje'])

    return render(request, 'visitas/portal_pastor.html', {
        'sin_visita': sin_visita,
        'visita_realizada': visita_realizada,
        'buena_asistencia': buena_asistencia,
        'total_eventos': total_eventos,
    })


@login_required(login_url='login')
@rol_requerido('Pastor')
def marcar_visita(request, persona_pk):
    persona = get_object_or_404(Persona, pk=persona_pk, iglesia=request.user.iglesia)
    if VisitaPendiente.objects.filter(persona=persona, estado='pendiente').exists():
        messages.warning(request, f'Ya hay una visita pendiente para {persona.nombre_persona}.')
        return redirect('portal_pastor')
    VisitaPendiente.objects.create(
        persona=persona,
        creada_por=request.user,
        estado='pendiente'
    )
    messages.success(request, f'Visita pendiente marcada para {persona.nombre_persona}.')
    return redirect('portal_pastor')


@login_required(login_url='login')
@rol_requerido('Pastor')
def realizar_visita(request, visita_pk):
    visita = get_object_or_404(VisitaPendiente, pk=visita_pk, estado='pendiente')
    if request.method == 'POST':
        form = VisitaRealizadaForm(request.POST, instance=visita)
        if form.is_valid():
            visita = form.save(commit=False)
            visita.estado = 'realizada'
            visita.fecha_realizada = timezone.now()
            visita.save()
            messages.success(request, 'Visita marcada como realizada.')
            return redirect('portal_pastor')
    else:
        form = VisitaRealizadaForm(instance=visita)
    return render(request, 'visitas/realizar_visita.html', {
        'form': form,
        'visita': visita,
    })


@login_required(login_url='login')
@rol_requerido('Pastor', 'Supervisor')
def historial_visitas(request):
    visitas = VisitaPendiente.objects.filter(
        persona__iglesia=request.user.iglesia
    ).order_by('-fecha_creacion')
    pendientes = visitas.filter(estado='pendiente').count()
    realizadas = visitas.filter(estado='realizada').count()
    return render(request, 'visitas/historial_visitas.html', {
        'visitas': visitas,
        'pendientes': pendientes,
        'realizadas': realizadas,
    })