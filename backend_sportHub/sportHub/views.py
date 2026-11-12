from django.shortcuts import render
from .models import Pista
from django.db.models import Avg, Max, Min, Count

# Create your views here.
def index(request):
    return render(request, 'index.html')

