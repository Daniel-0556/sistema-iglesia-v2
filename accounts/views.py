from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from functools import wraps
from .models import Usuario, Rol
from miembros.models import Persona, SolicitudEliminacion
from eventos.models import Evento
from visitas.models import VisitaPendiente


# --- Decorador personalizado por rol ---
def rol_requerido(*roles_permitidos):
    def decorador(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            rol_usuario = request.user.rol.nombre_rol if request.user.rol else None
            if request.user.is_superuser or rol_usuario in roles_permitidos:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
        return wrapper
    return decorador


# --- Redirección automática según rol ---
@login_required(login_url='login')
def redirigir_por_rol(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    rol = request.user.rol.nombre_rol if request.user.rol else None
    rutas = {
        'Supervisor':  'dashboard_supervisor',
        'Secretaria':  'dashboard_secretaria',
        'Digitador':   'dashboard_digitador',
        'Pastor':      'dashboard_pastor',
        'Presidente':  'dashboard_presidente',
    }
    destino = rutas.get(rol)
    if destino:
        return redirect(destino)
    return HttpResponseForbidden("Tu usuario no tiene un rol asignado.")


# --- Dashboards ---
@login_required(login_url='login')
@rol_requerido('Supervisor')
def dashboard_supervisor(request):
    iglesia = request.user.iglesia
    total_miembros = Persona.objects.filter(iglesia=iglesia).count()
    total_usuarios = Usuario.objects.filter(iglesia=iglesia).count()
    total_eventos = Evento.objects.filter(iglesia=iglesia).count()
    solicitudes_pendientes = SolicitudEliminacion.objects.filter(
        estado='pendiente',
        persona__iglesia=iglesia
    ).count()
    return render(request, 'accounts/dashboard_supervisor.html', {
        'total_miembros': total_miembros,
        'total_usuarios': total_usuarios,
        'total_eventos': total_eventos,
        'solicitudes_pendientes': solicitudes_pendientes,
    })


@login_required(login_url='login')
@rol_requerido('Secretaria')
def dashboard_secretaria(request):
    iglesia = request.user.iglesia
    total_miembros = Persona.objects.filter(iglesia=iglesia).count()
    total_eventos = Evento.objects.filter(iglesia=iglesia).count()
    return render(request, 'accounts/dashboard_secretaria.html', {
        'total_miembros': total_miembros,
        'total_eventos': total_eventos,
    })


@login_required(login_url='login')
@rol_requerido('Digitador')
def dashboard_digitador(request):
    iglesia = request.user.iglesia
    total_miembros = Persona.objects.filter(iglesia=iglesia).count()
    total_eventos = Evento.objects.filter(iglesia=iglesia).count()
    return render(request, 'accounts/dashboard_digitador.html', {
        'total_miembros': total_miembros,
        'total_eventos': total_eventos,
    })


@login_required(login_url='login')
@rol_requerido('Pastor')
def dashboard_pastor(request):
    iglesia = request.user.iglesia
    total_miembros = Persona.objects.filter(iglesia=iglesia).count()
    total_eventos = Evento.objects.filter(iglesia=iglesia).count()
    visitas_pendientes = VisitaPendiente.objects.filter(
        persona__iglesia=iglesia,
        estado='pendiente'
    ).count()
    return render(request, 'accounts/dashboard_pastor.html', {
        'total_miembros': total_miembros,
        'total_eventos': total_eventos,
        'visitas_pendientes': visitas_pendientes,
    })


@login_required(login_url='login')
@rol_requerido('Presidente')
def dashboard_presidente(request):
    from eventos.models import Asistencia
    iglesia = request.user.iglesia
    total_miembros = Persona.objects.filter(iglesia=iglesia).count()
    total_eventos = Evento.objects.filter(iglesia=iglesia).count()
    total_asistencias = Asistencia.objects.filter(
        evento__iglesia=iglesia, estado='presente'
    ).count()
    total_registros = Asistencia.objects.filter(evento__iglesia=iglesia).count()
    promedio = round((total_asistencias / total_registros) * 100) if total_registros > 0 else 0
    ultimos_eventos = Evento.objects.filter(iglesia=iglesia).order_by('-fecha_evento')[:5]
    ultimos_eventos_data = []
    for evento in ultimos_eventos:
        presentes = Asistencia.objects.filter(evento=evento, estado='presente').count()
        total = Asistencia.objects.filter(evento=evento).count()
        porcentaje = round((presentes / total) * 100) if total > 0 else 0
        ultimos_eventos_data.append({
            'evento': evento,
            'presentes': presentes,
            'total': total,
            'porcentaje': porcentaje,
        })
    return render(request, 'accounts/dashboard_presidente.html', {
        'total_miembros': total_miembros,
        'total_eventos': total_eventos,
        'promedio': promedio,
        'ultimos_eventos': ultimos_eventos_data,
    })


# --- Gestión de Usuarios ---
@login_required(login_url='login')
@rol_requerido('Supervisor')
def lista_usuarios(request):
    usuarios = Usuario.objects.filter(
        iglesia=request.user.iglesia,
        is_superuser=False
    ).order_by('username')
    return render(request, 'accounts/lista_usuarios.html', {
        'usuarios': usuarios
    })


@login_required(login_url='login')
@rol_requerido('Supervisor')
def crear_usuario(request):
    from .forms import UsuarioCrearForm
    if request.method == 'POST':
        form = UsuarioCrearForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.iglesia = request.user.iglesia
            usuario.save()
            messages.success(request, f'Usuario "{usuario.username}" creado exitosamente.')
            return redirect('lista_usuarios')
    else:
        form = UsuarioCrearForm()
    return render(request, 'accounts/form_usuario.html', {
        'form': form,
        'titulo': 'Crear usuario',
        'boton': 'Crear usuario'
    })


@login_required(login_url='login')
@rol_requerido('Supervisor')
def editar_usuario(request, pk):
    from .forms import UsuarioEditarForm
    usuario = get_object_or_404(Usuario, pk=pk, iglesia=request.user.iglesia)
    if request.method == 'POST':
        form = UsuarioEditarForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuario "{usuario.username}" actualizado.')
            return redirect('lista_usuarios')
    else:
        form = UsuarioEditarForm(instance=usuario)
    return render(request, 'accounts/form_usuario.html', {
        'form': form,
        'titulo': 'Editar usuario',
        'boton': 'Guardar cambios'
    })


@login_required(login_url='login')
@rol_requerido('Supervisor')
def desactivar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk, iglesia=request.user.iglesia)
    if request.method == 'POST':
        usuario.is_active = False
        usuario.save()
        messages.warning(request, f'Usuario "{usuario.username}" desactivado.')
        return redirect('lista_usuarios')
    return render(request, 'accounts/confirmar_desactivar.html', {
        'usuario': usuario
    })


@login_required(login_url='login')
@rol_requerido('Supervisor')
def activar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk, iglesia=request.user.iglesia)
    usuario.is_active = True
    usuario.save()
    messages.success(request, f'Usuario "{usuario.username}" activado.')
    return redirect('lista_usuarios')


@login_required(login_url='login')
@rol_requerido('Supervisor')
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk, iglesia=request.user.iglesia)
    if usuario == request.user:
        messages.error(request, 'No puedes eliminarte a ti mismo.')
        return redirect('lista_usuarios')
    if request.method == 'POST':
        nombre = usuario.username
        usuario.delete()
        messages.success(request, f'Usuario "{nombre}" eliminado correctamente.')
        return redirect('lista_usuarios')
    return render(request, 'accounts/confirmar_eliminar_usuario.html', {
        'usuario': usuario
    })