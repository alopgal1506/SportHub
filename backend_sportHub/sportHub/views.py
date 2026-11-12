from django.shortcuts import render
from .models import Pista, Polideportivo, Usuario, Administrador, Direccion

# Create your views here.
def index(request):
    return render(request, 'index.html')

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