# Archivo que contiene las validaciones de los datos de entrada
from errors import ErrorDatosInvalidos
import re

def validarDatosCliente(idCliente, nombre, correo):
    # Definición de expresiones regulares
    expresionId = r"[A-Za-z0-9]+"
    expresionNombre = r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ][A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]*"
    expresionCorreo = r"[^@\s]+@[^@\s]+\.[^@\s.]+"
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
