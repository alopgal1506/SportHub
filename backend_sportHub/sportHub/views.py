from django.shortcuts import render
from django.db.models import Avg, Max, Min, Count
from django.views.defaults import page_not_found
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.http import Http404
from .models import Pista, Polideportivo, Usuario, Administrador, Direccion

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

    #Mostrar todos los polideportivos que administra un administardor en una ciudad en concreto
def polideportivo(requets, idAdmin, nombreCiudad):
    polideportivo = Polideportivo.objects.select_related('idUsuario', 'idDireccion').filter(idUsuario = idAdmin, idDireccion__ciudad=nombreCiudad)
    return render(requets, 'polideportivo.html', {'polideportivo': polideportivo})

"""
def polideportivo(request, idAdmin, nombreCiudad):
    polideportivo = Polideportivo.objects.raw(
        "SELECT * FROM Polideportivo WHERE idUsuario_id = %s AND idDireccion_id IN (SELECT idDireccion FROM Direccion WHERE ciudad = %s)",
        [idAdmin, nombreCiudad]
    )
    return render(request, 'polideportivo.html', {'polideportivo': polideportivo})

"""

def mi_error_400(request,exception=None):
    return render(request, 'errores/400.html',None,None,400)

def mi_error_403(request,exception=None):
    return render(request, 'errores/403.html',None,None,403)

def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

def mi_error_500(request):
    return render(request, 'errores/500.html',None,None,500)


# VISTAS TEMPORALES PARA PROBAR LOS ERRORES

def probar_400(request):
    raise SuspiciousOperation("Prueba intencional del error 400")

def probar_403(request):
    raise PermissionDenied("Prueba intencional del error 403")

def probar_404(request):
    raise Http404("Prueba intencional del error 404")

def probar_500(request):
    resultado = 1 / 0  # Esto fuerza un error 500 
    return render(request, 'inicio.html')


