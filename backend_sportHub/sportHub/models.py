from datetime import date, time
from django.db import models
from django.utils import timezone


class Usuario(models.Model):
    idUsuario = models.AutoField(primary_key=True)
    nombreUsuario = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=20)
    apellidos = models.CharField(max_length=50)
    correoElectronico = models.EmailField(max_length=200, unique=True)
    dni = models.CharField(max_length=9, unique=True)
    contrasenia = models.CharField(max_length=128, help_text="Contraseña cifrada")
    telefono = models.IntegerField(null=True, blank=True)
    fechaAlta = models.DateField(default=date.today)

    # N:M Recibe
    notificaciones = models.ManyToManyField(
        'Notificacion', related_name='destinatarios', blank=True
    )
    # N:M  Reporta 
    incidencias_reportadas = models.ManyToManyField(
        'Incidencia', related_name='reportada_por', blank=True
    )

    def __str__(self):
        return f"{self.nombreUsuario} ({self.nombre} {self.apellidos}) - DNI: {self.dni}"


class Administrador(Usuario):
    cargo = models.CharField(max_length=50)
    nivelAcceso = models.IntegerField(default=1, choices=[(1, "Básico"), (2, "Medio"), (3, "Total")])
    fechaNombramiento = models.DateField(default=date.today)

    def __str__(self):
        return f"{super().__str__()} - Cargo: {self.cargo}"


class Descuento(models.Model):
    idDescuento = models.AutoField(primary_key=True)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)
    codigo = models.CharField(max_length=20, unique=True)
    fechaInicio = models.DateField(default=date.today)
    fechaFin = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Descuento {self.codigo}: {self.porcentaje}%"


class Trabajador(Usuario):
    codigoDescuento = models.CharField(max_length=20, unique=True)
    puesto = models.CharField(max_length=50)
    fechaContratacion = models.DateField()
    # 1:N  Aplica
    descuento = models.ForeignKey(Descuento, on_delete=models.CASCADE, related_name='trabajadores')
    # N:M Resuelve 
    incidencias_resueltas = models.ManyToManyField(
        'Incidencia', through='Resuelve', related_name='resolutores', blank=True
    )

    def __str__(self):
        return f"{super().__str__()} - Puesto: {self.puesto}"


class Direccion(models.Model):
    idDireccion = models.AutoField(primary_key=True)
    codigoPostal = models.IntegerField()
    ciudad = models.CharField(max_length=50)
    provincia = models.CharField(max_length=50, blank=True)
    calleNumero = models.TextField()

    def __str__(self):
        return f"{self.calleNumero}, {self.codigoPostal} {self.ciudad}"


class Notificacion(models.Model):
    TIPOS = [
        ("RESER", "Reserva"),
        ("ANUL", "Anular"),
        ("REGIST", "Registrado"),
    ]
    idNotificacion = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=50, choices=TIPOS, default="RESER")
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(default=timezone.now)
    leida = models.BooleanField(default=False)
    fecha_lectura = models.DateTimeField(null=True, blank=True)

    def marcar_leida(self):
        self.leida = True
        self.fecha_lectura = timezone.now()
        self.save()

    def __str__(self):
        return f"[{self.tipo}] {self.mensaje[:40]}"


class Sistema_Control(models.Model):
    idSistema_Control = models.AutoField(primary_key=True)
    num_serie = models.IntegerField(default=0, db_column='numero_serie')
    direccion_IP = models.GenericIPAddressField()
    modelo_fabricante = models.CharField(max_length=6)
    fecha_instalacion = models.DateField(default=date.today)

    def __str__(self):
        return f"Sistema {self.modelo_fabricante} (serie {self.num_serie}, IP {self.direccion_IP})"


class Polideportivo(models.Model):
    idPolideportivo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    hora_apertura = models.TimeField(default=time(9, 0))
    hora_cierre = models.TimeField(default=time(22, 0))
    # 1:1  Gestiona 
    idUsuario = models.OneToOneField(Administrador, on_delete=models.CASCADE, related_name='polideportivo')
    # 1:1  Localiza
    idDireccion = models.OneToOneField(Direccion, on_delete=models.CASCADE, related_name='polideportivo')

    def __str__(self):
        return f"{self.nombre} ({self.hora_apertura:%H:%M}-{self.hora_cierre:%H:%M})"


class Incidencia(models.Model):
    idIncidencia = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    num_pista = models.IntegerField()
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Incidencia {self.idIncidencia}: {self.titulo} (pista {self.num_pista})"


class Pista(models.Model):
    ESTADOS = [
        ("DISP", "Disponible"),
        ("OCUP", "Ocupada"),
        ("MANT", "Mantenimiento"),
    ]
    idPista = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=50)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="DISP")
    metro = models.DecimalField(max_digits=6, decimal_places=2)
    precioHora = models.DecimalField(max_digits=6, decimal_places=2, default=10)
    # 1:N  Reserva 
    idUsuario = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='pistas_reservadas'
    )
    # 1:N  Contiene 
    idPolideportivo = models.ForeignKey(Polideportivo, on_delete=models.CASCADE, related_name='pistas')
    # 1:1  Pertenece 
    idSistema_Control = models.OneToOneField(Sistema_Control, on_delete=models.CASCADE, related_name='pista')
    # N:M  Registra 
    incidencias = models.ManyToManyField(Incidencia, related_name='pistas', blank=True)

    def __str__(self):
        return f"Pista {self.idPista}: {self.tipo} ({self.get_estado_display()})"


class Resuelve(models.Model):
    """Tabla intermedia N:M Trabajador - Incidencia con atributos extra."""
    idUsuario = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    idIncidencia = models.ForeignKey(Incidencia, on_delete=models.CASCADE)
    fecha_resolver = models.DateTimeField(default=timezone.now)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"{self.idUsuario.nombreUsuario} resolvió la incidencia {self.idIncidencia_id}"
   