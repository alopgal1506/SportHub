from django.shortcuts import render
from .models import Pista

# Create your views here.
def index(request):
    return render(request, 'index.html')
    #Pistas filtradas por tipo y estado
def pistasFiltradas(request, nuevoTipo ,nuevoEstado):
    pistas = Pista.objects.filter(tipo=nuevoTipo,estado=nuevoEstado)
    return render(request,'pistasFiltradas.html', {'pistas':pistas})

"""
    def pistasFiltradas(request, nuevoTipo, nuevoEstado):
    pistas = Pista.objects.raw(
        "SELECT * FROM Pista WHERE tipo = %s AND estado = %s",
        [nuevoTipo, nuevoEstado]
    )
    return render(request, 'pistasFiltradas.html', {'pistas': pistas})
"""