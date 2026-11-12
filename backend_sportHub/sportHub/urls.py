from django.urls import path
from . import views


urlpatterns = [
   path('', views.index, name='index'),
   path('notificaciones/<int:id>/', views.notificaciones_usuario, name='notificaciones_usuario'),

]