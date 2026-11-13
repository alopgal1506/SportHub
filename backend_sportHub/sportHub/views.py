from django.shortcuts import render
from .models import Pista,Incidencia
from django.db.models import Prefetch


# Create your views here.
def index(request):
    return render(request, 'index.html')
    # Incidencia en un año en concreto
def incidenciasPorAno(request, ano):
    incidencias = Incidencia.objects.filter(fecha__year=ano).prefetch_related(Prefetch('pistas', queryset=Pista.objects.select_related('idPolideportivo', 'idSistema_Control', 'idUsuario'))).order_by('-fecha')
    return render(request, 'incidenciasPorAno.html', {'incidencias': incidencias,'ano': ano})