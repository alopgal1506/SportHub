from django.urls import path
from . import views


urlpatterns = [
   path('', views.index, name='index'),
   path('incidencia/<str:texto>/', views.pistasConIncidencias, name='pistasConIncidencias')
]