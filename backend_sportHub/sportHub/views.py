from django.shortcuts import render
from django.db.models import Avg, Max, Min, Count
from django.views.defaults import page_not_found
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.http import Http404
from .models import Pista, Polideportivo, Usuario, Administrador, Direccion, Incidencia
from django.db.models import Q
from django.db.models import Prefetch

# Create your views here.
def index(request):
    return render(request, 'index.html')

    # Mostar todas las pistas disponibles de un polideportivo
def pistasDisponibles(request, idPoli, nuevoEstado):
    pistas = Pista.objects.select_related("idPolideportivo").filter(idPolideportivo = idPoli, estado = nuevoEstado)
    return render(request,'pistasDisponibles.html',{'pistas':pistas})


"""
def pistasDisponibles(request, idPoli, nuevoEstado):
    pistas = Pista.objects.raw(
        "SELECT pista.*, polideportivo.nombre, usuario.nombreUsuario "
        "FROM sportHub_pista pista "
        "INNER JOIN sportHub_polideportivo polideportivo ON pista.idPolideportivo_id = polideportivo.idPolideportivo "
        "LEFT JOIN sportHub_usuario usuario ON pista.idUsuario_id = usuario.idUsuario "
        "WHERE pista.idPolideportivo_id = %s AND pista.estado = %s",
        [idPoli, nuevoEstado]
    )
    return render(request, 'pistasDisponibles.html', {'pistas': pistas})
"""

    #Mostrar todos los polideportivos que administra un administardor en una ciudad en concreto
def polideportivo(requets, idAdmin, nombreCiudad):
    polideportivo = Polideportivo.objects.select_related('idUsuario', 'idDireccion').filter(idUsuario = idAdmin, idDireccion__ciudad=nombreCiudad)
    return render(requets, 'polideportivo.html', {'polideportivo': polideportivo})

"""
def polideportivo(request, idAdmin, nombreCiudad):
    polideportivo = Polideportivo.objects.raw(
        "SELECT poli.*, admin.cargo, admin.nivelAcceso, usuario.nombreUsuario, "
        "direccion.ciudad, direccion.calleNumero, direccion.codigoPostal "
        "FROM sportHub_polideportivo poli "
        "INNER JOIN sportHub_administrador admin ON poli.idUsuario_id = admin.usuario_ptr_id "
        "INNER JOIN sportHub_usuario usuario ON admin.usuario_ptr_id = usuario.idUsuario "
        "INNER JOIN sportHub_direccion direccion ON poli.idDireccion_id = direccion.idDireccion "
        "WHERE poli.idUsuario_id = %s AND direccion.ciudad = %s",
        [idAdmin, nombreCiudad]
    )
    return render(request, 'polideportivo.html', {'polideportivo': polideportivo})
"""

    #Pistas filtradas por tipo y estado
def pistasFiltradas(request, nuevoTipo ,nuevoEstado):
    pistas = Pista.objects.filter(tipo=nuevoTipo,estado=nuevoEstado)
    return render(request,'pistasFiltradas.html', {'pistas':pistas})


"""
    def pistasFiltradas(request, nuevoTipo, nuevoEstado):
    pistas = Pista.objects.raw(
        "SELECT * FROM Pista WHERE tipo = %s AND estado = %s",
        [nuevoTipo, nuevoEstado]
    )
    return render(request, 'pistasFiltradas.html', {'pistas': pistas})
"""
    # Incidencias cuyo titulo o descripcion contenga el texto con sus vistas
def pistasConIncidencias(request, texto):
    incidencia = Pista.objects.prefetch_related('incidencias').filter(Q(incidencias__titulo__icontains=texto) | Q(incidencias__descripcion__icontains=texto) )
    return render(request, 'pistasConIncidencias.html', {'incidencia': incidencia, 'texto': texto})


"""
def pistasConIncidencias(request, texto):
    incidencia = Pista.objects.raw(
        "SELECT DISTINCT pista.* "
        "FROM sportHub_pista pista "
        "INNER JOIN sportHub_pista_incidencias pi ON pista.idPista = pi.pista_id "
        "INNER JOIN sportHub_incidencia inc ON pi.incidencia_id = inc.idIncidencia "
        "WHERE inc.titulo LIKE '%%' || %s || '%%' "
        "OR inc.descripcion LIKE '%%' || %s || '%%'",
        [texto, texto]
    )
    return render(request, 'pistasConIncidencias.html', {'incidencia': incidencia, 'texto': texto})
"""
    # Incidencia en un año en concreto
def incidenciasPorAno(request, ano):
    incidencias = Incidencia.objects.filter(fecha__year=ano).prefetch_related(Prefetch('pistas', queryset=Pista.objects.select_related('idPolideportivo', 'idSistema_Control', 'idUsuario'))).order_by('-fecha')
    return render(request, 'incidenciasPorAno.html', {'incidencias': incidencias,'ano': ano})
"""
    def incidenciasPorAno(request, ano):
    incidencias = Incidencia.objects.raw(
        "SELECT * FROM Incidencia WHERE YEAR(fecha) = %s ORDER BY fecha DESC",
        [ano]
    )
    return render(request, 'incidenciasPorAno.html', {'incidencias': incidencias, 'ano': ano})
    
"""

    # Precio AVG, MAX, MIN y el count de las pistas
def listaPrecios(request):
    precio = Pista.objects.aggregate(Avg("precioHora"), Max("precioHora"), Min("precioHora"), Count("idPista"))
    media = precio["precioHora__avg"]
    maximo = precio["precioHora__max"]
    minimo = precio["precioHora__min"]
    total = precio["idPista__count"]
    return render(request, 'listaPrecios.html', {"media": media,"maximo": maximo,"minimo": minimo,"total": total,})

"""
    SELECT 
    AVG(precioHora) AS media,
    MAX(precioHora) AS maximo,
    MIN(precioHora) AS minimo,
    COUNT(idPista) AS total
    FROM Pista;
"""


def mi_error_400(request,exception=None):
    return render(request, 'errores/400.html',None,None,400)

def mi_error_403(request,exception=None):
    return render(request, 'errores/403.html',None,None,403)

def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

def mi_error_500(request):
    return render(request, 'errores/500.html',None,None,500)


# VISTAS TEMPORALES PARA PROBAR LOS ERRORES

def probar_400(request):
    raise SuspiciousOperation("Prueba intencional del error 400")

def probar_403(request):
    raise PermissionDenied("Prueba intencional del error 403")

def probar_404(request):
    raise Http404("Prueba intencional del error 404")

def probar_500(request):
    resultado = 1 / 0  # Esto fuerza un error 500 
    return render(request, 'inicio.html')





