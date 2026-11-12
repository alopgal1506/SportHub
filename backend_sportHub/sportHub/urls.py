from django.urls import path
from . import views


urlpatterns = [
   path('', views.index, name='index'),
   path('incidencias/sin-resolver/', views.incidencias_sin_resolver, name='incidencias_sin_resolver'),

]