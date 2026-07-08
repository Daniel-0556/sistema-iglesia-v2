from .models import ConfiguracionSitio


def configuracion_sitio(request):
    try:
        config = ConfiguracionSitio.objects.first()
    except Exception:
        config = None
    return {'config': config}