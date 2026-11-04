from django.shortcuts import render
from .models import Pista

# Create your views here.
def index(request):
    return render(request, 'index.html')

    # Mostar todas las pistas disponibles de un polideportivo
def pistasDisponibles(request, idPoli, nuevoEstado):
    pistas = Pista.objects.select_related("idPolideportivo").filter(idPolideportivo = idPoli, estado = nuevoEstado)
    return render(request,'pistasDisponibles.html',{'pistas':pistas})