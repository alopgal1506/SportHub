from django.shortcuts import render
from .models import Notificacion, Pista
from django.db.models import Avg, Max, Min, Count

# Create your views here.
def index(request):
    return render(request, 'index.html')

def notificaciones_usuario(request, id):
    notificaciones = Notificacion.objects.filter(destinatarios__idUsuario=id).order_by('-fecha_envio')

    return render(request, 'notificaciones_usuario.html', {
        'notificaciones': notificaciones
    })
    