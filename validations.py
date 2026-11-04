# Archivo que contiene las validaciones de los datos de entrada
from errors import ErrorDatosInvalidos, ErrorClienteNoEncontrado, ErrorFechaInvalida
import re
import datetime

# Método para validar los datos de entrada del cliente
def validarDatosCliente(idCliente, nombre, correo):
    # Definición de expresiones regulares
    expresionId = r"[A-Za-z0-9]+"
    expresionNombre = r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ][A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]*"
    expresionCorreo = r"[^@\s]+@[^@\s.]+\.[^@\s.]+"
    # validación de los datos de entrada
    if not isinstance(idCliente, str) or not re.fullmatch(expresionId, idCliente):
        # raise una excepción si el idCliente no cumple con el formato solicitado
        raise ErrorDatosInvalidos("idCliente", idCliente)
    if not isinstance(nombre, str) or not re.fullmatch(expresionNombre, nombre):
        # raise una excepción si el nombre no cumple con el formato solicitado
        raise ErrorDatosInvalidos("nombre", nombre)
    if not isinstance(correo, str) or not re.fullmatch(expresionCorreo, correo):
        # raise una excepción si el correo no cumple con el formato solicitado
        raise ErrorDatosInvalidos("correo", correo)

def validarFecha(fecha, fechasAlmacenadas):
    pass


# Validación de fecha valida
def validacionDeFechaValida(fecha, fechasAlmacenadas):
    # Formato para validar el formato de la fecha
    formatoFecha=r"[0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9]"

    # Validación de si la fecha ya se encuentra almacenada
    if validarFecha(fecha,fechasAlmacenadas) == False:
        raise ErrorFechaInvalida(fecha,"Esa fecha ya paso")
    
    if not isinstance(fecha, str) or not re.fullmatch(formatoFecha, fecha):
        raise ErrorFechaInvalida(fecha, "El formato es invalido para la fecha")

    # Try y Except para validar que la fecha exista
    try:
        fecha = datetime.strptime(fecha, "%d-%m-%Y").date()
    except ValueError:
        raise ErrorFechaInvalida(fecha, "la fecha no existe")


# Método para validar los datos de entrada de la compra
def validarDatosCompra(idCliente, clientes, fecha, fechasAlmacenadas):
    # Validación de la existencia del cliente
    if idCliente not in clientes:
        # raise una excepción si el cliente no existe en la tabla de clientes
        raise ErrorClienteNoEncontrado(idCliente)

    # Llamada del método para validar la fecha
    validacionDeFechaValida(fecha,fechasAlmacenadas)

    
    