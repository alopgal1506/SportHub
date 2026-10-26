# SportHub

## 1. ¿En qué consiste la web?
SportHub es una aplicación web para gestionar y reservar pistas deportivas de polideportivos.

- Los **usuarios** se registran, reservan pistas, reciben notificaciones y reportan incidencias.
- Los **trabajadores** (son usuarios) resuelven incidencias y tienen un descuento asociado.
- Los **administradores** (son usuarios) gestionan un polideportivo.
- Cada **polideportivo** tiene una dirección y varias pistas; cada **pista** tiene un sistema de control y puede tener incidencias.

## 2. Modelo entidad-relación
En el documento entregado junto a este archivo

## 3. Modelos y atributos
Todas las claves primarias son `AutoField(primary_key=True)` (`idUsuario`, `idPista`) y no se repiten en las tablas.

| Modelo | Qué es | Atributos (tipo) |
|---|---|---|
| **Usuario** | Persona registrada | `nombreUsuario` (Char), `nombre` (Char), `apellidos` (Char), `correoElectronico` (Email), `dni` (Char), `contrasenia` (Char), `telefono` (Integer), `fechaAlta` (Date) |
| **Administrador** | Hereda de Usuario; gestiona un polideportivo | `cargo` (Char), `nivelAcceso` (Integer), `fechaNombramiento` (Date) |
| **Trabajador** | Hereda de Usuario; resuelve incidencias | `codigoDescuento` (Char), `puesto` (Char), `fechaContratacion` (Date) |
| **Descuento** | Descuento para trabajadores | `porcentaje` (Decimal), `codigo` (Char), `fechaInicio` (Date), `fechaFin` (Date), `activo` (Boolean) |
| **Direccion** | Dirección de un polideportivo | `codigoPostal` (Integer), `ciudad` (Char), `provincia` (Char), `calleNumero` (Text) |
| **Notificacion** | Aviso a usuarios | `tipo` (Char), `mensaje` (Text), `fecha_envio` (DateTime), `leida` (Boolean), `fecha_lectura` (DateTime) |
| **Sistema_Control** | Dispositivo de control de una pista | `num_serie` (Integer), `direccion_IP` (GenericIPAddress), `modelo_fabricante` (Char), `fecha_instalacion` (Date) |
| **Polideportivo** | Instalación deportiva | `nombre` (Char), `descripcion` (Text), `hora_apertura` (Time), `hora_cierre` (Time) |
| **Incidencia** | Problema en una pista | `titulo` (Char), `descripcion` (Text), `num_pista` (Integer), `fecha` (DateTime) |
| **Pista** | Pista reservable | `tipo` (Char), `estado` (Char), `metro` (Decimal), `precioHora` (Decimal) |
| **Resuelve** | Tabla intermedia Trabajador–Incidencia | `fecha_resolver` (DateTime), `observaciones` (Text) |

### Relaciones

| Tipo | Relación | Campo |
|---|---|---|
| **OneToOne** | Polideportivo – Administrador | `Polideportivo.idUsuario` |
| **OneToOne** | Polideportivo – Direccion | `Polideportivo.idDireccion` |
| **OneToOne** | Pista – Sistema_Control | `Pista.idSistema_Control` |
| **ManyToOne** | Trabajador → Descuento | `Trabajador.descuento` |
| **ManyToOne** | Pista → Polideportivo | `Pista.idPolideportivo` |
| **ManyToOne** | Pista → Usuario | `Pista.idUsuario` |
| **ManyToMany** | Usuario – Notificacion | `Usuario.notificaciones` |
| **ManyToMany** | Usuario – Incidencia | `Usuario.incidencias_reportadas` |
| **ManyToMany** | Pista – Incidencia | `Pista.incidencias` |
| **ManyToMany** (tabla intermedia con atributos extra) | Trabajador – Incidencia | `Trabajador.incidencias_resueltas` → `Resuelve` (`fecha_resolver`, `observaciones`) |

### Tipos de campo usados 

| Tipo | Para qué sirve |
|---|---|
| `AutoField` | Entero que se autoincrementa (claves primarias) |
| `CharField` | Texto corto de longitud limitada |
| `TextField` | Texto largo |
| `EmailField` | Texto que valida que sea un email |
| `IntegerField` | Número entero |
| `DecimalField` | Número decimal exacto |
| `BooleanField` | `True` / `False` |
| `DateField` | Fecha |
| `TimeField` | Hora |
| `DateTimeField` | Fecha y hora |
| `GenericIPAddressField` | Dirección IP (IPv4 o IPv6) |

## 4. Parámetros usados 

| Parámetro | Qué hace | Ejemplo |
|---|---|---|
| `max_length` | Longitud máxima del texto | `nombreUsuario` (20) |
| `unique` | No permite valores repetidos | `dni`, `correoElectronico` |
| `primary_key` | El campo es la clave primaria | `idUsuario` |
| `default` | Valor por defecto | `leida=False` |
| `null` | Permite `NULL` en la base de datos | `telefono` |
| `blank` | Permite dejar el campo vacío en formularios | `provincia` |
| `help_text` | Texto de ayuda en formularios/admin | `contrasenia` |
| `choices` | Limita los valores a una lista de opciones | `Pista.estado` |
| `max_digits` | Nº total de dígitos de un decimal | `porcentaje` (5) |
| `decimal_places` | Nº de decimales | `porcentaje` (2) |
| `db_column` | Nombre de la columna en la BD | `num_serie` → `numero_serie` |
| `on_delete` | Qué pasa al borrar el registro relacionado (`CASCADE` borra también; `SET_NULL` pone `NULL`) | `Pista.idPolideportivo` |
| `related_name` | Nombre para acceder a la relación desde el otro modelo | `polideportivo.pistas.all()` |
| `through` | Indica la tabla intermedia de un ManyToMany | `Trabajador.incidencias_resueltas` |

## 5. Código que no se vio en clase

- `default=date.today`:guarda por defecto la fecha de hoy va sin paréntesis para que calcule al crear cada registro y no una sola vez al arrancar.
- `default=timezone.now`: guarda la fecha y hora actuales va sin paréntesis para que calcule al crear cada registro y no una sola vez al arrancar.
- `default=time(9, 0)`:pone una hora fija por defecto, las 9:00 en este caso. Se usa en los TimeField de apertura y cierre del polideportivo.
- `class Administrador(Usuario)`: Administrador y Trabajador reutilizan los campos de Usuario en vez de repetirlos. Django crea una tabla por clase y las une con un OneToOne automático
- `__str__`: define el texto con el que se muestra un objeto, por ejemplo en el admin, sin él saldría algo como Pista object (1).
- `get_estado_display()`: devuelve la etiqueta legible de un campo con `choices` por ejemplo "Disponible" en vez de la clave guardada "DISP".
- `f"{self.hora_apertura:%H:%M}"`:f-string que inserta la hora con el formato horas:minutos. Así sale 09:00 en vez de 09:00:00.
- `marcar_leida()`:método de Notificacion que pone leida=True y guarda la fecha de lectura. Termina con save() para que el cambio se guarde en la base de datos.

## 6. Datos de prueba

### Comando con Faker
Con esto:
python manage.py generar_datos 
Creamos 10 registros de cada modelo y rellena las relaciones ManyToMany. 

Cosas que no se vieron en clase:

- `BaseCommand`: clase de Django de la que heredamos para crear un comando propio, que se lanza con python manage.py generar_datos. El método handle() es el que se ejecuta al lanzarlo.
- `Faker('es_ES')`: generador de datos falsos en español.
- `fake.unique.<método>()`: evita valores repetidos se usa para los campos `unique`.
- `fake.bothify('????-####')`:genera un texto con el patrón que le das. Cada ? se cambia por una letra y cada # por un número, por ejemplo ABCD-1234.
- `fake.date_between(start_date, end_date)`: fecha aleatoria en un rango.
- `fake.nif()`, `fake.sha256()`, `fake.ipv4()`, `fake.job()`, `fake.sentence()`, `fake.text()`: cada uno genera un dato falso de su tipo: un DNI, un hash para la contraseña, una IP, una profesión, una frase y un texto largo.
- `random.choice(lista)` / `random.sample(lista, n)`: choice elige un elemento al azar de la lista. sample elige n elementos distintos, sin repetir.
- `objeto.relacion.add(*lista)`: añade varios objetos a una relación ManyToMany de una sola vez. El * separa la lista en elementos sueltos, porque add los recibe uno a uno.

### Seeders
python manage.py seed sportHub --number=10

### Backup con fixture
`sportHub/fixtures/datos.json`
 # crear backup
python manage.py dumpdata sportHub --indent 4 > sportHub/fixtures/datos.json 
 # restaurar 
python manage.py loaddata datos                   

## 7. Git

- Ramas: `main`, `Configuracion_inicial`, `Modelos` y `Backups`.
- El `.gitignore` excluye lo innecesario: entorno virtual (`myvenv/`, `venv/`), `__pycache__/`, `*.pyc`, `db.sqlite3`, `.env`, `media/`, `staticfiles/`, `.vscode/`, `.idea/`.