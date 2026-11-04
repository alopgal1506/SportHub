from django.urls import path
from . import views


urlpatterns = [
   path('', views.index, name='index'),
   path('polideportivo/<int:idAdmin>/<str:nombreCiudad>/', views.polideportivo, name='polideportivo'),
]