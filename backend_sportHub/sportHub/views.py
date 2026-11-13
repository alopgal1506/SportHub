from django.shortcuts import render
from .models import Pista
from django.db.models import Avg, Max, Min, Count

# Create your views here.
def index(request):
    return render(request, 'index.html')

    # Precio AVG, MAX, MIN y el count de las pistas
def listaPrecios(request):
    precio = Pista.objects.aggregate(Avg("precioHora"), Max("precioHora"), Min("precioHora"), Count("idPista"))
    media = precio["precioHora__avg"]
    maximo = precio["precioHora__max"]
    minimo = precio["precioHora__min"]
    total = precio["idPista__count"]
    return render(request, 'listaPrecios.html', {"media": media,"maximo": maximo,"minimo": minimo,"total": total,})

"""
    SELECT 
    AVG(precioHora) AS media,
    MAX(precioHora) AS maximo,
    MIN(precioHora) AS minimo,
    COUNT(idPista) AS total
    FROM Pista;
"""