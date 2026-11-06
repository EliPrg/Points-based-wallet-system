# Archivo que contiene calculos matemáticos para el sistema de lealtad
# Importaciónes necesarias
from config import UM_puntos
from decimal import Decimal
import math


# Método para calcular los puntos acumulados a partir del monto de la compra
def calcularPuntosAcum(monto):
    return (math.floor((Decimal(monto)/UM_puntos)*1))
