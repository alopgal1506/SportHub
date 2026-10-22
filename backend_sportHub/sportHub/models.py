from django.db import models
from django.utils import timezone
from datetime import time

class Usuario (models.Model):
    idUsuario = models.AutoField(primary_key=True)
    nombreUsuario = models.CharField(max_length=20)
    nombre = models.CharField(max_length=20)
    apellidos = models.CharField(max_length=50)
    correoElectronico = models.CharField(max_length=200,unique=True)
    dni = models.CharField(max_length=9, unique= True)
    contrasenia = models.CharField(max_length=128, unique=True)
    telefono = models.IntegerField()
    fechaAlta = models.DateField()
    
    def publish(self):
            self.fecha_envio = timezone.now()
            self.save()
        
    def publish(self):
            self.fecha_lectura = timezone.now()
            self.save()
        
    def __str__(self):
        return "Id: " + self.idUsuario + " Nombre Usuario: " + self.nombreUsuario + " Nombre: " + self.nombre + " Apellidos: " + self.apellidos + " Correo Eelectronico: " + self.correoElectronico + " DNI: " + self.dni +" Contraseña: " + self.contrasenia + " Telefono: " + self.telefono + " Fecha de alta: " + self.fechaAlta


            
class Administrador (Usuario):
    cargo = models.CharField(max_length=50)
        
    def __str__(self):
         return {super().__str__()} + " Cargo: " +  self.cargo
 
    
class Direccion (models.Model):
    idDireccion = models.AutoField(primary_key=True)
    codigoPostal = models.IntegerField()
    ciudad = models.CharField(max_length=50)
    calleNumero = models.TextField()

    
    def __str__(self):
        return "Id: " + self.idDireccion + " Codigo Postal: " + self.codigoPostal + " Ciudad: " + self.ciudad + " Calle y numero: " + self.calleNumero

class Descuento(models.Model):
    idDescuento = models.AutoField(primary_key=True)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return f"Descuento {self.idDescuento}: {self.porcentaje}%"


class Trabajador(Usuario):
    CodigoDescuento = models.CharField(max_length=20, unique=True)
    Puesto = models.CharField(max_length=50)
    fechaContratacion = models.DateField()
    descuento = models.ForeignKey(Descuento, on_delete=models.CASCADE,related_name='trabajadores')
    
    def __str__(self):
        return {super().__str__()} + " Puesto: " + self.Puesto + " Fecha de Contratacion: " + self.fechaContratacion + " Codigo de descuento" + self.CodigoDescuento
    
    
class Notificacion (models.Model):
    notificaciones=[
        ("RESER", "Reserva"),
        ("ANUL", "Anular"),
        ("REGIST", "Registrado"),
    ]
    idNotificacion = models.AutoField(primary_key=True)
    tipo = models.CharField( max_length=50, choices=notificaciones, default="RESER")
    mensaje= models.TextField()
    fecha_envio=models.DateTimeField(default=timezone.now)
    leida=models.BooleanField(default=False)
    fecha_lectura=models.DateTimeField(default=timezone.now)
    
    def publish(self):
        self.fecha_envio = timezone.now()
        self.save()
    
    def publish(self):
        self.fecha_lectura = timezone.now()
        self.save()
    
    def __str__ (self):
        return  "ID= "+self.idNotificacion+"Tipo notifiacion: "+self.tipo+ ", Mensaje: "+self.mensaje+ ", Fecha de envio: "+ self.fecha_envio+ ", Estado: "+self.estado+ ", Fecha de lectura: "+self.fecha_lectura


class Sistema_Control(models.Model):
    idSistema_Control= models.AutoField(primary_key=True)
    num_serie=models.IntegerField(default=0)
    direccion_IP=models.GenericIPAddressField()
    modelo_fabricante=models.CharField(max_length=6)
    
    def __str__ (self):
        return "ID: "+self.idSistema_Control+"Numero de serie: "+self.num_serie+ ", Dirección IP: "+self.direccion_IP+ ", Modelo de fabricante: "+ self.modelo_fabricante

    
class Polideportivo(models.Model):
    idPolideportivo =models.AutoField(primary_key=True)
    nombre= models.CharField(max_length=50)
    hora_apertura= models.TimeField(default=time(9, 0))
    hora_cierre= models.TimeField(default=time(22, 0))
    idUsuario=models.ForeignKey(Administrador, on_delete=models.CASCADE)
    idDireccion=models.OneToOneField(Direccion, on_delete=models.CASCADE)

    def __str__ (self):
        return "ID: "+self.idPolideportivo+"Nombre: "+self.nombre+ ", Hora de apertura: "+self.hora_apertura+ ", Hora de cierre: "+ self.hora_cierre+ ", Id Usuario: "+self.idUsuario+ ", Id Direccion: "+self.idDireccion

class Pista(models.Model):
    idPista = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=50)  
    estado = models.CharField(max_length=20)  
    metro = models.DecimalField(max_digits=6, decimal_places=2)
    idUsuario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    idPolideportivo = models.ForeignKey(Polideportivo,on_delete=models.CASCADE)
    idSistema_Control = models.ForeignKey(Sistema_Control,on_delete=models.CASCADE)

    def __str__(self):
        return "Pista: " + self.idPista + " Tipo: " + self.tipo + " Estado: " + self.estado

class Incidencia(models.Model):
    idIncidencia = models.AutoField(primary_key=True)
    descripcion = models.TextField()
    num_pista = models.IntegerField()
    titulo = models.CharField(max_length=100)
    fecha = models.DateTimeField(default=timezone.now)
    
    def publish(self):
        self.fecha = timezone.now()
        self.save()

    def __str__(self):
        return "idIncidencia" + self.idIncidencia + " Incidencia" + self.titulo + " Descripcion: " + self.descripcion + "Numero de pista: " + self.num_pista + "Fecha: " +  self.fecha

class Resuelve(models.Model):
    idUsuario=models.ForeignKey(Trabajador, on_delete=models.SET_NULL, null=True, blank=True)
    idIncidencia=models.ForeignKey(Incidencia, on_delete=models.CASCADE)
    fecha_resolver=models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return "ID Usuario: "+self.idUsuario+ ", ID Incidencia: "+self.idIncidencia+ " , Resuelta: "+self.fecha_resolver

class Recibe(models.Model):
    idUsuario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    idNotificacion = models.ForeignKey(Notificacion,on_delete=models.CASCADE)

    def __str__(self):
        return "Usuario" + self.idUsuario + " Notificación: " + self.idNotificacion
    
class Registra(models.Model):
    idPista = models.ForeignKey(Pista,on_delete=models.CASCADE)
    idIncidencia = models.ForeignKey(Incidencia,on_delete=models.CASCADE)
    
    def __str__(self):
        return "ID Pista" + self.idPista + " ID Incidencia: " + self.idIncidencia

class Reporta (models.Model):
    idUsuario = models.ForeignKey(Usuario,on_delete=models.CASCADE,)
    idIncidencia = models.ForeignKey(Incidencia, on_delete=models.CASCADE)


    def __str__(self):
        return "Usuario" + self.idUsuario + " Incidencia: " + self.idIncidencia
        