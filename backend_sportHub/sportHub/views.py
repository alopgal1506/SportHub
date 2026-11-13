from django.shortcuts import render
from .models import Pista

# Create your views here.
def index(request):
    return render(request, 'index.html')

    # Mostar todas las pistas disponibles de un polideportivo
def pistasDisponibles(request, idPoli, nuevoEstado):
    pistas = Pista.objects.select_related("idPolideportivo").filter(idPolideportivo = idPoli, estado = nuevoEstado)
    return render(request,'pistasDisponibles.html',{'pistas':pistas})


"""
def pistasDisponibles(request, idPoli, nuevoEstado):
    pistas = Pista.objects.raw(
        "SELECT pista.*, polideportivo.nombre, usuario.nombreUsuario "
        "FROM sportHub_pista pista "
        "INNER JOIN sportHub_polideportivo polideportivo ON pista.idPolideportivo_id = polideportivo.idPolideportivo "
        "LEFT JOIN sportHub_usuario usuario ON pista.idUsuario_id = usuario.idUsuario "
        "WHERE pista.idPolideportivo_id = %s AND pista.estado = %s",
        [idPoli, nuevoEstado]
    )
    return render(request, 'pistasDisponibles.html', {'pistas': pistas})
"""