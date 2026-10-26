import random
from django.core.management.base import BaseCommand
from faker import Faker
from sportHub.models import *


class Command(BaseCommand):
    help = 'Generando datos usando Faker'

    def handle(self, *args, **kwargs):
        fake = Faker('es_ES')

        # Crear 10 Direcciones
        direcciones = []
        for _ in range(10):
            d = Direccion.objects.create(
                codigoPostal=random.randint(1000, 52999),
                ciudad=fake.city(),
                calleNumero=fake.street_address()
            )
            direcciones.append(d)

        # Crear 10 Descuentos
        descuentos = []
        for _ in range(10):
            d = Descuento.objects.create(
                porcentaje=random.randint(5, 50)
            )
            descuentos.append(d)

        # Crear 10 Usuarios
        usuarios = []
        for _ in range(10):
            u = Usuario.objects.create(
                nombreUsuario=fake.user_name()[:20],
                nombre=fake.first_name(),
                apellidos=fake.last_name(),
                correoElectronico=fake.unique.email(),
                dni=fake.unique.nif(),
                contrasenia=fake.unique.sha256(),
                telefono=random.randint(600000000, 699999999),
                fechaAlta=fake.date_between(start_date='-2y', end_date='today')
            )
            usuarios.append(u)

        # Crear 10 Administradores
        administradores = []
        for _ in range(10):
            a = Administrador.objects.create(
                nombreUsuario=fake.user_name()[:20],
                nombre=fake.first_name(),
                apellidos=fake.last_name(),
                correoElectronico=fake.unique.email(),
                dni=fake.unique.nif(),
                contrasenia=fake.unique.sha256(),
                telefono=random.randint(600000000, 699999999),
                fechaAlta=fake.date_between(start_date='-2y', end_date='today'),
                cargo=fake.job()[:50]
            )
            administradores.append(a)

        # Crear 10 Trabajadores
        trabajadores = []
        for _ in range(10):
            t = Trabajador.objects.create(
                nombreUsuario=fake.user_name()[:20],
                nombre=fake.first_name(),
                apellidos=fake.last_name(),
                correoElectronico=fake.unique.email(),
                dni=fake.unique.nif(),
                contrasenia=fake.unique.sha256(),
                telefono=random.randint(600000000, 699999999),
                fechaAlta=fake.date_between(start_date='-2y', end_date='today'),
                CodigoDescuento=fake.unique.bothify('DESC-????-####').upper(),
                Puesto=fake.job()[:50],
                fechaContratacion=fake.date_between(start_date='-5y', end_date='today'),
                descuento=random.choice(descuentos)
            )
            trabajadores.append(t)

        # Crear 10 Notificaciones
        tipos = ["RESER", "ANUL", "REGIST"]
        notificaciones = []
        for _ in range(10):
            n = Notificacion.objects.create(
                tipo=random.choice(tipos),
                mensaje=fake.sentence(nb_words=10),
                leida=fake.boolean()
            )
            notificaciones.append(n)

        # Crear 10 Sistemas de Control
        sistemas = []
        for _ in range(10):
            s = Sistema_Control.objects.create(
                num_serie=random.randint(1000, 999999),
                direccion_IP=fake.ipv4(),
                modelo_fabricante=fake.bothify('???###').upper()
            )
            sistemas.append(s)

        # Crear 10 Polideportivos
        polideportivos = []
        for i in range(10):
            p = Polideportivo.objects.create(
                nombre='Polideportivo ' + fake.last_name(),
                idUsuario=random.choice(administradores),
                idDireccion=direcciones[i]
            )
            polideportivos.append(p)

        # Crear 10 Pistas
        pistas = []
        for _ in range(10):
            p = Pista.objects.create(
                tipo=random.choice(["Tenis", "Pádel", "Baloncesto", "Fútbol sala"]),
                estado=random.choice(["Disponible", "Ocupada", "Mantenimiento"]),
                metro=random.randint(100, 4000) / 10,
                idUsuario=random.choice(usuarios),
                idPolideportivo=random.choice(polideportivos),
                idSistema_Control=random.choice(sistemas)
            )
            pistas.append(p)

        # Crear 10 Incidencias
        incidencias = []
        for _ in range(10):
            i = Incidencia.objects.create(
                descripcion=fake.text(max_nb_chars=200),
                num_pista=random.randint(1, 20),
                titulo=fake.sentence(nb_words=4)[:100]
            )
            incidencias.append(i)

        # Tablas intermedias
        for _ in range(10):
            Resuelve.objects.create(
                idUsuario=random.choice(trabajadores),
                idIncidencia=random.choice(incidencias)
            )
            Recibe.objects.create(
                idUsuario=random.choice(usuarios),
                idNotificacion=random.choice(notificaciones)
            )
            Registra.objects.create(
                idPista=random.choice(pistas),
                idIncidencia=random.choice(incidencias)
            )
            Reporta.objects.create(
                idUsuario=random.choice(usuarios),
                idIncidencia=random.choice(incidencias)
            )

        self.stdout.write(self.style.SUCCESS('Datos generados correctamente'))