from django.urls import path
from . import views


urlpatterns = [
<<<<<<< HEAD
    path('', views.index, name='index'),
    path('pistas/<str:nuevoTipo>/<str:nuevoEstado>/', views.pistasFiltradas, name='pistasFiltradas'),
=======
   path('', views.index, name='index'),
   path('polideportivo/<int:idAdmin>/<str:nombreCiudad>/', views.polideportivo, name='polideportivo'),
>>>>>>> d0d61de0cb65a798a6cf862a02baf4c9fb3f8dd9
]