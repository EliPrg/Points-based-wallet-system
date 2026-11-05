# Archivo que contiene las validaciones de los datos de entrada
from errors import ErrorClienteDuplicado, ErrorDatosInvalidos, ErrorClienteNoEncontrado, ErrorFechaInvalida, ErrorMontoInvalido, ErrorSaldoInsuficiente, ErrorPremioSinStock, ErrorPremioNoEncontrado
import re
import datetime


# Método para validar los datos de entrada del cliente
def validarDatosCliente(idCliente, nombre, correo, clientes):
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
    if idCliente in clientes:
        # raise una excepción si el cliente ya existe en la tabla de clientes
        raise ErrorClienteDuplicado(idCliente)


def validarFecha(fecha, fechasAlmacenadas):
    pass


# Validación de fecha valida
def validacionDeFechaValida(fecha, fechasAlmacenadas):
    # Formato para validar el formato de la fecha
    formatoFecha = r"[0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9]"

    # Validación de si la fecha ya se encuentra almacenada
    if not validarFecha(fecha, fechasAlmacenadas):
        raise ErrorFechaInvalida(fecha, "Esa fecha ya paso")

    if not isinstance(fecha, str) or not re.fullmatch(formatoFecha, fecha):
        raise ErrorFechaInvalida(fecha, "El formato es invalido para la fecha")

    # Try y Except para validar que la fecha exista
    try:
        fecha = datetime.strptime(fecha, "%d-%m-%Y").date()
    except ValueError:
        raise ErrorFechaInvalida(fecha, "la fecha no existe")


# Método para validar los datos de entrada de la compra
def validarDatosCompra(idCliente, clientes, fecha, fechasAlmacenadas, monto):
    # Validación de la existencia del cliente
    validarExistenciaCliente(idCliente, clientes)
    # Llamada del método para validar la fecha
    validacionDeFechaValida(fecha, fechasAlmacenadas)
    # Validar que el monto sea mayor a 0
    if monto <= 0:
        # Mensaje de error si el monto es inferior o igual a 0
        raise ErrorMontoInvalido(monto, "el monto es menor o igual a 0")
    # Validar que los decimales del monto no sean más de dos
    if metodoConteoDecimal(monto) > 2:
        raise ErrorMontoInvalido(monto, "el monto contiene más de 2 decimales")


# Método para validar que un cliente exista en la tabla de clientes
def validarExistenciaCliente(idCliente, clientes):
    if idCliente not in clientes:
        # raise una excepción si el cliente no existe en la tabla de clientes
        raise ErrorClienteNoEncontrado(idCliente)


# Método para validar que los datos de entrada del canje de un premio
def validarDatosCanjePremio(idCliente, clientes, idPremio, premios, fecha, fechasAlmacenadas):
    # Validación de la existencia del cliente
    validarExistenciaCliente(idCliente, clientes)
    # Llamada del método para validar la fecha
    validacionDeFechaValida(fecha, fechasAlmacenadas)
    # Validaciones del saldo
    if idPremio not in premios:
        raise ErrorPremioNoEncontrado(idPremio)
    if clientes[idCliente]["saldo"] < premios[idPremio]["costo"]:
        raise ErrorSaldoInsuficiente(clientes[idCliente]["saldo"], premios[idPremio]["costo"])
    if premios[idPremio]["stock"] <= 0:
        raise ErrorPremioSinStock(premios[idPremio]["nombre"])


def metodoConteoDecimal(numero):
    numeroCasteado = str(numero)
    numeroCasteado = numeroCasteado.split(".")
    return len(numeroCasteado[1])
