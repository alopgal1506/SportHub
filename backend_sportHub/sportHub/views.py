from django.shortcuts import render
from .models import Pista
from django.db.models import Q
# Create your views here.
def index(request):
    return render(request, 'index.html')

def pistasConIncidencias(request, texto):
    incidencia = Pista.objects.prefetch_related('incidencias').filter(Q(incidencias__titulo__icontains=texto) | Q(incidencias__descripcion__icontains=texto) )
    return render(request, 'pistasConIncidencias.html', {'incidencia': incidencia, 'texto': texto})