from django.shortcuts import render
from .models import Pista, Trabajador
from django.db.models import Avg, Max, Min, Count

# Create your views here.
def index(request):
    return render(request, 'index.html')

def trabajadores_descuento(request):
    trabajadores = Trabajador.objects.filter(descuento__porcentaje__lt=15).prefetch_related('incidencias_resueltas')

    return render(request, 'trabajadores_descuento.html', {
        'trabajadores': trabajadores
    })
    
"""
    def trabajadores_descuento(request):
    trabajadores = Trabajador.objects.raw(
        "SELECT Usuario.* FROM Usuario "
        "INNER JOIN Trabajador ON Usuario.idUsuario = Trabajador.usuario_ptr_id "
        "INNER JOIN Descuento ON Trabajador.descuento_id = Descuento.idDescuento "
        "WHERE Descuento.porcentaje < %s",
        [15]
    )

    return render(request, 'trabajadores_descuento.html', {
        'trabajadores': trabajadores
    })
"""