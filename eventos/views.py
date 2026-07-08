from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.views import rol_requerido
from miembros.models import Persona
from .models import Evento, Asistencia
from .forms import EventoForm


@login_required(login_url='login')
@rol_requerido('Supervisor', 'Secretaria', 'Digitador', 'Pastor', 'Presidente')
def lista_eventos(request):
    eventos = Evento.objects.filter(
        iglesia=request.user.iglesia
    ).order_by('-fecha_evento')
    return render(request, 'eventos/lista_eventos.html', {
        'eventos': eventos
    })


@login_required(login_url='login')
@rol_requerido('Supervisor', 'Secretaria')
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.iglesia = request.user.iglesia
            evento.save()
            messages.success(request, 'Evento creado exitosamente.')
            return redirect('lista_eventos')
    else:
        form = EventoForm()
    return render(request, 'eventos/form_evento.html', {
        'form': form,
        'titulo': 'Crear evento',
        'boton': 'Guardar evento'
    })


@login_required(login_url='login')
@rol_requerido('Supervisor', 'Secretaria')
def editar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk, iglesia=request.user.iglesia)
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento actualizado correctamente.')
            return redirect('lista_eventos')
    else:
        form = EventoForm(instance=evento)
    return render(request, 'eventos/form_evento.html', {
        'form': form,
        'titulo': 'Editar evento',
        'boton': 'Guardar cambios'
    })


@login_required(login_url='login')
@rol_requerido('Supervisor')
def eliminar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk, iglesia=request.user.iglesia)
    if request.method == 'POST':
        evento.delete()
        messages.success(request, 'Evento eliminado correctamente.')
        return redirect('lista_eventos')
    return render(request, 'eventos/confirmar_eliminar_evento.html', {
        'evento': evento
    })


@login_required(login_url='login')
@rol_requerido('Digitador', 'Supervisor', 'Secretaria')
def registrar_asistencia(request, evento_pk):
    evento = get_object_or_404(Evento, pk=evento_pk, iglesia=request.user.iglesia)
    miembros = Persona.objects.filter(iglesia=request.user.iglesia).order_by('nombre_persona')

    if request.method == 'POST':
        for miembro in miembros:
            estado = request.POST.get(f'estado_{miembro.pk}', 'ausente')
            Asistencia.objects.update_or_create(
                evento=evento,
                persona=miembro,
                defaults={'estado': estado}
            )
        messages.success(request, 'Asistencia registrada correctamente.')
        return redirect('lista_eventos')

    asistencias_existentes = {}
    for a in Asistencia.objects.filter(evento=evento):
        asistencias_existentes[a.persona.pk] = a.estado

    miembros_con_estado = []
    for miembro in miembros:
        miembros_con_estado.append({
            'miembro': miembro,
            'estado': asistencias_existentes.get(miembro.pk, 'ausente')
        })

    return render(request, 'eventos/registrar_asistencia.html', {
        'evento': evento,
        'miembros_con_estado': miembros_con_estado,
    })


@login_required(login_url='login')
@rol_requerido('Supervisor', 'Secretaria', 'Pastor', 'Presidente')
def ver_asistencia(request, evento_pk):
    evento = get_object_or_404(Evento, pk=evento_pk, iglesia=request.user.iglesia)
    asistencias = Asistencia.objects.filter(evento=evento).order_by('persona__nombre_persona')
    total = asistencias.count()
    presentes = asistencias.filter(estado='presente').count()
    ausentes = asistencias.filter(estado='ausente').count()
    justificados = asistencias.filter(estado='justificado').count()
    return render(request, 'eventos/ver_asistencia.html', {
        'evento': evento,
        'asistencias': asistencias,
        'total': total,
        'presentes': presentes,
        'ausentes': ausentes,
        'justificados': justificados,
    })