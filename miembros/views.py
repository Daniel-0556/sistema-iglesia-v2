from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.views import rol_requerido
from .models import Persona, SolicitudEliminacion
from .forms import PersonaForm, SolicitudEliminacionForm


@login_required(login_url='login')
@rol_requerido('Supervisor', 'Secretaria')
def lista_miembros(request):
    rol = request.user.rol.nombre_rol if request.user.rol else None
    if rol == 'Supervisor':
        miembros = Persona.objects.all().order_by('nombre_persona')
    else:
        miembros = Persona.objects.filter(
            iglesia=request.user.iglesia
        ).order_by('nombre_persona')
    return render(request, 'miembros/lista_miembros.html', {
        'miembros': miembros
    })


@login_required(login_url='login')
@rol_requerido('Supervisor', 'Secretaria')
def agregar_miembro(request):
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            miembro = form.save(commit=False)
            miembro.iglesia = request.user.iglesia
            miembro.save()
            messages.success(request, 'Miembro agregado exitosamente.')
            return redirect('lista_miembros')
    else:
        form = PersonaForm()
    return render(request, 'miembros/form_miembro.html', {
        'form': form,
        'titulo': 'Agregar miembro',
        'boton': 'Guardar miembro'
    })


@login_required(login_url='login')
@rol_requerido('Supervisor', 'Secretaria')
def editar_miembro(request, pk):
    miembro = get_object_or_404(Persona, pk=pk, iglesia=request.user.iglesia)
    if request.method == 'POST':
        form = PersonaForm(request.POST, instance=miembro)
        if form.is_valid():
            miembro = form.save(commit=False)
            miembro.iglesia = request.user.iglesia
            miembro.save()
            messages.success(request, 'Miembro actualizado exitosamente.')
            return redirect('lista_miembros')
    else:
        form = PersonaForm(instance=miembro)
    return render(request, 'miembros/form_miembro.html', {
        'form': form,
        'titulo': 'Editar miembro',
        'boton': 'Guardar cambios'
    })


@login_required(login_url='login')
@rol_requerido('Supervisor')
def eliminar_miembro(request, pk):
    miembro = get_object_or_404(Persona, pk=pk, iglesia=request.user.iglesia)
    if request.method == 'POST':
        nombre = miembro.nombre_persona
        miembro.delete()
        messages.success(request, f'Miembro {nombre} eliminado correctamente.')
        return redirect('lista_miembros')
    return render(request, 'miembros/confirmar_eliminar.html', {
        'miembro': miembro
    })


@login_required(login_url='login')
@rol_requerido('Secretaria')
def solicitar_eliminacion(request, pk):
    miembro = get_object_or_404(Persona, pk=pk)
    if SolicitudEliminacion.objects.filter(persona=miembro, estado='pendiente').exists():
        messages.warning(request,
            f'Ya existe una solicitud pendiente para eliminar a "{miembro.nombre_persona}".')
        return redirect('lista_miembros')
    if request.method == 'POST':
        form = SolicitudEliminacionForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.persona = miembro
            solicitud.solicitada_por = request.user
            solicitud.save()
            messages.success(request,
                f'Solicitud enviada al Supervisor para eliminar a "{miembro.nombre_persona}".')
            return redirect('lista_miembros')
    else:
        form = SolicitudEliminacionForm()
    return render(request, 'miembros/solicitar_eliminacion.html', {
        'form': form,
        'miembro': miembro
    })


@login_required(login_url='login')
@rol_requerido('Supervisor')
def gestionar_solicitudes(request):
    solicitudes = SolicitudEliminacion.objects.filter(
        estado='pendiente',
        persona__iglesia=request.user.iglesia
    ).order_by('-fecha_solicitud')
    return render(request, 'miembros/gestionar_solicitudes.html', {
        'solicitudes': solicitudes
    })


@login_required(login_url='login')
@rol_requerido('Supervisor')
def resolver_solicitud(request, pk):
    solicitud = get_object_or_404(SolicitudEliminacion, pk=pk)
    if request.method == 'POST':
        accion = request.POST.get('accion')
        if accion == 'aprobar':
            nombre = solicitud.persona.nombre_persona
            solicitud.persona.delete()
            solicitud.estado = 'aprobada'
            solicitud.save()
            messages.success(request, f'Miembro "{nombre}" eliminado correctamente.')
        elif accion == 'rechazar':
            solicitud.estado = 'rechazada'
            solicitud.save()
            messages.info(request, 'Solicitud rechazada.')
        return redirect('gestionar_solicitudes')
    return render(request, 'miembros/resolver_solicitud.html', {
        'solicitud': solicitud
    })