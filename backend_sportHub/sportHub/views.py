from django.shortcuts import render
from .models import Incidencia, Pista
from django.db.models import Avg, Max, Min, Count

# Create your views here.
def index(request):
    return render(request, 'index.html')

def incidencias_sin_resolver(request):
    incidencias = Incidencia.objects.filter(resolutores__isnull=True)

    return render(request, 'incidencias_sin_resolver.html', {
        'incidencias': incidencias
    })
    
"""
    def incidencias_sin_resolver(request):
    incidencias = Incidencia.objects.raw(
        "SELECT * FROM Incidencia WHERE idIncidencia NOT IN (SELECT idIncidencia_id FROM Resuelve)"
    )

    return render(request, 'incidencias_sin_resolver.html', {
        'incidencias': incidencias
    })
"""