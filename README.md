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
Todas las claves primarias son **`AutoField*(primary_key=True)` (`idUsuario`, `idPista`) y no se repiten en las tablas.

| Modelo | Qué es | Atributos (tipo) |

**Usuario** | Persona registrada | `nombreUsuario` (Char), `nombre` (Char), `apellidos` (Char), `correoElectronico` (Email), `dni` (Char), `contrasenia` (Char), `telefono` (Integer), `fechaAlta` (Date) 

**Administrador** | Hereda de Usuario; gestiona un polideportivo | `cargo` (Char), `nivelAcceso` (Integer), `fechaNombramiento` (Date) 

**Trabajador** | Hereda de Usuario; resuelve incidencias | `codigoDescuento` (Char), `puesto` (Char), `fechaContratacion` (Date)

**Descuento** | Descuento para trabajadores | `porcentaje` (Decimal), `codigo` (Char), `fechaInicio` (Date), `fechaFin` (Date), `activo` (Boolean)

**Direccion** | Dirección de un polideportivo | `codigoPostal` (Integer), `ciudad` (Char), `provincia` (Char), `calleNumero` (Text)

**Notificacion** | Aviso a usuarios | `tipo` (Char), `mensaje` (Text), `fecha_envio` (DateTime), `leida` (Boolean), `fecha_lectura` (DateTime)

**Sistema_Control** | Dispositivo de control de una pista | `num_serie` (Integer), `direccion_IP` (GenericIPAddress), `modelo_fabricante` (Char), `fecha_instalacion` (Date)

**Polideportivo** | Instalación deportiva | `nombre` (Char), `descripcion` (Text), `hora_apertura` (Time), `hora_cierre` (Time)

**Incidencia** | Problema en una pista | `titulo` (Char), `descripcion` (Text), `num_pista` (Integer), `fecha` (DateTime)

**Pista** | Pista reservable | `tipo` (Char), `estado` (Char), `metro` (Decimal), `precioHora` (Decimal)

**Resuelve** | Tabla intermedia Trabajador–Incidencia | `fecha_resolver` (DateTime), `observaciones` (Text)

### Relaciones

| Tipo | Relación | Campo |
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
| `AutoField` | Entero que se autoincrementa  |
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

## 8. URLs de la aplicación

Todas las URLs son accesibles desde el index (`/`). Los valores de los enlaces del index están elegidos para que existan en el fixture y muestren resultados.

| Nº | URL | Vista | Qué hace |
|---|---|---|---|
| 1 | `pistas/disponibles/<int:idPoli>/<str:nuevoEstado>/` | `pistasDisponibles` | Muestra las pistas de un polideportivo con un estado concreto, con su polideportivo y su usuario |
| 2 | `polideportivo/<int:idAdmin>/<str:nombreCiudad>/` | `polideportivo` | Muestra los polideportivos que administra un administrador en una ciudad, con administrador y dirección |
| 3 | `pistas/<str:nuevoTipo>/<str:nuevoEstado>/` | `pistasFiltradas` | Muestra las pistas filtradas por tipo y estado |
| 4 | `incidencia/<str:texto>/` | `pistasConIncidencias` | Muestra las pistas con alguna incidencia cuyo título o descripción contenga el texto |
| 5 | `incidencias/ano/(\d{4})/` | `incidenciasPorAno` | Muestra las incidencias de un año, de más reciente a más antigua, con sus pistas |
| 6 | `precios/` | `listaPrecios` | Muestra el precio medio, máximo y mínimo por hora y el total de pistas |
| 7 | `incidencias/sin-resolver/` | `incidencias_sin_resolver` | Muestra las incidencias que ningún trabajador ha resuelto |
| 8 | `notificaciones/<int:id>/` | `notificaciones_usuario` | Muestra las 5 últimas notificaciones de un usuario |
| 9 | `trabajadores/descuento/` | `trabajadores_descuento` | Muestra los trabajadores con descuento inferior al 15 % y sus incidencias resueltas |
| 10 | `trabajadores/incidencias/` | `trabajadores_incidencias` | Muestra los trabajadores y las incidencias que han resuelto |

Cada vista tiene un comentario que explica qué hace y, debajo, la consulta equivalente en SQL comentada.

## 9. Requisitos que cumple cada URL

| Requisito | URL(s) donde se cumple |
|---|---|
| URL con `re_path` | 5 |
| URL con dos parámetros | 1, 2, 3 |
| URL con un parámetro entero | 8 (y el entero de 1 y 2) |
| URL con un parámetro `str` | 4 (y el `str` de 1, 2 y 3) |
| Filtro con AND | 1, 2, 3 |
| Filtro con OR | 4 (`Q(...) \| Q(...)`) |
| `aggregate` | 6 |
| Relación reversa | 7 (`resolutores`), 8 (`destinatarios`), 5 (`pistas`) |
| `order_by` | 5, 8 |
| Límite (`[:5]`) | 8 |
| Filtro con `None` en tabla intermedia | 7 (`resolutores__isnull=True`, tabla `Resuelve`) |
| Datos de **ManyToOne** | 1 (Pista → Polideportivo y Usuario), 9 (Trabajador → Descuento) |
| Datos de **OneToOne** | 2 (Polideportivo ↔ Administrador y Dirección), 5 (Pista ↔ Sistema_Control) |
| Datos de **ManyToMany** | 4, 5 (Pista ↔ Incidencia), 8 (Usuario ↔ Notificación), 9 y 10 (Trabajador ↔ Incidencia con `Resuelve`) |
| Consultas optimizadas | `select_related` (ManyToOne y OneToOne) y `prefetch_related` (ManyToMany) en las vistas que muestran modelos relacionados |
| SQL comentado | Todas las vistas |

## 10. Páginas de error personalizadas

| Error | Plantilla | Handler en `configuracionSportHub/urls.py` |
|---|---|---|
| 400 | `templates/errores/400.html` | `handler400 = 'sportHub.views.mi_error_400'` |
| 403 | `templates/errores/403.html` | `handler403 = 'sportHub.views.mi_error_403'` |
| 404 | `templates/errores/404.html` | `handler404 = 'sportHub.views.mi_error_404'` |
| 500 | `templates/errores/500.html` | `handler500 = 'sportHub.views.mi_error_500'` |

Solo se muestran con `DEBUG = False` (modo producción). Para probarlas: `/pagina-que-no-existe/` (404). El 400, el 403 y el 500 se comprobaron con vistas temporales que lanzaban `SuspiciousOperation`, `PermissionDenied` y una división por cero, y se eliminaron después.

## 11. Código que no se vio en clase

- **`aggregate()`** (URL 6): calcula un valor resumen sobre toda la tabla en una sola consulta, sin agrupar. Devuelve un diccionario con claves `campo__funcion`, por ejemplo `precioHora__avg`. Se usan `Avg`, `Max`, `Min` y `Count`, que se importan de `django.db.models`.
- **`Q()`** (URL 4): permite combinar condiciones con `|` (OR) y `&` (AND) en un `filter`. Sin `Q`, los filtros solo se pueden unir con AND.
- **`.distinct()`** (URL 4): elimina filas repetidas. Al filtrar por una relación ManyToMany, una pista con varias incidencias coincidentes aparecería varias veces.
- **`re_path`** (URL 5): define la URL con una expresión regular. `(\d{4})` exige exactamente 4 dígitos y los pasa a la vista como parámetro.
- **`Prefetch()`** (URL 5): permite indicar qué consulta se usa en `prefetch_related`, aquí para traer las pistas ya con su polideportivo, su sistema de control y su usuario.
- **`fecha__year`** (URL 5): filtra un campo de fecha por el año.
- **`__isnull=True`** (URL 7): filtra por registros sin relación. Con la tabla intermedia `Resuelve`, devuelve las incidencias que no tienen ningún trabajador resolutor.
- **`__lt`** (URL 9): "menor que", se usa para el descuento inferior al 15 %.
- **`[:5]`** (URL 8): corta el resultado a 5 registros. Equivale a `LIMIT 5` en SQL.
- **`raw()`** (solo en el SQL comentado): ejecuta una consulta SQL escrita a mano. Los `%s` son parámetros y el `%` literal se escribe `%%`.
- **`strftime('%%Y', fecha)`** (SQL comentado de la URL 5): extrae el año en SQLite, que no tiene la función `YEAR()`.
- **`handler400/403/404/500`**: variables de `urls.py` que indican qué vista se usa para cada error.

## 12. Cómo lanzar el proyecto

```
git clone https://github.com/alopgal1506/SportHub.git
cd SportHub/backend_sportHub
python -m venv myvenv
source myvenv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata datos
python manage.py runserver
```

Después se abre `http://127.0.0.1:8000/`. El proyecto está en modo producción (`DEBUG = False`).