from django.urls import path
from . import views


urlpatterns = [
   path('', views.index, name='index'),
   path('trabajadores/descuento/', views.trabajadores_descuento, name='trabajadores_descuento'),

]