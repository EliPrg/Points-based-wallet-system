# Archivo que contiene calculos matemáticos para el sistema de lealtad
# Importaciónes necesarias
from config import UM_puntos, Catalogo
from decimal import Decimal
import math


# Método para calcular los puntos acumulados a partir del monto de la compra
def calcularPuntosAcum(monto):
    return (math.floor((Decimal(monto)/UM_puntos)*1))


# Método para buscar un premio por id dentro del catálogo (lista)
def buscarPremio(idPremio):
    for premio in Catalogo:
        if premio.id_premio == idPremio:
            return premio
    return None
