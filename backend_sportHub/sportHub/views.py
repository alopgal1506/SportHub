from django.shortcuts import render
from .models import Pista
from django.db.models import Avg, Max, Min, Count
from django.views.defaults import page_not_found
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.http import Http404

# Create your views here.
def index(request):
    return render(request, 'index.html')

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