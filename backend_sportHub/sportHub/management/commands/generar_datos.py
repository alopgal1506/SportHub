import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
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
                provincia=random.choice(['Sevilla', 'Madrid', 'Barcelona', 'Valencia', 'Málaga']),
                calleNumero=fake.street_address()
            )
            direcciones.append(d)

        # Crear 10 Descuentos
        descuentos = []
        for _ in range(10):
            inicio = fake.date_between(start_date='-1y', end_date='today')
            d = Descuento.objects.create(
                porcentaje=random.randint(5, 50),
                codigo=fake.unique.bothify('DESC-????-####').upper(),
                fechaInicio=inicio,
                fechaFin=inicio + timedelta(days=random.randint(30, 365)),
                activo=fake.boolean()
            )
            descuentos.append(d)

        # Crear 10 Usuarios
        usuarios = []
        for _ in range(10):
            u = Usuario.objects.create(
                nombreUsuario=fake.unique.user_name()[:20],
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
                nombreUsuario=fake.unique.user_name()[:20],
                nombre=fake.first_name(),
                apellidos=fake.last_name(),
                correoElectronico=fake.unique.email(),
                dni=fake.unique.nif(),
                contrasenia=fake.unique.sha256(),
                telefono=random.randint(600000000, 699999999),
                fechaAlta=fake.date_between(start_date='-2y', end_date='today'),
                cargo=fake.job()[:50],
                nivelAcceso=random.choice([1, 2, 3]),
                fechaNombramiento=fake.date_between(start_date='-3y', end_date='today')
            )
            administradores.append(a)

        # Crear 10 Trabajadores
        trabajadores = []
        for _ in range(10):
            t = Trabajador.objects.create(
                nombreUsuario=fake.unique.user_name()[:20],
                nombre=fake.first_name(),
                apellidos=fake.last_name(),
                correoElectronico=fake.unique.email(),
                dni=fake.unique.nif(),
                contrasenia=fake.unique.sha256(),
                telefono=random.randint(600000000, 699999999),
                fechaAlta=fake.date_between(start_date='-2y', end_date='today'),
                codigoDescuento=fake.unique.bothify('TRAB-????-####').upper(),
                puesto=fake.job()[:50],
                fechaContratacion=fake.date_between(start_date='-5y', end_date='today'),
                descuento=random.choice(descuentos)
            )
            trabajadores.append(t)

        # Crear 10 Notificaciones
        tipos = ["RESER", "ANUL", "REGIST"]
        notificaciones = []
        for _ in range(10):
            leida = fake.boolean()
            n = Notificacion.objects.create(
                tipo=random.choice(tipos),
                mensaje=fake.sentence(nb_words=10),
                leida=leida,
                fecha_lectura=timezone.now() if leida else None
            )
            notificaciones.append(n)

        # Crear 10 Sistemas de Control
        sistemas = []
        for _ in range(10):
            s = Sistema_Control.objects.create(
                num_serie=random.randint(1000, 999999),
                direccion_IP=fake.ipv4(),
                modelo_fabricante=fake.bothify('???###').upper(),
                fecha_instalacion=fake.date_between(start_date='-3y', end_date='today')
            )
            sistemas.append(s)

        # Crear 10 Polideportivos (1:1 con Administrador y con Direccion)
        polideportivos = []
        for i in range(10):
            p = Polideportivo.objects.create(
                nombre='Polideportivo ' + fake.last_name(),
                descripcion=fake.text(max_nb_chars=150),
                idUsuario=administradores[i],
                idDireccion=direcciones[i]
            )
            polideportivos.append(p)

        # Crear 10 Pistas (1:1 con Sistema_Control)
        pistas = []
        for i in range(10):
            p = Pista.objects.create(
                tipo=random.choice(["Tenis", "Pádel", "Baloncesto", "Fútbol sala"]),
                estado=random.choice(["DISP", "OCUP", "MANT"]),
                metro=random.randint(100, 4000) / 10,
                precioHora=random.randint(8, 30),
                idUsuario=random.choice(usuarios),
                idPolideportivo=random.choice(polideportivos),
                idSistema_Control=sistemas[i]
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

        # Relaciones muchos a muchos (se rellenan con .add)

        # Recibe: cada usuario recibe entre 1 y 3 notificaciones
        for u in usuarios:
            u.notificaciones.add(*random.sample(notificaciones, random.randint(1, 3)))

        # Reporta: cada usuario reporta entre 1 y 2 incidencias
        for u in usuarios:
            u.incidencias_reportadas.add(*random.sample(incidencias, random.randint(1, 2)))

        # Registra: cada pista tiene entre 1 y 3 incidencias
        for p in pistas:
            p.incidencias.add(*random.sample(incidencias, random.randint(1, 3)))

        # Resuelve (tabla intermedia propia, con atributos extra)
        for _ in range(10):
            Resuelve.objects.create(
                idUsuario=random.choice(trabajadores),
                idIncidencia=random.choice(incidencias),
                observaciones=fake.sentence(nb_words=8)
            )

        self.stdout.write(self.style.SUCCESS('Datos generados correctamente'))