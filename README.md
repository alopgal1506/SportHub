# SportHub
# SportHub

## 1. ¿En qué consiste la web?

**SportHub** es una aplicación web para la gestión y reserva de pistas deportivas de polideportivos.

- Los usuarios se registran, reservan pistas, reciben notificaciones y reportan incidencias.
- Los trabajadores resuelven incidencias y disponen de un descuento asociado.
- Los administradores gestionan un polideportivo.
- Cada polideportivo tiene una dirección y contiene varias pistas; cada pista tiene un sistema de control y puede tener incidencias registradas.

## 2. Modelo entidad-relación
    Usuario {
        int idUsuario PK
        string nombreUsuario
        string nombre
        string apellidos
        string correoElectronico
        string dni
        string contrasenia
        int telefono
        date fechaAlta
    }
    Administrador {
        string cargo
        int nivelAcceso
        date fechaNombramiento
    }
    Trabajador {
        string codigoDescuento
        string puesto
        date fechaContratacion
    }
    Descuento {
        int idDescuento PK
        decimal porcentaje
        string codigo
        date fechaInicio
        date fechaFin
        bool activo
    }
    Direccion {
        int idDireccion PK
        int codigoPostal
        string ciudad
        string provincia
        text calleNumero
    }
    Polideportivo {
        int idPolideportivo PK
        string nombre
        text descripcion
        time hora_apertura
        time hora_cierre
    }
    Sistema_Control {
        int idSistema_Control PK
        int num_serie
        ip direccion_IP
        string modelo_fabricante
        date fecha_instalacion
    }
    Pista {
        int idPista PK
        string tipo
        string estado
        decimal metro
        decimal precioHora
    }
    Notificacion {
        int idNotificacion PK
        string tipo
        text mensaje
        datetime fecha_envio
        bool leida
        datetime fecha_lectura
    }
    Incidencia {
        int idIncidencia PK
        string titulo
        text descripcion
        int num_pista
        datetime fecha
    }
    Resuelve {
        int id PK
        datetime fecha_resolver
        text observaciones
    }

## 4. Modelos y atributos

### 4.1 `Usuario`
Persona registrada en la plataforma. Es la clase base de `Administrador` y `Trabajador`.

| Atributo | Tipo | Parámetros | Descripción |
|---|---|---|---|
| `idUsuario` | `AutoField` | `primary_key=True` | Identificador único autoincremental |
| `nombreUsuario` | `CharField` | `max_length=20`, `unique=True` | Nombre de usuario para iniciar sesión |
| `nombre` | `CharField` | `max_length=20` | Nombre de pila |
| `apellidos` | `CharField` | `max_length=50` | Apellidos |
| `correoElectronico` | `EmailField` | `max_length=200`, `unique=True` | Email (valida el formato) |
| `dni` | `CharField` | `max_length=9`, `unique=True` | DNI/NIF |
| `contrasenia` | `CharField` | `max_length=128`, `help_text` | Contraseña cifrada (hash) |
| `telefono` | `IntegerField` | `null=True`, `blank=True` | Teléfono (opcional) |
| `fechaAlta` | `DateField` | `default=date.today` | Fecha de registro |
| `notificaciones` | `ManyToManyField` → `Notificacion` | `related_name='destinatarios'`, `blank=True` | **Recibe** (N:M) |
| `incidencias_reportadas` | `ManyToManyField` → `Incidencia` | `related_name='reportada_por'`, `blank=True` | **Reporta** (N:M) |

### 4.2 `Administrador` (hereda de `Usuario`)
Usuario que gestiona un polideportivo.

| Atributo | Tipo | Parámetros | Descripción |
|---|---|---|---|
| `cargo` | `CharField` | `max_length=50` | Cargo que ocupa |
| `nivelAcceso` | `IntegerField` | `default=1`, `choices=[(1,"Básico"),(2,"Medio"),(3,"Total")]` | Nivel de permisos |
| `fechaNombramiento` | `DateField` | `default=date.today` | Fecha en la que fue nombrado |

### 4.3 `Trabajador` (hereda de `Usuario`)
Empleado del polideportivo que resuelve incidencias.

| Atributo | Tipo | Parámetros | Descripción |
|---|---|---|---|
| `codigoDescuento` | `CharField` | `max_length=20`, `unique=True` | Código personal de descuento |
| `puesto` | `CharField` | `max_length=50` | Puesto de trabajo |
| `fechaContratacion` | `DateField` | — | Fecha de contratación |
| `descuento` | `ForeignKey` → `Descuento` | `on_delete=CASCADE`, `related_name='trabajadores'` | **Aplica** (N:1) |
| `incidencias_resueltas` | `ManyToManyField` → `Incidencia` | `through='Resuelve'`, `related_name='resolutores'`, `blank=True` | **Resuelve** (N:M con tabla intermedia) |

### 4.4 `Descuento`
Descuentos aplicables a trabajadores.

| Atributo | Tipo | Parámetros | Descripción |
|---|---|---|---|
| `idDescuento` | `AutoField` | `primary_key=True` | Identificador |
| `porcentaje` | `DecimalField` | `max_digits=5`, `decimal_places=2` | Porcentaje de descuento (ej. 15.00) |
| `codigo` | `CharField` | `max_length=20`, `unique=True` | Código del descuento |
| `fechaInicio` | `DateField` | `default=date.today` | Inicio de validez |
| `fechaFin` | `DateField` | `null=True`, `blank=True` | Fin de validez (opcional) |
| `activo` | `BooleanField` | `default=True` | Si está en vigor |

### 4.5 `Direccion`
Dirección postal de un polideportivo.

| Atributo | Tipo | Parámetros | Descripción |
|---|---|---|---|
| `idDireccion` | `AutoField` | `primary_key=True` | Identificador |
| `codigoPostal` | `IntegerField` | — | Código postal |
| `ciudad` | `CharField` | `max_length=50` | Ciudad |
| `provincia` | `CharField` | `max_length=50`, `blank=True` | Provincia (opcional) |
| `calleNumero` | `TextField` | — | Calle y número |

### 4.6 `Notificacion`
Avisos enviados a los usuarios.

| Atributo | Tipo | Parámetros | Descripción |
|---|---|---|---|
| `idNotificacion` | `AutoField` | `primary_key=True` | Identificador |
| `tipo` | `CharField` | `max_length=50`, `choices=TIPOS`, `default="RESER"` | Reserva / Anular / Registrado |
| `mensaje` | `TextField` | — | Texto de la notificación |
| `fecha_envio` | `DateTimeField` | `default=timezone.now` | Momento del envío |
| `leida` | `BooleanField` | `default=False` | Si el usuario la ha leído |
| `fecha_lectura` | `DateTimeField` | `null=True`, `blank=True` | Momento de lectura |

Método `marcar_leida()`: pone `leida=True`, guarda la fecha actual en `fecha_lectura` y hace `save()`.

### 4.7 `Sistema_Control`
Dispositivo de control (acceso/iluminación) instalado en una pista.

| Atributo | Tipo | Parámetros | Descripción |
|---|---|---|---|
| `idSistema_Control` | `AutoField` | `primary_key=True` | Identificador |
| `num_serie` | `IntegerField` | `default=0`, `db_column='numero_serie'` | Número de serie (la columna en BD se llama `numero_serie`) |
| `direccion_IP` | `GenericIPAddressField` | — | IP del dispositivo (IPv4/IPv6) |
| `modelo_fabricante` | `CharField` | `max_length=6` | Modelo del fabricante |
| `fecha_instalacion` | `DateField` | `default=date.today` | Fecha de instalación |

### 4.8 `Polideportivo`
Instalación deportiva.

| Atributo | Tipo | Parámetros | Descripción |
|---|---|---|---|
| `idPolideportivo` | `AutoField` | `primary_key=True` | Identificador |
| `nombre` | `CharField` | `max_length=50` | Nombre |
| `descripcion` | `TextField` | `blank=True` | Descripción (opcional) |
| `hora_apertura` | `TimeField` | `default=time(9, 0)` | Hora de apertura |
| `hora_cierre` | `TimeField` | `default=time(22, 0)` | Hora de cierre |
| `idUsuario` | `OneToOneField` → `Administrador` | `on_delete=CASCADE`, `related_name='polideportivo'` | **Gestiona** (1:1) |
| `idDireccion` | `OneToOneField` → `Direccion` | `on_delete=CASCADE`, `related_name='polideportivo'` | **Localiza** (1:1) |

### 4.9 `Incidencia`
Problema detectado en una pista.

| Atributo | Tipo | Parámetros | Descripción |
|---|---|---|---|
| `idIncidencia` | `AutoField` | `primary_key=True` | Identificador |
| `titulo` | `CharField` | `max_length=100` | Título breve |
| `descripcion` | `TextField` | — | Descripción detallada |
| `num_pista` | `IntegerField` | — | Número de pista afectada |
| `fecha` | `DateTimeField` | `default=timezone.now` | Cuándo se creó |

### 4.10 `Pista`
Pista deportiva reservable.

| Atributo | Tipo | Parámetros | Descripción |
|---|---|---|---|
| `idPista` | `AutoField` | `primary_key=True` | Identificador |
| `tipo` | `CharField` | `max_length=50` | Deporte (Tenis, Pádel…) |
| `estado` | `CharField` | `max_length=20`, `choices=ESTADOS`, `default="DISP"` | Disponible / Ocupada / Mantenimiento |
| `metro` | `DecimalField` | `max_digits=6`, `decimal_places=2` | Metros cuadrados |
| `precioHora` | `DecimalField` | `max_digits=6`, `decimal_places=2`, `default=10` | Precio por hora |
| `idUsuario` | `ForeignKey` → `Usuario` | `on_delete=SET_NULL`, `null=True`, `blank=True`, `related_name='pistas_reservadas'` | **Reserva** (N:1) |
| `idPolideportivo` | `ForeignKey` → `Polideportivo` | `on_delete=CASCADE`, `related_name='pistas'` | **Contiene** (N:1) |
| `idSistema_Control` | `OneToOneField` → `Sistema_Control` | `on_delete=CASCADE`, `related_name='pista'` | **Pertenece** (1:1) |
| `incidencias` | `ManyToManyField` → `Incidencia` | `related_name='pistas'`, `blank=True` | **Registra** (N:M) |

### 4.11 `Resuelve` (tabla intermedia N:M con atributos extra)
Une `Trabajador` e `Incidencia` y guarda datos de la resolución.

| Atributo | Tipo | Parámetros | Descripción |
|---|---|---|---|
| `idUsuario` | `ForeignKey` → `Trabajador` | `on_delete=CASCADE` | Trabajador que resuelve |
| `idIncidencia` | `ForeignKey` → `Incidencia` | `on_delete=CASCADE` | Incidencia resuelta |
| `fecha_resolver` | `DateTimeField` | `default=timezone.now` | Cuándo se resolvió (**extra**) |
| `observaciones` | `TextField` | `blank=True` | Notas del trabajador (**extra**) |

---

## 5. Resumen de requisitos de los modelos

### Relaciones
| Tipo | Relaciones |
|---|---|
| **OneToOne** (3) | `Polideportivo`–`Administrador` (Gestiona), `Polideportivo`–`Direccion` (Localiza), `Pista`–`Sistema_Control` (Pertenece). Además, `Administrador` y `Trabajador` tienen un OneToOne implícito con `Usuario` por herencia |
| **ManyToOne** (3) | `Trabajador`→`Descuento` (Aplica), `Pista`→`Polideportivo` (Contiene), `Pista`→`Usuario` (Reserva) |
| **ManyToMany** (4) | `Usuario`↔`Notificacion` (Recibe), `Usuario`↔`Incidencia` (Reporta), `Pista`↔`Incidencia` (Registra), `Trabajador`↔`Incidencia` (Resuelve, **con tabla intermedia `Resuelve`** y atributos extra `fecha_resolver` y `observaciones`) |

### Tipos de atributo usados (11 distintos, sin contar relaciones)
`AutoField`, `CharField`, `EmailField`, `IntegerField`, `DecimalField`, `BooleanField`, `TextField`, `DateField`, `TimeField`, `DateTimeField`, `GenericIPAddressField`.

---

## 6. Parámetros usados en los atributos

| Parámetro | Qué hace | Dónde se usa (ejemplo) |
|---|---|---|
| `max_length` | Longitud máxima de un campo de texto | `nombreUsuario` (20) |
| `unique` | No permite valores repetidos en la tabla | `dni`, `correoElectronico`, `codigo` |
| `primary_key` | El campo es la clave primaria | `idUsuario`, `idPista`… |
| `default` | Valor por defecto (puede ser un valor o una función que se evalúa al crear el registro) | `fechaAlta=date.today`, `leida=False` |
| `null` | Permite `NULL` en la base de datos | `telefono`, `fechaFin` |
| `blank` | Permite dejar el campo vacío en formularios/validación | `provincia`, `descripcion` |
| `help_text` | Texto de ayuda mostrado en formularios y admin | `contrasenia` |
| `choices` | Limita los valores a una lista de pares `(valor, etiqueta)` | `nivelAcceso`, `Notificacion.tipo`, `Pista.estado` |
| `max_digits` | Nº total de dígitos de un decimal | `porcentaje` (5), `metro` (6) |
| `decimal_places` | Nº de decimales de un decimal | `porcentaje` (2) |
| `db_column` | Nombre de la columna en la BD distinto al del atributo | `num_serie` → `numero_serie` |
| `on_delete` | Qué pasa al borrar el objeto referenciado (`CASCADE` borra también este registro; `SET_NULL` pone el campo a `NULL`) | Todas las relaciones |
| `related_name` | Nombre para acceder a la relación desde el modelo opuesto | `polideportivo.pistas.all()` |
| `through` | Indica la tabla intermedia de un ManyToMany | `Trabajador.incidencias_resueltas` |

### Código adicional que no se vio en clase
- **`default=date.today` / `timezone.now`**: se pasa la *función sin paréntesis* para que se ejecute cada vez que se crea un registro, no una sola vez al arrancar.
- **`default=time(9, 0)`**: objeto `datetime.time` con hora y minutos.
- **Herencia multi-tabla** (`class Administrador(Usuario)`): Django crea una tabla por cada clase y las une con un `OneToOne` automático (`usuario_ptr`).
- **`__str__`**: define el texto con el que se muestra el objeto (admin, shell). `get_estado_display()` devuelve la etiqueta legible de un campo con `choices`.
- **`f"{self.hora_apertura:%H:%M}"`**: f-string con formato de hora.
- **`db_column`**: ver tabla anterior.

---

## 7. Datos de prueba

### 7.1 Comando con Faker: `generar_datos`
`sportHub/management/commands/generar_datos.py`

```bash
python manage.py generar_datos
```

Crea **10 registros de cada modelo** (direcciones, descuentos, usuarios, administradores, trabajadores, notificaciones, sistemas de control, polideportivos, pistas, incidencias y 10 filas de `Resuelve`) y rellena las relaciones N:M.

Elementos usados que no se vieron en clase:
- `BaseCommand`: clase base de los comandos personalizados de Django; el método `handle()` es el que se ejecuta con `manage.py`.
- `Faker('es_ES')`: generador de datos falsos con localización española.
- `fake.unique.<método>()`: garantiza que no se repitan valores (necesario en campos `unique`).
- `fake.bothify('????-####')`: sustituye `?` por letras y `#` por números.
- `fake.date_between(start_date, end_date)`: fecha aleatoria en un rango.
- `fake.nif()`, `fake.sha256()`, `fake.ipv4()`, `fake.job()`, `fake.sentence()`, `fake.text()`: DNI, hash, IP, profesión, frase y texto.
- `random.choice(lista)` / `random.sample(lista, n)`: elige un elemento / `n` elementos distintos.
- `objeto.relacion.add(*lista)`: añade varios objetos a un ManyToMany (el `*` desempaqueta la lista).

### 7.2 Seeders
Las tablas se rellenan mediante el comando anterior y también se pueden rellenar con `django-seed`:

```bash
python manage.py seed sportHub --number=10
```

### 7.3 Backup con fixture
`sportHub/fixtures/datos.json`

```bash
python manage.py dumpdata sportHub --indent 4 > sportHub/fixtures/datos.json   # crear
python manage.py loaddata datos                                                  # restaurar
```

---

## 8. Archivos no subidos a Git
El `.gitignore` excluye: entornos virtuales (`venv/`, `.venv/`), `__pycache__/` y `*.pyc`, la base de datos `db.sqlite3`, `.env`, `media/`, `staticfiles/`, `.vscode/`, `.idea/` y archivos del sistema (`.DS_Store`).