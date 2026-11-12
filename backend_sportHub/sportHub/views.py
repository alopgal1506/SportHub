from django.shortcuts import render
from .models import Pista, Trabajador
from django.db.models import Avg, Max, Min, Count

# Create your views here.
def index(request):
    return render(request, 'index.html')


def trabajadores_incidencias(request):
    trabajadores = Trabajador.objects.prefetch_related('incidencias_resueltas')

    return render(request, 'trabajadores_incidencias.html', {
        'trabajadores': trabajadores
    })
    
"""
def trabajadores_incidencias(request):
    trabajadores = Trabajador.objects.raw(
        "SELECT Usuario.* FROM Usuario "
        "INNER JOIN Trabajador ON Usuario.idUsuario = Trabajador.usuario_ptr_id "
        "INNER JOIN Resuelve ON Trabajador.usuario_ptr_id = Resuelve.idUsuario_id"
    )

    return render(request, 'trabajadores_incidencias.html', {
        'trabajadores': trabajadores
    })   

"""