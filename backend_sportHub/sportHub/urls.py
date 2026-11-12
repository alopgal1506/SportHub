from django.urls import path
from . import views


urlpatterns = [
   path('', views.index, name='index'),
   path('trabajadores/incidencias/', views.trabajadores_incidencias, name='trabajadores_incidencias'),

]