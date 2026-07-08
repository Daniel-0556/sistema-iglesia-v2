from miembros.models import SolicitudEliminacion


def solicitudes_pendientes(request):
    if request.user.is_authenticated and request.user.rol:
        if request.user.rol.nombre_rol == 'Supervisor':
            count = SolicitudEliminacion.objects.filter(
                estado='pendiente',
                persona__iglesia=request.user.iglesia
            ).count()
            return {'solicitudes_pendientes': count}
    return {'solicitudes_pendientes': 0}