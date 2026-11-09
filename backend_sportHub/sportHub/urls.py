from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('pistas/<str:nuevoTipo>/<str:nuevoEstado>/', views.pistasFiltradas, name='pistasFiltradas'),
]