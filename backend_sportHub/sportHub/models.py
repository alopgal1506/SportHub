from django.db import models

class Notificacion (models.Model):
    notificaciones=[
        ("RESER", "Reserva"),
        ("ANUL", "Anular"),
        ("REGIST", "rEGISTRO"),
    ]
    idNotificacion = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo = models.models.CharField(_(""), max_length=50, choices=notificaciones, default="")