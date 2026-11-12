from django.urls import path,  re_path
from . import views


urlpatterns = [
   path('', views.index, name='index'),
   re_path(r'^incidencias/ano/(\d{4})/$', views.incidenciasPorAno, name='incidenciasPorAno'),
]