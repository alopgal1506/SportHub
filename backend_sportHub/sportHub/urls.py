from django.urls import path,  re_path
from . import views


urlpatterns = [
   path('', views.index, name='index'),
   path('pistas/disponibles/<int:idPoli>/<str:nuevoEstado>/', views.pistasDisponibles, name='pistasDisponibles'),
   path('polideportivo/<int:idAdmin>/<str:nombreCiudad>/', views.polideportivo, name='polideportivo'),
   path('pistas/<str:nuevoTipo>/<str:nuevoEstado>/', views.pistasFiltradas, name='pistasFiltradas'),
   path('incidencia/<str:texto>/', views.pistasConIncidencias, name='pistasConIncidencias'),
   re_path(r'^incidencias/ano/(\d{4})/$', views.incidenciasPorAno, name='incidenciasPorAno'),
   path('precios/', views.listaPrecios, name='listaPrecios'),
   path('incidencias/sin-resolver/', views.incidencias_sin_resolver, name='incidencias_sin_resolver'),
   path('notificaciones/<int:id>/', views.notificaciones_usuario, name='notificaciones_usuario'),
   path('probar-400/', views.probar_400, name='probar_400'),
   path('probar-403/', views.probar_403, name='probar_403'),
   path('probar-404/', views.probar_404, name='probar_404'),
   path('probar-500/', views.probar_500, name='probar_500'),


]