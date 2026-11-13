from django.shortcuts import render
from .models import Pista
from django.db.models import Q
# Create your views here.
def index(request):
    return render(request, 'index.html')

    # Incidencias cuyo titulo o descripcion contenga el texto con sus vistas
def pistasConIncidencias(request, texto):
    incidencia = Pista.objects.prefetch_related('incidencias').filter(Q(incidencias__titulo__icontains=texto) | Q(incidencias__descripcion__icontains=texto) )
    return render(request, 'pistasConIncidencias.html', {'incidencia': incidencia, 'texto': texto})


"""
def pistasConIncidencias(request, texto):
    incidencia = Pista.objects.raw(
        "SELECT DISTINCT pista.* "
        "FROM sportHub_pista pista "
        "INNER JOIN sportHub_pista_incidencias pi ON pista.idPista = pi.pista_id "
        "INNER JOIN sportHub_incidencia inc ON pi.incidencia_id = inc.idIncidencia "
        "WHERE inc.titulo LIKE '%%' || %s || '%%' "
        "OR inc.descripcion LIKE '%%' || %s || '%%'",
        [texto, texto]
    )
    return render(request, 'pistasConIncidencias.html', {'incidencia': incidencia, 'texto': texto})
"""