from django.urls import path
from . import views


urlpatterns = [
   path('', views.index, name='index'),
   path('pistas/disponibles/<int:idPoli>/<str:nuevoEstado>/', views.pistasDisponibles, name='pistasDisponibles')
]