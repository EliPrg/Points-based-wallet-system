# Archivo que contiene calculos matemáticos para el sistema de lealtad
# Importaciónes necesarias
from config import UM_puntos


# Método para validar que la fecha ingresada no sea mayor a la ultima fecha ingresada
def validarFecha(fecha, fechasAlmacenadas):
    pass


# Método para contar los decimales de un número
def metodoConteoDecimal(numero):
    numeroCasteado = str(numero)
    numeroCasteado = numeroCasteado.split(".")
    return len(numeroCasteado[1])


# Método para calcular los puntos acumulados a partir del monto de la compra
def calcularPuntosAcum(monto: float):
    return ((monto/UM_puntos)*1)