from django.contrib import admin

# Register your models here.
from .models import Usuario,Administrador,Descuento,Trabajador,Direccion,Notificacion,Sistema_Control,Polideportivo,Incidencia,Pista,Resuelve
admin.site.register(Usuario)
admin.site.register(Administrador)
admin.site.register(Descuento)
admin.site.register(Trabajador)
admin.site.register(Direccion)
admin.site.register(Notificacion)
admin.site.register(Sistema_Control)
admin.site.register(Polideportivo)
admin.site.register(Incidencia)
admin.site.register(Pista)
admin.site.register(Resuelve)