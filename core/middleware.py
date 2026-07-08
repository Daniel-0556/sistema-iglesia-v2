from django.shortcuts import render
from .models import ModoMantenimiento


class MantenimientoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            mantenimiento = ModoMantenimiento.objects.first()
            if mantenimiento and mantenimiento.activo:
                if not request.user.is_superuser:
                    if not request.path.startswith('/admin'):
                        return render(request, 'mantenimiento.html', {
                            'mensaje': mantenimiento.mensaje,
                            'contacto': mantenimiento.contacto,
                        }, status=503)
        except Exception:
            pass
        return self.get_response(request)