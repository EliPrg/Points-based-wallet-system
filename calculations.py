# Archivo que contiene calculos matemáticos para el sistema de lealtad
# Importaciónes necesarias
from config import UM_puntos, Catalogo, Niveles
from decimal import Decimal
import math


# Método para calcular los puntos acumulados a partir del monto de la compra
def calcularPuntosAcum(monto, multiNivel):
    # Cálculo de los puntos acumulados a partir del monto de la compra y el nivel del cliente
    return (math.floor((Decimal(monto)/UM_puntos)*multiNivel))


# Método para buscar un premio por id dentro del catálogo (lista)
def buscarPremio(idPremio):
    for premio in Catalogo:
        if premio.idPremio == idPremio:
            return premio
    return None


# Método para calcular el nivel del cliente
def calcularNivel(puntosAcum):
    nivelActual = None
    for nombre, (umbral, multiplicador) in Niveles.items():
        if puntosAcum >= umbral:
            nivelActual = (nombre, multiplicador)
    return nivelActual


# Método para obtener el multiplicador según el nivel
def calcularMulti(nivel):
    for nombre, (umbral, multiplicador) in Niveles.items():
        if nivel == nombre:
            return multiplicador
