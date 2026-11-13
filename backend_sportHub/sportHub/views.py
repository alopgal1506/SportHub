from django.shortcuts import render
from .models import Notificacion, Pista
from django.db.models import Avg, Max, Min, Count

# Create your views here.
def index(request):
    return render(request, 'index.html')
    # Notificaciones de un usuario ordenadas por fecha y solo salen los 5 primeros regisros
def notificaciones_usuario(request, id):
    notificaciones = Notificacion.objects.filter(destinatarios__idUsuario=id).order_by('-fecha_envio')[:5]
    return render(request, 'notificaciones_usuario.html', {
        'notificaciones': notificaciones
    })
   
"""
    def notificaciones_usuario(request, id):
    notificaciones = Notificacion.objects.raw(
        "SELECT Notificacion.* FROM Notificacion "
        "INNER JOIN Usuario_notificaciones ON Notificacion.idNotificacion = Usuario_notificaciones.notificacion_id "
        "WHERE Usuario_notificaciones.usuario_id = %s "
        "ORDER BY fecha_envio DESC",
        "LIMIT 5",
        [id]
    )

    return render(request, 'notificaciones_usuario.html', {
        'notificaciones': notificaciones
    })
"""